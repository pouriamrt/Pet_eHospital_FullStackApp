from flask import Blueprint

bp = Blueprint('doctor_main', __name__)

from app.doctor_main import routes