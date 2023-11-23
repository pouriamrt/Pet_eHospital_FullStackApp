from flask import Blueprint

bp = Blueprint('AI_suggestion', __name__)

from app.AI_suggestion import routes