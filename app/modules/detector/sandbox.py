import requests

class Sandbox_API(object):

    def __init__(self, cuckoo_API, SECRET_KEY, hash_type, timeout):
        self.hash_type = hash_type
        self.cuckoo_API = cuckoo_API
        self.SECRET_KEY = SECRET_KEY
        self.timeout = timeout
        return

    def start_analysis(self, filepath):
        REST_URL = self.cuckoo_API+"/tasks/create/file"
        HEADERS = {"Authorization": self.SECRET_KEY}

        print('Submiting '+filepath+' to cuckoo')
        with open(filepath, "rb") as sample:
            # files = {"file": ("temp_file_name", sample)}
            files = {"file": sample}
            data = {"enforce_timeout": True, "timeout": self.timeout}
            r = requests.post(REST_URL, headers=HEADERS, files=files, data=data)

        # Add your code to error checking for r.status_code.
        task_id = r.json()["task_id"]
        print('** Created task for CUckoo: ', task_id)

        # Add your code for error checking if task_id is None.

        return task_id


    def get_task_status(self, task_id):
        REST_URL = self.cuckoo_API+"/tasks/view/{}".format(task_id)
        HEADERS = {"Authorization": self.SECRET_KEY}

        r = requests.get(REST_URL, headers=HEADERS)

        task = r.json()["task"]
        # print('task', task)

        if 'errors' in task:
            return task['status'], task['errors'], task['sample'][self.hash_type]
        
        return None, None, None


    def get_report(self, task_id):
        REST_URL = self.cuckoo_API+"/tasks/report/{}".format(task_id)
        HEADERS = {"Authorization": self.SECRET_KEY}

        r = requests.get(REST_URL, headers=HEADERS)

        task = r.json()

        return task