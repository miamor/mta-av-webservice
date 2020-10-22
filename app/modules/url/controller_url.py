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
        malware = self._parse_url(data=data, malware=None)
        db.session.add(malware)
        db.session.commit()
        return malware

    def get(self, mode, filters=None, page=0):
        modes = mode.split(',')
        print('~~~~~~ modes', modes)

        page_size = 30
        start = page*page_size
        end = (page+1)*page_size

        cond = []
        if 'benign' in modes and 'critical' not in modes and 'malware' not in modes:
            cond.append(
                "detected_by not like '%static%' and detected_by not like '%virustotal%' and detected_by not like '%HAN_sec%' and detected_by not like '%cuckoo%'")

        for key in filters:
            if key not in ['types', 'mode']:
                print(key, filters[key])
                cond.append("{} = '{}'".format(key, filters[key]))

        if len(cond) > 0:
            cond_str = 'where ' + (' and '.join(cond))
        else:
            cond_str = ''
        cmd = "select capture_id, file_name, file_size, hash, source_ip, destination_ip, protocol, date_received, time_received, detected_by from capture " + \
            cond_str+" order by date_received desc, time_received desc"
        # cmd = "select capture_id, file_name, file_size, hash, source_ip, destination_ip, protocol, date_received, time_received, detected_by from capture "+cond_str+" order by date_received desc, time_received desc limit "+str(start)+", "+str(end)
        print('cmd', cmd)

        engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
        connection = engine.connect()

        malwares = connection.execute(cmd).fetchall()
        return malwares

    def get_by_id(self, object_id):
        malware = Url.query.filter_by(capture_id=object_id).first()
        return malware

    def update(self, object_id, data):
        malware = Url.query.filter_by(malware_id=object_id).first()
        malware = self._parse_url(data=data, malware=malware)
        db.session.commit()
        return malware

    def delete(self, object_id):
        malware = Url.query.filter_by(malware_id=object_id).first()
        db.session.delete(malware)
        db.session.commit()

    def _parse_url(self, data, malware=None):
        file_name, file_size, file_extension, file_path, hash, md5, sha1, sha256, sha512, ssdeep, report_path, report_id, date_created, date_modified, date_sent, time_sent, date_received, time_received, collection_date, collection_type, source_ip, destination_ip, source_url, destination_url, hostname, protocol, source_email, destination_email, source_country, destination_country, malware_type, source_dns, destination_dns, entropy, description, detected_by, detector_output, scan_time, warning_level = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
        # print('~~ data _parse_url', data)
        if 'file_name' in data:
            file_name = data['file_name']
        if 'file_size' in data:
            file_size = data['file_size']
        if 'file_extension' in data:
            file_extension = data['file_extension']
        if 'file_path' in data:
            file_path = data['file_path']

        if 'hash' in data:
            hash = data['hash']
        if 'md5' in data:
            md5 = data['md5']
        if 'sha1' in data:
            sha1 = data['sha1']
        if 'sha256' in data:
            sha256 = data['sha256']
        if 'sha512' in data:
            sha512 = data['sha512']
        if 'ssdeep' in data:
            ssdeep = data['ssdeep']
        if 'report_path' in data:
            report_path = data['report_path']
        if 'report_id' in data:
            report_id = data['report_id']

        if 'date_created' in data:
            date_created = data['date_created']
        if 'date_modified' in data:
            date_modified = data['date_modified']

        if 'date_sent' in data:
            date_sent = data['date_sent']
        if 'time_sent' in data:
            time_sent = data['time_sent']
        if 'date_received' in data:
            date_received = data['date_received']
        if 'time_received' in data:
            time_received = data['time_received']

        if 'collection_date' in data:
            collection_date = data['collection_date']
        if 'collection_type' in data:
            collection_type = data['collection_type']
        if 'source_ip' in data:
            source_ip = data['source_ip']
        if 'destination_ip' in data:
            destination_ip = data['destination_ip']

        if 'source_url' in data:
            source_url = data['source_url']
        if 'destination_url' in data:
            destination_url = data['destination_url']
        if 'hostname' in data:
            hostname = data['hostname']
        if 'protocol' in data:
            protocol = data['protocol']

        if 'source_email' in data:
            source_email = data['source_email']
        if 'destination_email' in data:
            destination_email = data['destination_email']
        if 'source_country' in data:
            source_country = data['source_country']
        if 'destination_country' in data:
            destination_country = data['destination_country']

        if 'malware_type' in data:
            malware_type = data['malware_type']
        if 'source_dns' in data:
            source_dns = data['source_dns']
        if 'destination_dns' in data:
            destination_dns = data['destination_dns']
        if 'entropy' in data:
            entropy = data['entropy']

        if 'description' in data:
            description = data['description']
        if 'detected_by' in data:
            detected_by = data['detected_by']
        if 'detector_output' in data:
            detector_output = data['detector_output']
        if 'warning_level' in data:
            warning_level = data['warning_level']
        if 'scan_time' in data:
            scan_time = data['scan_time']

        if malware is None:
            malware = Url(file_name=file_name, file_size=file_size, file_extension=file_extension, hash=hash,
                              md5=md5, sha1=sha1, sha256=sha256, sha512=sha512, ssdeep=ssdeep,
                              report_path=report_path, report_id=report_id,
                              date_created=date_created, date_modified=date_modified, date_sent=date_sent,
                              date_received=date_received, time_received=time_received, collection_date=collection_date,
                              collection_type=collection_type, source_ip=source_ip, destination_ip=destination_ip,
                              source_url=source_url, destination_url=destination_url, hostname=hostname,
                              protocol=protocol, source_email=source_email, destination_email=destination_email,
                              source_country=source_country, destination_country=destination_country,
                              malware_type=malware_type, source_dns=source_dns, destination_dns=destination_dns,
                              entropy=entropy, description=description,
                              detected_by=detected_by, detector_output=detector_output,
                              scan_time=scan_time,
                              warning_level=warning_level)
        else:
            malware.file_name = file_name
            malware.file_size = file_size
            malware.file_extension = file_extension
            malware.file_path = file_path

            malware.hash = hash
            malware.md5 = md5
            malware.sha1 = sha1
            malware.sha256 = sha256
            malware.sha512 = sha512
            malware.ssdeep = ssdeep
            malware.report_path = report_path
            malware.report_id = report_id

            malware.date_created = date_created
            malware.date_modified = date_modified

            malware.date_sent = date_sent
            malware.time_sent = time_sent
            malware.date_received = date_received
            malware.time_received = time_received

            malware.collection_date = collection_date
            malware.collection_type = collection_type
            malware.source_ip = source_ip
            malware.destination_ip = destination_ip

            malware.source_url = source_url
            malware.destination_url = destination_url
            malware.hostname = hostname
            malware.protocol = protocol

            malware.source_email = source_email
            malware.destination_email = destination_email
            malware.source_country = source_country
            malware.destination_country = destination_country

            malware.malware_type = malware_type
            malware.source_dns = source_dns
            malware.destination_dns = destination_dns
            malware.entropy = entropy

            malware.description = description
            malware.detected_by = detected_by
            malware.detector_output = detector_output
            malware.scan_time = scan_time
            malware.warning_level = warning_level
        return malware

