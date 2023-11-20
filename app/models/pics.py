from app.extensions import db

class Pictures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    pet_img_url = db.Column(db.Text)

    def __repr__(self):
        return f'<Pictures "{self.email}">'
    