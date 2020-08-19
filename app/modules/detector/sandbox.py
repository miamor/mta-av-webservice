import requests

class Sandbox_API(object):

    def __init__(self, cuckoo_API, SECRET_KEY, hash_type):
        self.hash_type = hash_type
        self.cuckoo_API = cuckoo_API
        self.SECRET_KEY = SECRET_KEY
        return

    def start_analysis(self, filepath):
        REST_URL = self.cuckoo_API+"/tasks/create/file"
        HEADERS = {"Authorization": self.SECRET_KEY}

        with open(filepath, "rb") as sample:
            files = {"file": ("temp_file_name", sample)}
            r = requests.post(REST_URL, headers=HEADERS, files=files)

        # Add your code to error checking for r.status_code.
        task_id = r.json()["task_id"]

        # Add your code for error checking if task_id is None.

        return task_id


    def get_task_status(self, task_id):
        REST_URL = self.cuckoo_API+"/tasks/view/{}".format(task_id)
        HEADERS = {"Authorization": self.SECRET_KEY}

        r = requests.get(REST_URL, headers=HEADERS)

        task = r.json()["task"]
        print('task', task)

        if 'errors' in task:
            return task['status'], task['errors'], task['sample'][self.hash_type]
        
        return None, None, None


    def get_report(self, task_id):
        REST_URL = self.cuckoo_API+"/tasks/report/{}".format(task_id)
        HEADERS = {"Authorization": self.SECRET_KEY}

        r = requests.get(REST_URL, headers=HEADERS)

        task = r.json()

        return task