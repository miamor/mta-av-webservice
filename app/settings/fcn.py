import app.settings.cf as cf
import os
import json
import time

from app.modules.common.controller import Controller
from app.modules.malware.capture import Capture
from app.modules.malware.controller_capture import ControllerCapture
from app.modules.notification.controller_noti import ControllerNoti
# from sqlalchemy import text
from app.app import db
from app.settings.config import Config

from werkzeug.utils import secure_filename
from app.utils.response import error, result
from multiprocessing import Pool

from app.modules.detector.detection_module import Detector
if not cf.set_detector:
    cf.set_detector = True
    cf.detector = Detector()

from app.modules.detector.sandbox import Sandbox_API
cf.sandbox = Sandbox_API(cuckoo_API=cf.cuckoo_API, SECRET_KEY=cf.cuckoo_SECRET_KEY,
                         hash_type=cf.hash_type, timeout=cf.cuckoo_timeout)



def submit_cuckoo(filepaths):
    task_ids = []
    for filepath in filepaths:
        # task_id = cf.detector.run_sandbox(filepath)
        task_id = cf.sandbox.start_analysis(filepath)
        task_ids.append(task_id)

    return task_ids


def upload_file_submit_cuckoo(files):
    # filenames = []
    filepaths = []
    task_ids = []

    for i in range(len(files)):
        file = files[i]

        if file.filename == "":
            continue

        # if file and allowed_file(file.filename):
        if file:
            # upload file
            filename = secure_filename(file.filename)
            filepath = os.path.join(cf.UPLOAD_FOLDER, filename)
            file.save(filepath)

            # filenames.append(filename)
            filepaths.append(filepath)

            # submit to cuckoo
            # task_id = cf.detector.run_sandbox(filepath)
            task_id = cf.sandbox.start_analysis(filepath)
            task_ids.append(task_id)

    return filepaths, task_ids



cf.is_processing = False

def get_unprocessed():
    while True:
        if not cf.is_processing: # if no task is being processed
            # load unprocessed from database
            cmd = "select * from capture where detected_by is null and file_path is not null and task_id is not null order by capture_id asc limit 0,{}".format(
                cf.process_batch_size)

            captures_unprocessed = cf.connection.execute(cmd).fetchall()

            # if found unprocessed task
            if captures_unprocessed is not None and len(captures_unprocessed) > 0:
                cf.is_processing = True # lock

                filepaths = []
                task_ids = []
                for capture_unprocessed in captures_unprocessed:
                    print('[check] #', 'capture_unprocessed', capture_unprocessed)
                    # filepaths, task_ids, task_data = data
                    filepaths.append(capture_unprocessed.file_path)
                    task_ids.append(capture_unprocessed.task_id)
                
                cf.__tasks_to_run_detector__.put((filepaths, task_ids, captures_unprocessed))

            print('[get_unprocessed] Sleep for 10s')
            time.sleep(10)

def get_done_to_update():
    while True:
        if cf.__tasks_done__.empty():
            print('[check] No task in [cf.__tasks_done__] queue. Sleep 1s then check again')
            time.sleep(10)
        else:
            captures_data_new, captures_unprocessed = cf.__tasks_done__.get()
            links = []
            filenames = []
            for i in range(len(captures_unprocessed)):
                # update capture database
                cf.controllerCapture._parse_malware(data=captures_data_new[i], capture_id=captures_unprocessed[i].capture_id)
                db.session.commit()

                links.append(str(captures_unprocessed[i].capture_id))
                filenames.append(captures_unprocessed[i].file_name)

            # add notification
            noti_data = {
                'user_id': 2,
                'message': 'Xử lý thành công các file {}. Xem chi tiết tại: <<{}>>'.format(', '.join(filenames), '|'.join(links))
            }
            cf.controllerNoti.create(data=noti_data)

            cf.__tasks_done__.task_done()


def check():
    print('[check] **** CALL check')

    t_engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
    t_connection = t_engine.connect()
    controllerCapture = ControllerCapture()
    controllerNoti = ControllerNoti()
    
    cmd = "select * from capture where detected_by is null and file_path is not null and task_id is not null order by capture_id asc limit 0,{}".format(cf.process_batch_size)

    # if True:
    while True:
        # print('[check] ~~ cf.is_processing', cf.is_processing)
        # if cf.__tasks_to_run_detector__.empty():
        #     print('[check] No task in [cf.__tasks_to_run_detector__] queue. Sleep 1s then check again')
        #     time.sleep(10)
        # else:
        #     filepaths, task_ids, captures_unprocessed = cf.__tasks_to_run_detector__.get()

        # Process by batch.
        # Load a batch of {batch_size} files unprocessed in database
        if cf.is_processing:
            print('[check] Some task is processing. Sleep 10s then check again')
            time.sleep(10)
        else:
            print('[check] Run process')
            # load unprocessed from database
            # captures_unprocessed_proxy = t_connection.execute(cmd).fetchall()
            # # captures_unprocessed = Capture.query.filter(db.and_(Capture.detected_by == None, Capture.file_path != None, Capture.task_id != None)).order_by(Capture.capture_id.asc()).fetchall()
            # print('[check] captures_unprocessed_proxy', captures_unprocessed)

            captures_unprocessed = t_connection.execute(cmd).fetchall()
            print('[check] captures_unprocessed', captures_unprocessed)

            # t_connection.execute(capture.update().where(capture.capture_id == ).values(foo="bar"))

            # if found unprocessed task
            # if captures_unprocessed_proxy is not None and len(captures_unprocessed_proxy) > 0:
            if captures_unprocessed is not None and len(captures_unprocessed) > 0:
                cf.is_processing = True # lock

                filepaths = []
                task_ids = []
                # for capture_unprocessed_proxy in captures_unprocessed_proxy:
                #     capture_unprocessed = dict(capture_unprocessed_proxy.items())
                print('[check] *** captures_unprocessed', captures_unprocessed)
                for capture_unprocessed in captures_unprocessed:
                    print('[check] #', 'capture_unprocessed', capture_unprocessed)
                    # filepaths, task_ids, task_data = data
                    filepaths.append(capture_unprocessed.file_path)
                    task_ids.append(capture_unprocessed.task_id)

                print('[fcn_check] *** Working on ', task_ids, 'filepaths', filepaths, 'captures_unprocessed', captures_unprocessed)

                # print('[fcn_check] task_ids', task_ids, 'filepaths', filepaths)
                # Run detector core
                # to get report
                # and cukoo/virustotal result
                # task_ids, resp, scan_time = cf.detector.run(filepaths, task_ids)
                resp, scan_time = cf.detector.run(filepaths, task_ids)

                # start a thread for other detectors
                # t1 = threading.Thread(target=detector.run_han, args=(task_ids))
                # t1.start()
                # print('[fcn_check] resp', resp)
                # with concurrent.futures.ThreadPoolExecutor() as executor:
                #     future_han = executor.submit(detector.run_han, task_ids, resp)
                #     resp_all, scan_time = future_han.result()
                resp_all, scan_time = cf.detector.run_han(task_ids, resp)
                print('[check] *** HAN return ', resp_all, scan_time)

                # future_ngram = executor.submit(detector.run_ngram, filepaths, task_ids, resp_all)
                # resp_all, scan_time = future_ngram.result()
                # print('** NGRAM return ', resp_all, scan_time)

                links = []
                captures_data_new = []
                filenames = []
                i = 0
                for capture_unprocessed in captures_unprocessed:
                    tmp = {}
                    task_id = task_ids[i]
                    filepath = filepaths[i]
                    # filename = filenames[i]

                    filename = filepath.split('/')[-1]
                    res = resp_all[0][task_id]
                    engines_detected = resp_all[1][task_id]
                    detector_output = resp_all[2][task_id]
                    # print('res', res)
                    # if res['is_malware'] == 1:
                    # print('i=', i, tmp)
                    tmp['file_name'] = filename
                    tmp['file_size'] = os.path.getsize(filepath)
                    tmp['file_extension'] = filepath.split('.')[-1]
                    # tmp['file_path'] = filepath
                    tmp['report_path'] = res['report_path']
                    tmp['report_id'] = res['report_id']

                    tmp['hash'] = res['hash_value']
                    tmp['md5'] = res['md5']
                    tmp['sha1'] = res['sha1']
                    tmp['sha256'] = res['sha256']
                    tmp['sha512'] = res['sha512']
                    tmp['ssdeep'] = res['ssdeep']

                    # tmp['source_ip'] = request.remote_addr
                    tmp['detected_by'] = ','.join(engines_detected)
                    tmp['detector_output'] = json.dumps(
                        detector_output)
                    tmp['scan_time'] = scan_time

                    if 'date_received' not in tmp:
                        tmp['date_received'] = time.strftime('%Y-%m-%d')
                    if 'time_received' not in tmp:
                        tmp['time_received'] = time.strftime('%H:%M:%S')

                    if 'destination_ip' not in tmp:
                        tmp['destination_ip'] = ''

                    filenames.append(filename)
                    captures_data_new.append(tmp)
                    links.append(str(capture_unprocessed.capture_id))

                    # update database
                    # controllerCapture._parse_malware(data=tmp, capture_id=capture_unprocessed.capture_id)
                    # db.session.commit()
                    controllerCapture.update(object_id=capture_unprocessed.capture_id, data=tmp)

                    i += 1


                # cf.__tasks_done__.put((captures_data_new, captures_unprocessed))
                # cf.is_processing = False # done processing
                # cf.__tasks_to_run_detector__.task_done()

                cf.is_processing = False

                # add notification
                noti_data = {
                    'user_id': 2,
                    'message': 'Xử lý thành công các files {}. Xem chi tiết tại: <<{}>>'.format(', '.join(filenames), '|'.join(links))
                }
                controllerNoti.create(data=noti_data)

                print('[check] Process done. Sleep 10s')
                time.sleep(10)