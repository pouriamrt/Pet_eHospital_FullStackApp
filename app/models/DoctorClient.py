from app.extensions import db

class DoctorClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_email = db.Column(db.String(100), unique=True)
    client_email = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(10))

    def __repr__(self):
        return f'<DoctorClient "{self.doctor_email}">'