from app.extensions import db

class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(30))
    phone = db.Column(db.Integer)
    email = db.Column(db.String(30))
    subject = db.Column(db.String(50))
    message = db.Column(db.Text)

    def __repr__(self):
        return f'<ContactForm "{self.subject}">'