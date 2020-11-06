import app.settings.cf as cf
import os
import json
import time

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
    print('[check] **** CALL check')

    t_engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
    t_connection = t_engine.connect()
    
    cmd = "select * from capture where detected_by is null and file_path is not null and task_id is not null order by capture_id asc limit 0,{}".format(cf.process_batch_size)

    while True:
        # Process by batch.
        # Load a batch of {batch_size} files unprocessed in database
        if cf.is_processing:
            print('[check] Some task is processing. Sleep 10s then check again')
            time.sleep(30)
        else:
            print('[check] *** Load some tasks to process')
            # load unprocessed from database

            captures_unprocessed = t_connection.execute(cmd).fetchall()
            # print('[check] captures_unprocessed', captures_unprocessed)

            # if found unprocessed task
            # if captures_unprocessed_proxy is not None and len(captures_unprocessed_proxy) > 0:
            if captures_unprocessed is not None and len(captures_unprocessed) > 0:
                cf.is_processing = True # lock

                filepaths = []
                task_ids = []
                # print('[check] *** captures_unprocessed', captures_unprocessed)
                for capture_unprocessed in captures_unprocessed:
                    # print('[check] #', 'capture_unprocessed', capture_unprocessed)
                    filepaths.append(capture_unprocessed.file_path)
                    task_ids.append(capture_unprocessed.task_id)

                print('[fcn_check] *** Working on ', task_ids, 'filepaths', filepaths, 'captures_unprocessed', captures_unprocessed)

                # Run detector core
                # to get report
                # and cukoo/virustotal result
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

                links = []
                captures_data_new = []
                filenames = []
                i = 0
                for capture_unprocessed in captures_unprocessed:
                    tmp = {}
                    task_id = task_ids[i]
                    filepath = filepaths[i]

                    filename = filepath.split('/')[-1]
                    res = resp_all[0][task_id]
                    engines_detected = resp_all[1][task_id]
                    detector_output = resp_all[2][task_id]

                    update_el = []

                    update_el.append("{} = '{}'".format('file_name', filename))
                    update_el.append("{} = '{}'".format('file_extension', filepath.split('.')[-1]))
                    update_el.append("{} = '{}'".format('file_size', os.path.getsize(filepath)))
                    update_el.append("{} = '{}'".format('report_path', res['report_path']))
                    update_el.append("{} = '{}'".format('report_id', res['report_id']))
                    update_el.append("{} = '{}'".format('hash', res['hash_value']))
                    update_el.append("{} = '{}'".format('md5', res['md5']))
                    update_el.append("{} = '{}'".format('sha1', res['sha1']))
                    update_el.append("{} = '{}'".format('sha256', res['sha256']))
                    update_el.append("{} = '{}'".format('sha512', res['sha512']))
                    update_el.append("{} = '{}'".format('ssdeep', res['ssdeep']))

                    update_el.append("{} = '{}'".format('detected_by', ','.join(engines_detected)))
                    update_el.append("{} = '{}'".format('detector_output', json.dumps(
                        detector_output)))
                    update_el.append("{} = '{}'".format('scan_time', scan_time))

                    update_str = ', '.join(update_el)
                    cmd_update_capture = 'update capture set {} where capture_id = {}'.format(update_str, capture_unprocessed.capture_id)
                    t_connection.execute(cmd_update_capture)

                    filenames.append(filename)
                    captures_data_new.append(tmp)
                    links.append(str(capture_unprocessed.capture_id))

                    i += 1


                cf.is_processing = False

                # add notification
                msg = 'Xử lý thành công các files {}. Xem chi tiết tại: <<{}>>'.format(', '.join(filenames), '|'.join(links))
                cmd_add_noti = "insert into notification (user_id, message) values ({}, '{}')".format(2, msg)
                t_connection.execute(cmd_add_noti)


                print('[check] Process done. Sleep 30s')
                time.sleep(30)
