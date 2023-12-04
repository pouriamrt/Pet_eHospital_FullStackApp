from app.doctor_main import bp
from flask import render_template, request, url_for, jsonify
from flask_login import login_required, current_user
from app.extensions import db
import os

@bp.route('/doctor_portal')
@login_required
def index():
    return render_template('doctor_side/portal.html', name=current_user.name)