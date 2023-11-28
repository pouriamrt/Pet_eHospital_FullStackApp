from app.extensions import db

class doctorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    department = db.Column(db.String(30))
    position = db.Column(db.String(40))
    doctor_img_url = db.Column(db.Text)
    introduction = db.Column(db.String(150))
    speciality = db.Column(db.Text)
    rate = db.Column(db.Numeric(precision=2, scale=1))
    email = db.Column(db.String(100), unique=True)


    def __repr__(self):
        return f'<doctorProfile "{self.name}">'

    def to_dict(self):
        return {
            'name': self.name,
            'speciality': self.speciality,
            'introduction': self.introduction,
            'url': self.doctor_img_url,
            'department': self.department,
            'position': self.position,
            'rate':self.rate
        }