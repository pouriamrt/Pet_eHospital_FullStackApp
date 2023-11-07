from app.pet_profile import bp
from flask import render_template
from flask_login import login_required, current_user

@bp.route('/mypet')
@login_required
def pet_profile():
    return render_template('PetProfile.html')