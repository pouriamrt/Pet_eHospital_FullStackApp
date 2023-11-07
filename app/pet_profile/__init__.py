from flask import Blueprint

bp = Blueprint("pet_profile", __name__)

from app.pet_profile import routes