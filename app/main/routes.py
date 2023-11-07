from app.main import bp
from flask import render_template
from flask_login import login_required, current_user

@bp.route('/')
@login_required
def index():
    return render_template('index.html', name=current_user.name)