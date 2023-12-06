from app.user_profile import bp
from flask import render_template, request,url_for, redirect
from flask_login import login_required, current_user
from app.models.auth import User
from app.extensions import db
from werkzeug.security import generate_password_hash

@bp.route('/my_profile', methods=['GET', 'POST', 'PUT'])
@login_required
def user_profile():
    user = User.query.filter_by(id=current_user.id).first()
    
    if request.method == 'POST':
        flag = False
        if request.form['name']:
            user.name = request.form['name']
            flag = True
        if request.form['email']:
            user.email = request.form['email']
            flag = True
        if request.form['password']:
            flag = True
            user.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256:600000')
        if flag:
            db.session.commit()
        return redirect(url_for('user_profile.user_profile'))



    return render_template('user_profile.html', user=user)