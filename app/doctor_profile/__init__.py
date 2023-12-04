from flask import Blueprint

bp = Blueprint("doctor_profile", __name__)

from app.doctor_profile import routes