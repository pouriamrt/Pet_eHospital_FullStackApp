from flask import render_template, session, request, jsonify
from app.chat import bp
from flask_login import login_required
from app.models.chats import Chats
from app.extensions import db
from sqlalchemy import or_, and_

@bp.route("/chat")
@login_required
def room():
    session["room"] = "_".join(sorted([session['email'], "pmort101@uottawa.ca"]))
    return render_template("chat.html")

# @bp.route("/send_message", methods=['POST'])
# @login_required
# def send_msg():
#     sender_email = session['email']
#     receiver_email = "pmort101@uottawa.ca" #request.form['receiver_email']
#     message = request.form['message']
    
#     new_message = Chats(sender=sender_email, receiver=receiver_email, message=message)
#     db.session.add(new_message)
#     db.session.commit()
    
#     return jsonify({'success': True})

@bp.route('/get_messages', methods=['GET'])
@login_required
def get_messages():
    sender_email = session['email']
    receiver_email = "pmort101@uottawa.ca" #request.args.get('receiver_id')
    
    messages = Chats.query.filter(
        or_(
        and_(Chats.sender == sender_email, Chats.receiver == receiver_email),
        and_(Chats.sender == receiver_email, Chats.receiver == sender_email)
    )
    ).order_by(Chats.timestamp).all()
    
    data = to_json(messages)
    data = jsonify(data)
    print(data)
    return data

def to_json(messages):
    data = []
    for msg_obj in messages:
        sender = False
        if msg_obj.sender == session['email']:
            sender = True
        data.append({"message": msg_obj.message, "sender": sender, "timestamp": msg_obj.timestamp})
    return data