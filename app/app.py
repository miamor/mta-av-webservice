from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
# from app.dto import db

from app.settings.config import config_by_name
import app.settings.cf as cf
# from multiprocessing import Process, Queue
import threading, queue
from app.modules.malware.controller_capture import ControllerCapture

cf.controllerCapture = ControllerCapture()
cf.detector = None
cf.set_detector = False
# cf.is_running_detection = False
cf.waiting_tasks = queue.Queue()


db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def init_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    return app


cf.controllerCapture.check()