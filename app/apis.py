from flask_restplus import Api
from app.modules import ns_user, ns_auth, ns_capture, ns_history, ns_url, ns_noti
import app.settings.cf as cf
import app.settings.fcn as fcn
# from app.modules.malware.controller_capture import ControllerCapture
# from app.modules.notification.controller_noti import ControllerNoti

from multiprocessing import Process, Queue, Pool
import threading, queue



# cf.controllerCapture = ControllerCapture()
# cf.controllerNoti = ControllerNoti()

# cf.__tasks_to_run_detector__ = queue.Queue()
# cf.__tasks_done__ = queue.Queue()


# cf.__tasks_process__ = threading.Thread(target=fcn.fcn_check, args=(cf.detector,))
# cf.__tasks_process__.start()
# cf.__submit_cuckoo_thread__ = insert_db_unprocessed


# def process_task():
#     threading.Thread(target=cf.controllerCapture.check, daemon=True).start()

# cf.__tasks_process__ = Process(target=fcn.check)
# cf.__tasks_process__.start()

t = threading.Thread(target=fcn.check)
t.start()

# t.join()

def init_api():
    api = Api(title='mtaSMaD APIs',
              version='1.0',
              description='mtaAV Web API')
    api.add_namespace(ns_user, path='/api/v1/user')
    api.add_namespace(ns_auth, path='/api/v1/auth')
    api.add_namespace(ns_capture, path='/api/v1/capture')
    api.add_namespace(ns_history, path='/api/v1/history')
    api.add_namespace(ns_url, path='/api/v1/url')
    api.add_namespace(ns_noti, path='/api/v1/noti')
    return api


# cf.__tasks_process__.join()
