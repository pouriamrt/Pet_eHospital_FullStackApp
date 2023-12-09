from app.models.doctorProfile import doctorProfile
from app.user_profile import bp
from flask import render_template, request,url_for, redirect
from flask_login import login_required, current_user
from app.models.auth import User, DoctorUser
from app.extensions import db
from werkzeug.security import generate_password_hash

@bp.route('/doctor_my_profile', methods=['GET', 'POST', 'PUT'])
@login_required
def doctor_user_profile():
    doctor_User = DoctorUser.query.filter_by(id=current_user.id).first()
    doctor_profile = doctorProfile.query.filter_by(email=doctor_User.email).first()
    
    if request.method == 'POST':
        flag = False
        print(doctor_User.email)
        if request.form['name']:
            doctor_User.name = request.form['name']
            flag = True
        if request.form['email']:
            doctor_User.email = request.form['email']
            flag = True
        if request.form['password']:
            flag = True
            doctor_User.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256:600000')
        if request.form['speciality']:
            doctor_profile.speciality = request.form['speciality']
            flag = True
        if request.form['position']:
            doctor_profile.position = request.form['position']
            flag = True
        if request.form['department']:
            doctor_profile.department = request.form['department']
            flag = True
        if request.form['introduction']:
            doctor_profile.introduction = request.form['introduction']
            flag = True
        if flag:
            db.session.commit()
        return redirect(url_for('user_profile.doctor_user_profile'))

    return render_template('doctor_side/doctor_user_profile.html', user=doctor_User)



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
