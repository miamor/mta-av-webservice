from app.modules.common.controller import Controller
from .url import Url
from app.app import db
from app.settings.config import Config
import datetime
import app.settings.cf as cf
from flask_restplus import marshal
import time

import sys
sys.path.insert(1, cf.__URLCHECKER_ROOT__)
import classifier as urlclassifier

# import sys
# sys.path.insert(1, cf.__URLCHECKER_ROOT__)
# import classifier as urlclassifier

# engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
# connection = engine.connect()


class ControllerUrl(Controller):
    def create(self, data):
        data['date_requested'] = time.strftime('%Y-%m-%d')
        data['time_requested'] = time.strftime('%H:%M:%S')
        url_captured = self._parse_url(data=data, url_captured=None)
        db.session.add(url_captured)
        db.session.commit()
        return url_captured



    def get_query(self, mode, filters=None):
        modes = mode.split(',')
        # print('~~~~~~ modes', modes)

        cond = []
        if 'benign' in modes and 'critical' not in modes and 'malware' not in modes:
            cond.append(
                "detected_by not like '%static%' and detected_by not like '%virustotal%' and detected_by not like '%HAN_sec%' and detected_by not like '%cuckoo%'")

        if filters is not None:
            for key in filters:
                if key not in ['types', 'mode', 'p', 'page']:
                    print(key, filters[key])
                    cond.append("{} = '{}'".format(key, filters[key]))

        if len(cond) > 0:
            cond_str = 'where ' + (' and '.join(cond))
        else:
            cond_str = ''

        cmd = "select url_capture_id, url, source_ip, protocol, date_requested, time_requested, is_malicious, score from capture_url " + cond_str+" order by date_requested desc, time_requested desc"
        # print('cmd', cmd)

        return cmd

    def count_all(self, cmd):
        engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
        connection = engine.connect()
        cmd = 'select count(url_capture_id) from '+cmd.split('from')[1]
        # print('[count_all] cmd', cmd)
        total = connection.execute(cmd).scalar()
        if total is None: 
            return 0

        total = int(total)
        # print('~~total', total)
        return total

    def get(self, cmd, page=0):
        page_size = 30
        start = page*page_size
        end = (page+1)*page_size

        cmd = cmd + " limit "+str(start)+", "+str(end)
        print('** [get] cmd', cmd)

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


    def check(self, urls, source_ips):
        is_malicious_urls = []
        if len(urls) > 0:
            is_malicious_urls = urlclassifier.classifier(urls).tolist()
        for i in range(len(urls)):
            if is_malicious_urls[i] == 1:
                data = {
                    'url': urls[i],
                    'is_malicious': is_malicious_urls[i],
                    'source_ip': source_ips[i]
                }
                self.create(data=data)
        add_total_url_cmd = "insert into total_urls (date, time, total) values('{}', '{}', '{}')".format(str(datetime.datetime.now().strftime('%Y-%m-%d')), str(datetime.datetime.now().strftime('%H:%M:%S')), len(urls))

        engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
        connection = engine.connect()
        connection.execute(add_total_url_cmd)

        return urls, is_malicious_urls


    def stat_by_date(self, days, split):
        today = datetime.datetime.now()
        dist = datetime.timedelta(days=days)
        d_start = today - dist

        print('[/url][stat_by_date] days', days, 'split', split)
        print('[/url][stat_by_date] d_start', d_start)

        stat_by_date_tot_cmd = db.select([
            db.func.count(db.distinct(Url.url)).label('total_url'),

            db.func.count(Url.url_capture_id).label('total'),

            db.func.FROM_UNIXTIME(db.func.FLOOR(db.func.UNIX_TIMESTAMP(
                db.func.timestamp(Url.date_requested, Url.time_requested)
            )/split)*split).label('time')

        ]).group_by(
            'time'
        ).where(db.and_(
            Url.url.notlike('%msftncsi%'), 
            Url.date_requested.isnot(None), 
            Url.date_requested >= d_start,
            Url.date_requested <= today
        )).order_by(db.asc('time'))

        engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
        connection = engine.connect()

        stat_date_tot = connection.execute(stat_by_date_tot_cmd).fetchall()

        stat_by_date_data_req = []
        stat_by_date_data_url = []
        stat_by_date_cat = []
        for k, r in enumerate(stat_date_tot):
            # print(r)
            stat_by_date_data_url.append(r[0])
            stat_by_date_cat.append(r[2].strftime('%d/%m, %H:%M'))
            stat_by_date_data_req.append(r[1])

        stat_by_date = {
            'series': [{
                'name': 'Total URLs',
                # 'type': 'column',
                'type': 'area',
                'data': stat_by_date_data_url
            }, {
                'name': 'Total requests',
                'type': 'line',
                'data': stat_by_date_data_req
            }],
            'cat': stat_by_date_cat
        }
        # print('stat_by_date', stat_by_date)

        return stat_by_date


    def stat(self):
        top_url_cmd = db.select([db.func.count(Url.url_capture_id).label('total'), Url.url]).where(db.and_(Url.url.isnot(None), Url.url.notlike('%msftncsi%'))).group_by(Url.url).order_by(db.desc('total')).limit(5)


        engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
        connection = engine.connect()

        top_url = connection.execute(top_url_cmd).fetchall()

        top_url_data = []
        for r in top_url:
            top_url_data.append({'url': r[1], 'total': r[0]})


        stat_data = {
            'top_url': top_url_data
        }

        return stat_data


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

