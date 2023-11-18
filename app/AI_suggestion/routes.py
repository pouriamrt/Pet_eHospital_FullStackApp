from app.AI_suggestion import bp
from flask import render_template, jsonify
from flask_login import login_required
from app.models.doctorProfile import doctorProfile

@login_required
@bp.route('/suggestion', methods=["GET"])
def get_suggestion_page():
    doctors = doctorProfile.query.all()
    return render_template('suggestion.html', doctors=doctors)

@bp.route('/get_doctors/<department>')
def get_doctors(department):
    doctors = doctorProfile.query.filter_by(department=department).all()
    doctors_data = [doc.to_dict() for doc in doctors]
    return jsonify(doctors_data)