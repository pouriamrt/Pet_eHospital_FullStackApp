from flask import Blueprint

bp = Blueprint('checkout', __name__)

from app.checkout import routes