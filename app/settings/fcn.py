import app.settings.cf as cf
import os
import json
import time

from app.modules.common.controller import Controller
from app.modules.malware.capture import Capture
# from sqlalchemy import text
from app.app import db
from app.settings.config import Config

from app.modules.detector.detection_module import Detector
if not cf.set_detector:
    cf.set_detector = True
    cf.detector = Detector()

from app.modules.detector.sandbox import Sandbox_API
cf.sandbox = Sandbox_API(cuckoo_API=cf.cuckoo_API, SECRET_KEY=cf.cuckoo_SECRET_KEY, hash_type=cf.hash_type, timeout=cf.cuckoo_timeout)


def insert_db_unprocessed(self):
        print('\n*** CALL insert_db_unprocessed ')
        while not cf.__tasks_to_process__.empty():
            filepaths, task_ids, task_data = cf.__tasks_to_process__.get()

            filenames = []
            for i in range(len(task_data)):
                task_data[i]['task_id'] = task_ids[i]
                controller = ControllerCapture()
                malware = controller.create(data=task_data[i])
                print('**** malware inserted', i, malware)
        return result(message='Insert completed')



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


def check():
        print('[fcn_check] **** CALL fcn_check')
        # while not cf.__tasks_to_process__.empty():
        #     filepaths, task_ids, task_data = cf.__tasks_to_process__.get()

        # load unprocessed from database
        cmd = "select * from capture where detected_by is null"
        engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
        connection = engine.connect()
        captures_unprocessed = connection.execute(cmd).fetchall()


            # filepaths, task_ids, task_data = data
            print('[fcn_check] *** Working on {}'.format(task_ids), 'filepaths', filepaths)

            # print('[fcn_check] task_ids', task_ids, 'filepaths', filepaths)
            # Run detector core
            # to get report
            # and cukoo/virustotal result
            task_ids, resp, scan_time = cf.detector.run(filepaths, task_ids)

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

            # future_img_bytes = executor.submit(detector.run_img_bytes, filepaths, task_ids, resp_all)
            # resp_all, scan_time = future_img_bytes.result()
            # print('** img_bytes return ', resp_all, scan_time)

            # future_asm = executor.submit(detector.run_asm, filepaths, task_ids, resp_all)
            # resp_all, scan_time = future_asm.result()
            # print('** asm return ', resp_all, scan_time)

            report_ids = []
            for i in range(len(task_data)):
                # filepath = task_data[i]['file_path']
                # task_id = task_data[i]['task_id']

                task_id = task_ids[i]
                filepath = filepaths[i]
                # filename = filenames[i]

                filename = filepath.split('/')[-1]
                res = resp_all[0][task_id]
                engines_detected = resp_all[1][task_id]
                detector_output = resp_all[2][task_id]
                # print('res', res)
                # if res['is_malware'] == 1:
                # print('i=', i, task_data[i])
                task_data[i]['file_name'] = filename
                task_data[i]['file_size'] = os.path.getsize(filepath)
                task_data[i]['file_extension'] = filepath.split('.')[-1]
                # task_data[i]['file_path'] = filepath
                task_data[i]['report_path'] = res['report_path']
                task_data[i]['report_id'] = res['report_id']

                task_data[i]['hash'] = res['hash_value']
                task_data[i]['md5'] = res['md5']
                task_data[i]['sha1'] = res['sha1']
                task_data[i]['sha256'] = res['sha256']
                task_data[i]['sha512'] = res['sha512']
                task_data[i]['ssdeep'] = res['ssdeep']

                # task_data[i]['source_ip'] = request.remote_addr
                task_data[i]['detected_by'] = ','.join(engines_detected)
                task_data[i]['detector_output'] = json.dumps(
                    detector_output)
                task_data[i]['scan_time'] = scan_time

                if 'date_received' not in task_data[i]:
                    task_data[i]['date_received'] = time.strftime('%Y-%m-%d')
                if 'time_received' not in task_data[i]:
                    task_data[i]['time_received'] = time.strftime('%H:%M:%S')

                if 'destination_ip' not in task_data[i]:
                    task_data[i]['destination_ip'] = ''

                # print('**** data insert: ', task_data[i])
                # controller = ControllerCapture()
                # malware = controller.create(data=task_data[i])
                # print('**** malware inserted', i, malware)

                # # get inserted row
                # row = controller.get_by_rpid(rp_id=res['report_id'])
                # links.append(row.capture_id)
                report_ids.append(res['report_id'])

            # print('resp_all[0]', resp_all[0])
            # cf.is_running_detection = False

            cf.__tasks_done__.put((task_ids, task_data, report_ids))
            cf.__tasks_to_process__.task_done()

            # # add notification
            # noti_data = {
            #     'user_id': 2,
            #     'message': 'Xử lý thành công các tác vụ {}. Xem chi tiết tại: <<{}>>'.format(', '.join(task_ids), '|'.join(links))
            # }
            # controllerNoti = ControllerNoti()
            # controllerNoti.create(data=noti_data)

            # return result(message='Check completed', data=resp_all[0])
            # return task_data

        # print('resp', resp)
        # return result(message='Check completed. File clean!')


