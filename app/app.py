from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
# from app.dto import db

from app.settings.config import config_by_name

import app.settings.cf as cf
# import threading, queue
cf.detector = None
cf.set_detector = False
cf.is_running_detection = False
# cf.waiting_tasks = queue.Queue()
cf.waiting_tasks = None
cf.__tasks_process__ = None
cf.controllerCapture = None


# from app.modules.detector.detection_module import Detector
# # if not cf.set_detector:
# cf.set_detector = True
# cf.detector = Detector()


db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def init_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    return app
