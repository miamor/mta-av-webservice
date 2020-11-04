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
sys.path.insert(3, cf.__IMG_BYTES_API_ROOT__)
from api_img_bytes import CNN_Img_Module
sys.path.insert(4, cf.__ASM_API_ROOT__)
from api_asm import Asm_Module

class Response(object):
    def __init__(self, res_obj=None):
        if res_obj is not None:
            self.res = res_obj[0]
            self.engines_detected = res_obj[1]
            self.detector_output = res_obj[2]
        else:
            self.res = {}
            self.engines_detected = {}
            self.detector_output = {}
    
    def add_obj(self, task_id, filename, hash_value, report_path, ftype, fsize, md5, sha1, sha256, sha512, ssdeep):
        ''' Add detection result to response '''
        if task_id not in self.res:
            print('add_obj: ~~~~ ', task_id, filename, hash_value, report_path, ftype, fsize, md5, sha1, sha256, sha512, ssdeep)

            self.res[task_id] = {
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

                'is_malware': 0,
            }
        if task_id not in self.engines_detected:
            self.engines_detected[task_id] = []
        if task_id not in self.detector_output:
            self.detector_output[task_id] = {}
    
    def add_response(self, task_id, is_malware, score, engine, scan_time, msg=''):
        ''' Add detection result to response '''
        if is_malware == 1:
            self.res[task_id]['is_malware'] = 1

        # self.res[task_id][engine] = {
        #     'is_malware' : is_malware,
        #     'score' : score,
        #     'msg' : msg
        # }
        self.detector_output[task_id][engine] = {
            'is_malware' : is_malware,
            'score' : score,
            'scan_time': scan_time,
            'msg' : msg
        }

        if is_malware == 1 and engine not in self.engines_detected[task_id]:
            self.engines_detected[task_id].append(engine)

    def get(self):
        return self.res, self.engines_detected, self.detector_output


class Detector(object):
    def __init__(self):
        self.han = None
        # self.ngram = NGRAM_module(model_path=cf.NGRAM_MODEL_PATH)
        # self.img_bytes_module = CNN_Img_Module(img_model_path=cf.__IMG_BYTES_API_ROOT__+'/code_img/models/rgb.h5', cnn_bytes_model_path=cf.__IMG_BYTES_API_ROOT__+'/code_bytes/output/cnn_best__7500_1259.h5', lstm_bytes_model_path=cf.__IMG_BYTES_API_ROOT__+'/code_bytes/output/lstm_best__7240_1259.h5')
        # self.asm_module = Asm_Module(cnn_model_path=cf.__ASM_API_ROOT__+'/output/cnn_best__9635_1778.h5', lstm_model_path=cf.__ASM_API_ROOT__+'/output/lstm_best__9427_1926.h5')

        self.sandbox = Sandbox_API(cuckoo_API=cf.cuckoo_API, SECRET_KEY=cf.cuckoo_SECRET_KEY, hash_type=cf.hash_type, timeout=cf.cuckoo_timeout)

        return


    def run(self, filepaths, task_ids):
        self.__res__ = Response()

        done_report = []
        hash_values = {}

        self.begin_time = time.time()

        ####################################################
        # 1. static detect
        ####################################################



        ####################################################
        # 2. get report from task_id
        ####################################################
        # task_ids, hash_values, reports = self.run_sandbox_and_wait(filepaths)

        while len(done_report) < len(task_ids):
            for task_id in task_ids:
                if task_id not in done_report:
                    task_status, errors, hash_value = self.sandbox.get_task_status(task_id)
                    # print('errors', errors)
                    print('#', task_id, 'task_status', task_status, 'errors', errors)
                    if task_status == 'reported':
                        hash_values[task_id] = hash_value
                        done_report.append(task_id)
            time.sleep(30)


        k = 0
        for task_id in task_ids:
            filename = filepaths[k].split('/')[-1]
            # filename = filenames[k]
            report = self.sandbox.get_report(task_id)
            # hash_value = report['sample'][cf.hash_type]
            hash_value = hash_values[task_id]

            # hash_value = hash_values[task_id]
            k += 1

            # print("***** report[task_id]", task_id, report)
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
            # 3. feed different dynamic detectors (cuckoo & virus total)
            # -----------------
            # Each engine can return whatever format you want
            # For each engine, use this format to add its result to final response
            # __res__.add_response(task_id, engine__is_malware, engine__score, engine__name, engine__scan_time, engine__msg)
            #   engine__is_malware  (int):      1:malware|0:benign
            #   engine__score       (float):    confidence/score/...
            #   engine__name        (string):   name of the engine
            ####################################################

            # cuckoo virustotal detector
            obj_res = self.cuckoo_virustotal_detect(report)
            for engine_name in obj_res:
                engine_res = obj_res[engine_name]
                # for each engine, use this format to add its result to final response
                self.__res__.add_response(task_id, engine_res['is_malware'], engine_res['score'], engine_name, time.time()-self.begin_time, engine_res['msg'])

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
        print('* [run_han]', res_obj)

        self.begin_time = time.time()
        
        # task_ids = [task_id]
        labels, scores, msg = self.HAN_detect(task_ids)
        for i, task_id in enumerate(task_ids):
            # A little trick to decrease far
            if labels[i] == 1:
                if res_obj[2][task_id]['cuckoo']['score'] < 3:
                    labels[i] = 0
                    scores[i] = 0-scores[i]
            # if res_obj[2][task_id]['cuckoo']['is_malware'] == 1 and labels[i] == 0:
            #     labels[i] = 1
            #     scores[i] = 0-scores[i]
            # elif scores[i] < 0.75 and labels[i] == 1:
            #     labels[i] = 0
            #     scores[i] = 1 - scores[i]
            # labels[i] = res_obj[2][task_id]['cuckoo']['is_malware']

            # elif res_obj[2][task_id]['virustotal']['is_malware'] == 0:
            #     labels[i] = 0
            #     scores[i] = 0 - scores[i]
            # elif res_obj[2][task_id]['virustotal']['is_malware'] == 1 and labels[i] == 0:
            #     labels[i] = 1
            #     scores[i] = 0 - scores[i]

            self.__res__.add_response(task_id, labels[i], scores[i], 'HAN_sec', time.time()-self.begin_time)
        # self.__res__.add_response(task_id, labels[0], scores[0], 'HAN_sec')

        scan_time = time.time()-self.begin_time
        print('[run_han] HAN time', scan_time)

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
        print('* [run_ngram]', file_paths, res_obj)
        self.__res__ = Response(res_obj)

        self.begin_time = time.time()

        #### n-gram detector 
        df = self.ngram.creator(file_paths, cf.N_GRAM_SIZE, len(file_paths), cf.FREQ_FILE)
        labels = [int(val) for val in self.ngram.infer(df)]

        for i, task_id in enumerate(task_ids):
            self.__res__.add_response(task_id, labels[i], 0, 'ngram', time.time()-self.begin_time)

        scan_time = time.time()-self.begin_time
        print('[run_ngram] NGRAM time', scan_time)

        return self.__res__.get(), scan_time


    def run_img_bytes(self, file_paths, task_ids, res_obj):
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
        print('* [run_img_bytes]', file_paths, res_obj)
        self.__res__ = Response(res_obj)

        self.begin_time = time.time()

        #### cnn img, cnn bytes, lstm bytes detector 
        module_res = self.img_bytes_module.from_files(file_paths, task_ids=task_ids, output_directory=cf.__IMG_BYTES_API_ROOT__+'/api_tasks/__prepared_RGB')

        for engine in module_res:
            labels, scores = module_res[engine]
            labels = labels.tolist()
            scores = scores.tolist()

            for i, task_id in enumerate(task_ids):
                self.__res__.add_response(task_id, labels[i], scores[i], engine, time.time()-self.begin_time)

        scan_time = time.time()-self.begin_time
        print('[run_img_bytes] CNN_img_bytes time', scan_time)

        return self.__res__.get(), scan_time



    def run_asm(self, file_paths, task_ids, res_obj):
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
        print('* [run_asm]', file_paths, res_obj)
        self.__res__ = Response(res_obj)

        self.begin_time = time.time()

        #### cnn, lstm asm detector 
        module_res = self.asm_module.from_files(file_paths, task_ids=task_ids)

        for engine in module_res:
            labels, scores = module_res[engine]
            labels = labels.tolist()
            scores = scores.tolist()

            for i, task_id in enumerate(task_ids):
                self.__res__.add_response(task_id, labels[i], scores[i], engine, time.time()-self.begin_time)

        scan_time = time.time()-self.begin_time
        print('[run_asm] CNN_asm, LSTM_asm time', scan_time)

        return self.__res__.get(), scan_time


    def static_detector(self, filepath):
        return
    
    def run_sandbox(self, filepath):
        return self.sandbox.start_analysis(filepath)
    
    def run_sandbox_and_wait(self, filepaths):
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
        print('[cuckoo_virustotal_detect] task', task)
        if 'virustotal' in task:
            virustotal_detected = 0
            virustotal_tot_engine = 0
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
            'is_malware': int(task_info['score'] >= 3.5),
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
        # data = self.han.prepare_files(task_ids, cuda=False)
        data = self.han.prepare_files(cuda=False)
        print('*** data', data)
        if data is None:
            print('Graph can\'t be created!')
            return [0]*num_task, [0]*num_task, ['Graph can\'t be created!']*num_task
        else:
            print('task_ids', task_ids)
            # print('len data', len(data))
            labels, scores = self.han.predict_files(data, cuda=False)
            labels = labels.cpu().numpy().tolist()
            scores = scores.cpu().numpy().tolist()
            print('labels, scores', labels, scores)

            return labels, scores, None
        
        return None, None, None



    
    def run_(self, filenames, filepaths):
        self.sandbox = Sandbox_API(cuckoo_API=cf.cuckoo_API, SECRET_KEY=cf.cuckoo_SECRET_KEY, hash_type=cf.hash_type, timeout=cf.cuckoo_timeout)
        
        # Run analysis
        for filepath in filepaths:
            task_id = self.sandbox.start_analysis(filepath)
            # print("task_id", task_id)

            if task_id is None:
                return jsonify({"status": "error", "status_msg": "Create task for file {} failed.".format(filepath)})
            else:
                return jsonify({"status": "success", "status_msg": "Created task for file {}. {}".format(filepath, task_id)})
