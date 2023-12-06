<<<<<<< HEAD
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



=======
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



>>>>>>> 1a22a7e358ff1bed34c6e598981293764ecef85d
    return render_template('user_profile.html', user=user)