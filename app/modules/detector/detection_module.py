import os
from werkzeug.utils import secure_filename
import time
from flask import jsonify
from ..detector.sandbox import Sandbox_API

import app.settings.cf as cf
import sys
# sys.path.insert(0, '')
sys.path.insert(0, cf.__ROOT__)
import han_sec_api as han

class Response(object):
    def __init__(self):
        self.resp = {}
        self.engines_detected = []
    
    def add_obj(self, task_id, filename, hash_value, report_path, ftype, fsize, md5, sha1, sha256, sha512, ssdeep):
        ''' Add detection result to response '''
        if task_id not in self.resp:
            print('add_obj: ~~~~ ', task_id, filename, hash_value, report_path, ftype, fsize, md5, sha1, sha256, sha512, ssdeep)

            self.resp[task_id] = {
                'filename' : filename,
                'hash_type' : cf.hash_type,
                'hash_value' : hash_value,
                
                'report_path': report_path,
                'report_id': task_id,
                'file_type': ftype,
                'file_size': fsize,
                
                'md5': md5,
                'sha1': sha1,
                'sha256': sha256,
                'sha512': sha512,
                'ssdeep': ssdeep,
            }
    
    def add_response(self, task_id, is_malware, score, engine, msg=''):
        ''' Add detection result to response '''
        if is_malware == 1:
            self.resp[task_id]['is_malware'] = 1

        self.resp[task_id][engine] = {
            'is_malware' : is_malware,
            'score' : score,
            'msg' : msg
        }

        if is_malware == 1 and engine not in self.engines_detected:
            self.engines_detected.append(engine)

    def get(self):
        return self.resp, self.engines_detected


class Detector(object):
    def __init__(self):
        return
    
    def run(self, filename, filepath):
        self.task_ids = []
        self.map_task_file = {}
        self.map_task_report = {}
        self.sandbox = Sandbox_API(cuckoo_API=cf.cuckoo_API, SECRET_KEY=cf.cuckoo_SECRET_KEY, hash_type=cf.hash_type)
        self.__res__ = Response()


        self.begin_time = time.time()

        ####################################################
        # 1. static detect
        ####################################################

        ####################################################
        # 2. run sandbox to get report
        ####################################################
        task_id, hash_value, report = self.run_sandbox(filepath)
        self.task_ids.append(task_id)
        self.map_task_file[task_id] = filepath
        # self.map_task_report[task_id] = report

        print("***** report", report)
        # print("***** report['target']['file']~~~~~~~~", report['target']['file'])
        report_path = report['target']['file']['path']
        ftype = report['target']['file']['type']
        md5 = report['target']['file']['md5']
        sha1 = report['target']['file']['sha1']
        sha256 = report['target']['file']['sha256']
        sha512 = report['target']['file']['sha512']
        ssdeep = report['target']['file']['ssdeep']
        fsize = report['target']['file']['size']

        self.__res__.add_obj(task_id, filename, hash_value, report_path, ftype, fsize, md5, sha1, sha256, sha512, ssdeep)

        ####################################################
        # 3. feed different dynamic detectors
        # -----------------
        # Each engine can return whatever format you want
        # For each engine, use this format to add its result to final response
        # __res__.add_response(task_id, engine__is_malware, engine__score, engine__name)
        #   engine__is_malware  (int):      1:malware|0:benign
        #   engine__score       (float):    confidence/score/...
        #   engine__name        (string):   name of the engine
        ####################################################

        # cuckoo virustotal detector
        obj_res = self.cuckoo_virustotal_detect(report)
        for engine_name in obj_res:
            engine_res = obj_res[engine_name]
            # for each engine, use this format to add its result to final response
            self.__res__.add_response(task_id, engine_res['is_malware'], engine_res['score'], engine_name, engine_res['msg'])

        # HAN detector
        task_ids = [task_id]
        labels, scores, msg = self.HAN_detect(task_ids)
        # for i, task_id in enumerate(task_ids):
        #     self.__res__.add_response(task_id, labels[i], scores[i], 'HAN_sec')
        self.__res__.add_response(task_id, labels[0], scores[0], 'HAN_sec')

        scan_time = time.time()-self.begin_time
        print('time', scan_time)

        return task_id, self.__res__.get(), scan_time


    def static_detector(self, filepath):
        return
    
    def run_sandbox(self, filepath):
        done_report = False

        # Run analysis
        task_id = self.sandbox.start_analysis(filepath)
        # print("task_id", task_id)

        if task_id is None:
            return jsonify(
                {"status": "error", "status_msg": "Create task for file {} failed.".format(filepath)}
            )

        # Now wait until task is complete
        # Keep checking status
        while not done_report:
            task_status, errors, hash_value = self.sandbox.get_task_status(task_id)
            # print('errors', errors)
            print('#', task_id, 'task_status', task_status, 'errors', errors)
            if task_status == 'reported':
                done_report = True
                # if errors is not None:
                #     return jsonify(
                #         {"status": "error", "status_msg": "Error analyzing.\n"+'\n'.join(errors)}
                #     )
            time.sleep(10)


        # Analyzing done. Now get report and feed to different malware detectors
        report = self.sandbox.get_report(task_id)

        return task_id, hash_value, report


    def cuckoo_virustotal_detect(self, task):
        task_info = task["info"]

        # print('task', task)
        # print("task_info['score']=", task_info['score'])
        # return task_info['score'], task['virustotal']['scans']
        virustotal_res = {
            'is_malware': 0,
            'score': 0,
            'msg': ''
        }
        virustotal_detected = 0
        virustotal_tot_engine = 0
        # print('task', task)
        if 'scans' in task['virustotal']:
            for engine_name in task['virustotal']['scans']:
                engine_res = task['virustotal']['scans'][engine_name]
                print('engine_res', engine_res)
                virustotal_tot_engine += 1
                if engine_res['detected'] is True:
                    virustotal_detected += 1
        if virustotal_tot_engine > 0:
            virustotal_res['score'] = virustotal_detected / virustotal_tot_engine
            virustotal_res['msg'] = '{}/{} engines detected as malware'.format(virustotal_detected, virustotal_tot_engine)
            if virustotal_res['score'] > 0.4:
                virustotal_res['is_malware'] = 1
        else:
            virustotal_res['msg'] = 'No virustotal scans found'

        cuckoo_res = {
            'is_malware': int(task_info['score'] > 0),
            'score': task_info['score'],
            'msg': ''
        }

        return {
            'cuckoo': cuckoo_res,
            'virustotal': virustotal_res
        }


    def HAN_detect(self, task_ids):
        num_task = len(task_ids)
        # data, args = prepare_files([9])
        data, args = han.prepare_files(task_ids, cuda=False)
        print('*** data', data)
        if data is None:
            print('Graph can\'t be created!')
            return [0]*num_task, [0]*num_task, ['Graph can\'t be created!']*num_task
        else:
            print('task_ids', task_ids)
            print('len data', len(data))
            labels, scores = han.predict_files(data, args, cuda=False)
            labels = labels.cpu().numpy().tolist()
            scores = scores.cpu().numpy().tolist()
            print('labels, scores', labels, scores)
            return labels, scores, None
        
        return None, None, None

