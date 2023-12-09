from datetime import datetime
from app.extensions import db

class DoctorClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_email = db.Column(db.String(100), unique=True)
    client_email = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(10))
    created_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<DoctorClient "{self.doctor_email}">'