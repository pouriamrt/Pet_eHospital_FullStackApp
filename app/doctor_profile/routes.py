from app.doctor_profile import bp
from flask import render_template, request, url_for, redirect, session
from flask_login import login_required, current_user
from app.models.doctorProfile import doctorProfile as Doctor
from app.models.comment import Comment
from app.extensions import db

@bp.route('/doctor_profile', methods=["GET", "POST"])
@login_required
def doctor_profile():
    if request.method == 'POST':
        session['doc_email'] = request.get_data().decode()
        print(session['doc_email'])
        
    doctor = Doctor.query.filter_by(email=session['doc_email']).first()
    comments = Comment.query.filter_by(doctor_email=session['doc_email']).all()

    return render_template('doctor_profile.html', doctor=doctor, comments=comments)

@bp.route('/new_comment', methods=["POST"])
@login_required
def comment():
    content = request.form.get('content')
    rate = request.form.get('rate')
    new_comment = Comment(doctor_email=session['doc_email'], name=current_user.name, content=content, rate=rate, avatar="/static/logo.png")
    db.session.add(new_comment)
    db.session.commit()
    
    return redirect(url_for('doctor_profile.doctor_profile'))
    
