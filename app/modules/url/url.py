from app.modules.common.model import Model
from app.app import db


class Url(Model):
    __tablename__ = "capture_url"
    url_capture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    url = db.Column(db.String, nullable=False)
    date_requested = db.Column(db.Date)
    time_requested = db.Column(db.String)

    source_ip = db.Column(db.String)
    protocol = db.Column(db.String)

    is_malicious = db.Column(db.String)
    score = db.Column(db.String)

    def __init__(self, url, date_requested=None, time_requested=None, source_ip=None, protocol=None, is_malicious=None, score=None):
        self.url = url

        self.date_requested = date_requested
        self.time_requested = time_requested

        self.source_ip = source_ip
        self.protocol = protocol

        self.is_malicious = is_malicious
        self.score = score
