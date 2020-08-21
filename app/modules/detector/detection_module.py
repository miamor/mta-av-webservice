import os
from werkzeug.utils import secure_filename
import time
from flask import jsonify
from ..detector.sandbox import Sandbox_API

import app.settings.cf as cf
import sys
# sys.path.insert(0, '')
sys.path.insert(1, cf.__HAN_ROOT__)
# import han_sec_api as han
from han_sec_api import HAN_module
sys.path.insert(2, cf.__NGRAM_ROOT__)
# import ngram_api as ngram
from ngram_api import NGRAM_module

class Response(object):
    def __init__(self, res_obj=None):
        if res_obj is not None:
            self.resp = res_obj[0]
            self.engines_detected = res_obj[1]
        else:
            self.resp = {}
            self.engines_detected = {}
    
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
        if task_id not in self.engines_detected:
            self.engines_detected[task_id] = []
    
    def add_response(self, task_id, is_malware, score, engine, msg=''):
        ''' Add detection result to response '''
        if is_malware == 1:
            self.resp[task_id]['is_malware'] = 1

        self.resp[task_id][engine] = {
            'is_malware' : is_malware,
            'score' : score,
            'msg' : msg
        }

        if is_malware == 1 and engine not in self.engines_detected[task_id]:
            self.engines_detected[task_id].append(engine)

    def get(self):
        return self.resp, self.engines_detected


class Detector(object):
    def __init__(self):
        return
    
    def run(self, filenames, filepaths):
        self.sandbox = Sandbox_API(cuckoo_API=cf.cuckoo_API, SECRET_KEY=cf.cuckoo_SECRET_KEY, hash_type=cf.hash_type, timeout=cf.cuckoo_timeout)
        self.__res__ = Response()


        self.begin_time = time.time()

        ####################################################
        # 1. static detect
        ####################################################



        ####################################################
        # 2. run sandbox to get report
        ####################################################
        task_ids, hash_values, reports = self.run_sandbox(filepaths)

        k = 0
        for task_id in task_ids:
            filename = filenames[k]
            hash_value = hash_values[task_id]
            k += 1

            # print("***** report[task_id]", task_id, reports[task_id])
            # print("***** reports[task_id]['target']['file']~~~~~~~~", reports[task_id]['target']['file'])
            report_path = reports[task_id]['target']['file']['path']
            ftype = reports[task_id]['target']['file']['type']
            md5 = reports[task_id]['target']['file']['md5']
            sha1 = reports[task_id]['target']['file']['sha1']
            sha256 = reports[task_id]['target']['file']['sha256']
            sha512 = reports[task_id]['target']['file']['sha512']
            ssdeep = reports[task_id]['target']['file']['ssdeep']
            fsize = reports[task_id]['target']['file']['size']

            self.__res__.add_obj(task_id, filename, hash_value, report_path, ftype, fsize, md5, sha1, sha256, sha512, ssdeep)


            ####################################################
            # 3. feed different dynamic detectors (cuckoo & virus total)
            # -----------------
            # Each engine can return whatever format you want
            # For each engine, use this format to add its result to final response
            # __res__.add_response(task_id, engine__is_malware, engine__score, engine__name)
            #   engine__is_malware  (int):      1:malware|0:benign
            #   engine__score       (float):    confidence/score/...
            #   engine__name        (string):   name of the engine
            ####################################################

            # cuckoo virustotal detector
            obj_res = self.cuckoo_virustotal_detect(reports[task_id])
            for engine_name in obj_res:
                engine_res = obj_res[engine_name]
                # for each engine, use this format to add its result to final response
                self.__res__.add_response(task_id, engine_res['is_malware'], engine_res['score'], engine_name, engine_res['msg'])

        scan_time = time.time()-self.begin_time
        print('time', scan_time)

        return task_ids, self.__res__.get(), scan_time


    def run_han(self, task_ids, res_obj):
        ####################################################
        # 3. feed different dynamic detectors (HAN)
        # -----------------
        # Each engine can return whatever format you want
        # For each engine, use this format to add its result to final response
        # __res__.add_response(task_id, engine__is_malware, engine__score, engine__name)
        #   engine__is_malware  (int):      1:malware|0:benign
        #   engine__score       (float):    confidence/score/...
        #   engine__name        (string):   name of the engine
        ####################################################
        self.han = HAN_module(task_ids)

        self.__res__ = Response(res_obj)
        print('~~~~~ run_han', self.__res__.get())

        self.begin_time = time.time()

        # task_ids = [task_id]
        labels, scores, msg = self.HAN_detect(task_ids)
        for i, task_id in enumerate(task_ids):
            self.__res__.add_response(task_id, labels[i], scores[i], 'HAN_sec')
        # self.__res__.add_response(task_id, labels[0], scores[0], 'HAN_sec')

        scan_time = time.time()-self.begin_time
        print('HAN time', scan_time)

        return self.__res__.get(), scan_time


    def run_ngram(self, file_paths, task_ids, res_obj):
        ####################################################
        # 3. feed different dynamic detectors (ngram)
        # -----------------
        # Each engine can return whatever format you want
        # For each engine, use this format to add its result to final response
        # __res__.add_response(task_id, engine__is_malware, engine__score, engine__name)
        #   engine__is_malware  (int):      1:malware|0:benign
        #   engine__score       (float):    confidence/score/...
        #   engine__name        (string):   name of the engine
        ####################################################
        self.ngram = NGRAM_module()

        self.__res__ = Response(res_obj)

        self.begin_time = time.time()

        # task_ids = [task_id]
        labels, scores, msg = self.HAN_detect(task_ids)
        for i, task_id in enumerate(task_ids):
            self.__res__.add_response(task_id, labels[i], scores[i], 'HAN_sec')
        # self.__res__.add_response(task_id, labels[0], scores[0], 'HAN_sec')

        #### n-gram detector 
        df = self.ngram.creator(file_paths, cf.N_GRAM_SIZE, len(file_paths), cf.FREQ_FILE)
        self.ngram.infer(df)

        scan_time = time.time()-self.begin_time
        print('HAN time', scan_time)

        return self.__res__.get(), scan_time



    def static_detector(self, filepath):
        return
    
    def run_sandbox(self, filepaths):
        done_report = []
        total_tasks = len(filepaths)
        task_ids = []
        hash_values = {}

        # Run analysis
        for filepath in filepaths:
            task_id = self.sandbox.start_analysis(filepath)
            # print("task_id", task_id)

            if task_id is None:
                return jsonify({"status": "error", "status_msg": "Create task for file {} failed.".format(filepath)})
            
            task_ids.append(task_id)

        # Now wait until task is complete
        # Keep checking status
        while len(done_report) < total_tasks:
            for task_id in task_ids:
                if task_id not in done_report:
                    task_status, errors, hash_value = self.sandbox.get_task_status(task_id)
                    # print('errors', errors)
                    print('#', task_id, 'task_status', task_status, 'errors', errors)
                    if task_status == 'reported':
                        hash_values[task_id] = hash_value
                        done_report.append(task_id)
                        # if errors is not None:
                        #     return jsonify(
                        #         {"status": "error", "status_msg": "Error analyzing.\n"+'\n'.join(errors)}
                        #     )
            time.sleep(10)


        # Analyzing done. Now get report and feed to different malware detectors
        reports = {task_id: self.sandbox.get_report(task_id) for task_id in task_ids}

        return task_ids, hash_values, reports


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
                # print('engine_res', engine_res)
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
        data = self.han.prepare_files(task_ids, cuda=False)
        print('*** data', data)
        if data is None:
            print('Graph can\'t be created!')
            return [0]*num_task, [0]*num_task, ['Graph can\'t be created!']*num_task
        else:
            print('task_ids', task_ids)
            print('len data', len(data))
            labels, scores = self.han.predict_files(data, cuda=False)
            labels = labels.cpu().numpy().tolist()
            scores = scores.cpu().numpy().tolist()
            print('labels, scores', labels, scores)
            return labels, scores, None
        
        return None, None, None

