from app.modules.common.controller import Controller
from .noti import Noti
from app.app import db
from app.settings.config import Config
import datetime
import app.settings.cf as cf
from flask_restplus import marshal
# from app.utils.response import error, result

# import sys
# sys.path.insert(1, cf.__URLCHECKER_ROOT__)
# import classifier as noticlassifier

# engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
# connection = engine.connect()


class ControllerNoti(Controller):
    def create(self, data):
        data['date_created'] = datetime.datetime.now()
        noti = self._parse_noti(data=data, noti=None)
        db.session.add(noti)
        db.session.commit()
        return noti

    def get_query(self, filters=None):
        cond_str = ''

        # cond = []

        # if filters is not None:
        #     for key in filters:
        #         if key not in ['types', 'mode', 'p', 'page']:
        #             print(key, filters[key])
        #             cond.append("{} = '{}'".format(key, filters[key]))

        # if 'destination_ip' not in filters:
        #     cond.append("destination_ip != ''")
        #     cond.append("destination_ip is not NULL")

        # if len(cond) > 0:
        #     cond_str = 'where ' + (' and '.join(cond))
        # else:
        #     cond_str = ''

        cmd = "select * from notification " + cond_str+" order by date_created desc"
        # print('cmd', cmd)

        return cmd

    def count_all(self, cmd):
        engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
        connection = engine.connect()
        cmd = 'select count(noti_id) from '+cmd.split('from')[1]
        print('[count_all] cmd', cmd)
        total = connection.execute(cmd).scalar()
        if total is None: 
            return 0

        total = int(total)
        print('~~total', total)
        return total

    def get(self, cmd, page=0):
        page_size = 30
        start = page*page_size
        end = (page+1)*page_size

        cmd = cmd + " limit "+str(start)+", "+str(end)
        print('** [get] cmd', cmd)

        engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
        connection = engine.connect()
        notis = connection.execute(cmd).fetchall()
        return notis


    def get_by_id(self, object_id):
        noti = Noti.query.filter_by(noti_id=object_id).first()
        return noti

    def update(self, object_id, data):
        noti = Noti.query.filter_by(noti_id=object_id).first()
        noti = self._parse_noti(data=data, noti=noti)
        db.session.commit()
        return noti

    def delete(self, object_id):
        noti = Noti.query.filter_by(noti_id=object_id).first()
        db.session.delete(noti)
        db.session.commit()

    def _parse_noti(self, data, noti=None):
        noti_id, user_id, message, date_created = None, None, None, None
        # print('~~ data _parse_noti', data)
        if 'user_id' in data:
            user_id = data['user_id']
        if 'message' in data:
            message = data['message']
        if 'date_created' in data:
            date_created = data['date_created']

        if noti is None:
            noti = Noti(user_id=user_id,
                        message=message,
                        date_created=date_created)
        else:
            noti.user_id = user_id
            noti.message = message
            noti.date_created = date_created
        return noti
