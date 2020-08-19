import requests
import app.settings.cf as cf

REST_URL = cf.cuckoo_API+"/tasks/create/file"
SAMPLE_FILE = "/home/mtaav/CODE/mta-av-webservice/uploads/VirusShare_0a7684ed716f2bc360990115b781cc8f__trojan__PE__0.58"
HEADERS = {"Authorization": cf.cuckoo_SECRET_KEY}

with open(SAMPLE_FILE, "rb") as sample:
    files = {"file": sample}
    data = {"enforce_timeout": True, "timeout": 90}
    r = requests.post(REST_URL, headers=HEADERS, files=files, data=data)

# Add your code to error checking for r.status_code.

task_id = r.json()["task_id"]

# Add your code for error checking if task_id is None.