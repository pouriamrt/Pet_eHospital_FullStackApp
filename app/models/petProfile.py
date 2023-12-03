# Import the database instance from extensions module
from app.extensions import db


class PetProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    pet_type = db.Column(db.String(64), index=True, unique=False)
    age = db.Column(db.Integer, index=True, unique=False)
    breed = db.Column(db.String(64), index=True, unique=False)
    weight = db.Column(db.Float, index=True, unique=False)
    user_email = db.Column(db.String(100), unique=True)  # Assuming you have a User model for the owner

    def __repr__(self):
        return f'<PetProfile {self.name}>'