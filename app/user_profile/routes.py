from app.user_profile import bp
from flask import render_template, request,url_for, redirect
from flask_login import login_required, current_user
from app.models.auth import User
from app.extensions import db

@bp.route('/', methods=['GET', 'POST', 'PUT'])
@login_required
def user_profile():
    user = User.query.filter_by(id=current_user.id).first()

    if request.method == 'POST':
        if request.form['name']:
            user.name = request.form['name']
        if request.form['email']:
            user.email = request.form['email']
        if request.form['password']:
            user.password = request.form['password']
        db.session.commit()
        return redirect(url_for('user_profile.user_profile'))



    return render_template('user_profile.html', user=user)