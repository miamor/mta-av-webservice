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

def check():
    print('[fcn_check] **** CALL fcn_check')

    # Process by batch.
    # Load a batch of 10 files unprocessed in database

    # while not cf.is_processing:
    if True:
        # cf.__pool_run_cuckoo__ = Pool(1)

        # load unprocessed from database
        cmd = "select * from capture where detected_by is null order by capture_id asc limit 0,{}".format(
            cf.process_batch_size)

        captures_unprocessed = cf.connection.execute(cmd).fetchall()

        # found unprocessed task
        if captures_unprocessed is not None and len(captures_unprocessed) > 0:
            cf.is_processing = True # Lock

            filepaths = []
            task_ids = []
            for capture_unprocessed in captures_unprocessed:
                # filepaths, task_ids, task_data = data
                filepaths.append(capture_unprocessed.file_path)
                task_ids.append(capture_unprocessed.task_id)

            print('[fcn_check] *** Working on {}'.format(task_ids),
                'filepaths', filepaths)

            # print('[fcn_check] task_ids', task_ids, 'filepaths', filepaths)
            # Run detector core
            # to get report
            # and cukoo/virustotal result
            # task_ids, resp, scan_time = cf.detector.run(filepaths, task_ids)
            # Run in pool
            # resp = cf.__pool_run_cuckoo__.map(cf.detector.run, task_ids)
            resp = []
            for task_id in task_ids:
                resp.append(cf.detector.run(task_id))
            print('[fcn_check] ** __pool_run_cuckoo__ return ', resp)

            # start a thread for other detectors
            # t1 = threading.Thread(target=detector.run_han, args=(task_ids))
            # t1.start()
            # print('[fcn_check] resp', resp)
            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     future_han = executor.submit(detector.run_han, task_ids, resp)
            #     resp_all, scan_time = future_han.result()
            resp_all, scan_time = cf.detector.run_han(task_ids, resp)
            print('[fcn_check] ** HAN return ', resp_all, scan_time)

            # future_ngram = executor.submit(detector.run_ngram, filepaths, task_ids, resp_all)
            # resp_all, scan_time = future_ngram.result()
            # print('** NGRAM return ', resp_all, scan_time)

            report_ids = []
            links = []
            # controllerCapture = ControllerCapture()
            for i in range(len(captures_unprocessed)):
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

                report_ids.append(res['report_id'])

                # update database
                # controllerCapture._parse_malware(data=tmp, malware=captures_unprocessed[i])
                # db.session.commit()

                # links.append(str(captures_unprocessed[i].capture_id))


            # cf.__pool_run_cuckoo__.close()
            # cf.__pool_run_cuckoo__.join()
            # cf.is_processing = False

            # # print('resp_all[0]', resp_all[0])
            # # cf.is_running_detection = False

            # # cf.__tasks_to_process__.task_done()

            # # add notification
            # noti_data = {
            #     'user_id': 2,
            #     'message': 'Xử lý thành công các tác vụ {}. Xem chi tiết tại: <<{}>>'.format(', '.join(task_ids), '|'.join(links))
            # }
            # controllerNoti = ControllerNoti()
            # controllerNoti.create(data=noti_data)


            time.sleep(1.0)

            # return result(message='Check completed', data=resp_all[0])
            # return task_data

            # print('resp', resp)
            # return result(message='Check completed. File clean!')
