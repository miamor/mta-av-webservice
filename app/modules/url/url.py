from app.modules.common.model import Model
from app.app import db


class Capture(Model):
    __tablename__ = "capture"
    capture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    file_name = db.Column(db.String, nullable=False)
    file_size = db.Column(db.Float)
    file_extension = db.Column(db.String)
    file_path = db.Column(db.String)

    hash = db.Column(db.String)
    md5 = db.Column(db.String)
    sha1 = db.Column(db.String)
    sha256 = db.Column(db.String)
    sha512 = db.Column(db.String)
    ssdeep = db.Column(db.String)
    report_path = db.Column(db.String)
    report_id = db.Column(db.Integer)

    date_created = db.Column(db.Date)
    date_modified = db.Column(db.Date)

    date_sent = db.Column(db.Date)
    time_sent = db.Column(db.DateTime)
    date_received = db.Column(db.Date)
    time_received = db.Column(db.String)

    collection_date = db.Column(db.Date)
    collection_type = db.Column(db.String)
    source_ip = db.Column(db.String)
    destination_ip = db.Column(db.String)

    source_mac = db.Column(db.String)
    destination_mac = db.Column(db.String)

    source_url = db.Column(db.String)
    destination_url = db.Column(db.String)
    hostname = db.Column(db.String)
    protocol = db.Column(db.String)

    source_email = db.Column(db.String)
    destination_email = db.Column(db.String)
    source_country = db.Column(db.String)
    destination_country = db.Column(db.String)

    malware_type = db.Column(db.String)
    source_dns = db.Column(db.String)
    destination_dns = db.Column(db.String)
    entropy = db.Column(db.Float)

    description = db.Column(db.String)
    detected_by = db.Column(db.String)
    detector_output = db.Column(db.String)
    scan_time = db.Column(db.Float)
    warning_level = db.Column(db.Integer)

    def __init__(self, file_name, file_size=None, file_extension=None, file_path=None,
                 hash=None, md5=None, sha1=None, sha256=None, sha512=None, ssdeep=None,
                 report_path=None,report_id=None,
                 date_created=None, date_modified=None, date_sent=None, time_sent=None, date_received=None,
                 time_received=None, collection_date=None, collection_type=None, source_ip=None, destination_ip=None,
                 source_url=None, destination_url=None, hostname=None, protocol=None, source_email=None,
                 destination_email=None, source_country=None, destination_country=None, malware_type=None,
                 source_dns=None, destination_dns=None, entropy=None, description=None, detected_by=None, detector_output=None,
                 scan_time=None, warning_level=None):
        self.file_name = file_name
        self.file_size = file_size
        self.file_extension = file_extension
        self.file_path = file_path

        self.hash = hash
        self.md5 = md5
        self.sha1 = sha1
        self.sha256 = sha256
        self.sha512 = sha512
        self.ssdeep = ssdeep
        self.report_path = report_path
        self.report_id = report_id

        self.date_created = date_created
        self.date_modified = date_modified

        self.date_sent = date_sent
        self.time_sent = time_sent
        self.date_received = date_received
        self.time_received = time_received

        self.collection_date = collection_date
        self.collection_type = collection_type
        self.source_ip = source_ip
        self.destination_ip = destination_ip

        self.source_url = source_url
        self.destination_url = destination_url
        self.hostname = hostname
        self.protocol = protocol

        self.source_email = source_email
        self.destination_email = destination_email
        self.source_country = source_country
        self.destination_country = destination_country

        self.malware_type = malware_type
        self.source_dns = source_dns
        self.destination_dns = destination_dns
        self.entropy = entropy

        self.description = description
        self.detected_by = detected_by
        self.detector_output = detector_output
        self.scan_time = scan_time
        self.warning_level = warning_level