from app.AI_suggestion import bp
from flask import render_template, jsonify, request
from flask_login import login_required
from app.models.doctorProfile import doctorProfile

@login_required
@bp.route('/suggestion', methods=["GET", "POST"])
def get_suggestion_page():
    department = request.args.get('department', default=None)
    if department:
        doctors = doctorProfile.query.filter_by(department=department).all()
    else:
        # 如果没有提供 department 参数，则获取所有医生
        doctors = doctorProfile.query.all()
    return render_template('suggestion.html', doctors=doctors, department=department)

@bp.route('/get_doctors/<department>')
def get_doctors(department):
    doctors = doctorProfile.query.filter_by(department=department).all()
    doctors_data = [doc.to_dict() for doc in doctors]
    return jsonify(doctors_data)