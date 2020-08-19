from app.modules.common.controller import Controller
from ..malware.capture import Capture
from sqlalchemy import text
from app.app import db


class ControllerStat(Controller):
    
    def get(self):
        malwares_num = Capture.query.filter_by(detected_by='').count()
        print('malwares_num', malwares_num)
        return malwares_num
