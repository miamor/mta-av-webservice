import os
import requests

host = '192.168.126.26'
port = 5002
hash_type = 'md5'
cuckoo_API = 'http://'+host+':1337'
cuckoo_SECRET_KEY = "Bearer RALTrRjHNT21MZdDCksugg"
cuckoo_timeout = 120

# REST_URL = cuckoo_API+"/tasks/create/file"
# HEADERS = {"Authorization": cuckoo_SECRET_KEY}

SUBMIT_URL = 'http://{}:{}/api/v1/capture/gen_report'.format(host, port)

BIN_ROOT = '../../MTAAV_data/bin/new_a_Dung'
count = 0

# for lbl in os.listdir(BIN_ROOT):
#     for filename in os.listdir(BIN_ROOT+'/'+lbl):
if True:
    for filename in os.listdir(BIN_ROOT+'/malware'):
        count += 1
        filepath = BIN_ROOT+'/malware/'+filename

        with open(filepath, "rb") as sample:
            # files = {"file": sample}
            # data = {"enforce_timeout": True, "timeout": cuckoo_timeout}
            # r = requests.post(REST_URL, headers=HEADERS, files=files, data=data)

            files = {"files[]": sample}
            r = requests.post(SUBMIT_URL, files=files)

            # Add your code to error checking for r.status_code.

            task_id = r.json()["task_id"]
            print(count, filepath, 'submitted. Task ', task_id)

            # Add your code for error checking if task_id is None.