from flask import Blueprint

bp = Blueprint("user_profile", __name__)

from app.user_profile import routes