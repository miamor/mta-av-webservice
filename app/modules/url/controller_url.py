from app.modules.common.controller import Controller
from .capture import Url
from app.app import db
from app.settings.config import Config
import datetime
import app.settings.cf as cf
from flask_restplus import marshal

# import sys
# sys.path.insert(1, cf.__URLCHECKER_ROOT__)
# import classifier as urlclassifier

# engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
# connection = engine.connect()


class ControllerUrl(Controller):
    def create(self, data):
        url_captured = self._parse_url(data=data, url_captured=None)
        db.session.add(url_captured)
        db.session.commit()
        return url_captured

    def get(self, filters=None, page=0):
        page_size = 30
        start = page*page_size
        end = (page+1)*page_size

        cond = []

        if len(cond) > 0:
            cond_str = 'where ' + (' and '.join(cond))
        else:
            cond_str = ''
        cmd = "select url_capture_id, url, source_ip, protocol, date_requested, time_requested, is_malicious, score from capture " + \
            cond_str+" order by date_requested desc, time_requested desc"
        print('cmd', cmd)

        engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
        connection = engine.connect()

        urls_captured = connection.execute(cmd).fetchall()
        return urls_captured

    def get_by_id(self, object_id):
        url_captured = Url.query.filter_by(url_capture_id=object_id).first()
        return url_captured

    def update(self, object_id, data):
        url_captured = Url.query.filter_by(url_capture_id=object_id).first()
        url_captured = self._parse_url(data=data, url_captured=url_captured)
        db.session.commit()
        return url_captured

    def delete(self, object_id):
        url_captured = Url.query.filter_by(url_capture_id=object_id).first()
        db.session.delete(url_captured)
        db.session.commit()

    def _parse_url(self, data, url_captured=None):
        url, date_requested, time_requested, source_ip, protocol, is_malicious, score = None, None, None, None, None, None, None
        # print('~~ data _parse_url', data)
        if 'url' in data:
            url = data['url']
        if 'date_requested' in data:
            date_requested = data['date_requested']
        if 'time_requested' in data:
            time_requested = data['time_requested']
        if 'source_ip' in data:
            source_ip = data['source_ip']
        if 'protocol' in data:
            protocol = data['protocol']
        if 'is_malicious' in data:
            is_malicious = data['is_malicious']
        if 'score' in data:
            score = data['score']

        if url_captured is None:
            url_captured = Url(url=url, 
                                date_requested=date_requested, 
                                time_requested=time_requested,
                                source_ip=source_ip, 
                                protocol=protocol,
                                is_malicious=is_malicious,
                                score=score)
        else:
            url_captured.url = url
            url_captured.date_requested = date_requested
            url_captured.time_requested = time_requested
            url_captured.source_ip = source_ip
            url_captured.protocol  =  protocol
            url_captured.is_malicious = is_malicious
            url_captured.score = score
        return url_captured

