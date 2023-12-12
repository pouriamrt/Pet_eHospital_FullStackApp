from app.extensions import db
from datetime import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_email = db.Column(db.String(30))
    name = db.Column(db.String(30))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.Text)
    content = db.Column(db.Text)
    rate = db.Column(db.Integer)
