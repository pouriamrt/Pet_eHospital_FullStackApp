from app.extensions import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer)
    name = db.Column(db.String(30))
    created_time = db.Column(db.String(30))
    avatar = db.Column(db.Text)
    content = db.Column(db.Text)
    rate = db.Column(db.Integer)
