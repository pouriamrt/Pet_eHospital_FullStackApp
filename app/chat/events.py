from flask import session, request
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from app.models.chats import Chats
from app.extensions import db

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    print(room)
    join_room(room)
    #emit('status', {'msg': session.get('email') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    sender_email = session['email']
    receiver_email = session['doc_email']
    
    new_message = Chats(sender=sender_email, receiver=receiver_email, message=message["msg"])
    db.session.add(new_message)
    db.session.commit()
    
    sender_sid = request.sid
    
    emit('message', {'msg': message['msg'], 'sender_sid': sender_sid}, room=session.get('room'))


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    #emit('status', {'msg': session.get('email') + ' has left the room.'}, room=room)
