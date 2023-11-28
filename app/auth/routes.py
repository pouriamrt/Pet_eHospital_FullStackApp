from app.auth import bp
from flask import render_template, redirect, url_for, request, flash, session
from app.extensions import db
from app.models.auth import User, DoctorUser
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

@bp.route('/login')
def login():
    return render_template('auth/login.html')

@bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    session['email'] = user.email
    return redirect(url_for('main.index'))

@bp.route('/doctor_login')
def doctor_login():
    return render_template('auth/doctor_login.html')

@bp.route('/doctor_login', methods=['POST'])
def doctor_login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = DoctorUser.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.doctor_login'))

    login_user(user, remember=remember)
    session['email'] = user.email
    return redirect(url_for('doctor_main.index'))


@bp.route('/signup')
def signup():
    return render_template('auth/signup.html')

@bp.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    role = request.form.get('role')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    if role == "client":
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256:600000'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    else:
        new_user = DoctorUser(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256:600000'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.doctor_login'))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))