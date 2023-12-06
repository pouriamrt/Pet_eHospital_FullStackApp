from app.doctor_profile import bp
from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user
from app.models.doctorProfile import doctorProfile as Doctor
from app.models.comment import Comment
from app.extensions import db

@bp.route('/doctor_profile')
@login_required
def doctor_profile():
    doctor_id = 1
    doctor = Doctor.query.filter_by(id=doctor_id).first()
    comments = Comment.query.filter_by(doctor_id=doctor_id).all()

    return render_template('doctor_profile.html', doctor=doctor, comments=comments)
