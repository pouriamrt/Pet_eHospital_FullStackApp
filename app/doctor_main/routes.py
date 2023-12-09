from app.doctor_main import bp
<<<<<<< HEAD
from flask import render_template, request, url_for, jsonify
=======

from flask import render_template, request, url_for, jsonify, session
>>>>>>> 60ffcc45cfb25fb7b72f8b74c2c3ffc1b817cd35
from flask_login import login_required, current_user

from app.models.doctorProfile import doctorProfile
from app.models.petProfile import PetProfile
from app.models.auth import User
from app.doctor_main.client_info_vo import ClientInfoVo
from app.models.DoctorClient import DoctorClient


@bp.route('/doctor_portal')
@login_required
def index():
    doctor_email = session['email']
    doctor_profile = doctorProfile.query.filter_by(email=doctor_email).first()
    print(doctorProfile.query.all())

    doctor_clients = DoctorClient.query.filter_by(doctor_email=doctor_email).all()
    client_infos = []
    for doctor_client in doctor_clients:
        user = User.query.filter_by(email=doctor_client.client_email).first()
        pet = PetProfile.query.filter_by(user_email=doctor_client.client_email).first()
        if user and pet:
            client_info = ClientInfoVo(doctor_client.created_timestamp, user.name, pet.name, pet.pet_type, pet.age, pet.breed, pet.weight, doctor_client.status)
            client_infos.append(client_info)
    print(client_infos)
    print(doctor_profile)

    return render_template('doctor_side/portal.html', name=doctor_profile.name, client_infos=client_infos, doctor_profile=doctor_profile)