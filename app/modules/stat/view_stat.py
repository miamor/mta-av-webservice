from flask_restplus import Resource
from app.modules.common.decorator import token_required, admin_token_required
from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
import app.settings.cf as cf
# from werkzeug.datastructures import FileStorage
from ..detector.detection_module import Detector
from app.utils.response import error, result
from flask_restplus import marshal
import time
from .dto_stat import DtoStat
from .controller_stat import ControllerStat
api = DtoStat.api


@api.route('')
class StatDashboard(Resource):
    def get(self):
        controller = ControllerStat()
        return controller.get()
