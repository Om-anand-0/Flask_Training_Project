from flask import Blueprint, render_template
from flask_login import login_required,current_user,request
from app.models import Room, Message, Participant
from app import db,socketio
from flask_socketio import emit, join_room, leave_room

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    rooms = [p.room for p in current_user.rooms_joined]
    return render_template('chat/dashboard.html', rooms=rooms)

@chat_bp.route('/chat/<int:room_id>', methods=['GET', 'POST'])
@login_required
def chat_room(room_id):
    room = Room.query.get_or_404(room_id)
    return render_template('chat/chat_room.html', room=room, messages=room.messages)

@socketio.on('join')
def handle_join(data):
    room_id = data['room_id']
    join_room(room_id)
    emit('join', {'room_id': room_id}, room=room_id)

@socketio.on('leave')
def handle_leave(data):
    room_id = data['room_id']
    leave_room(room_id)
    emit('leave', {'room_id': room_id}, room=room_id)

@socketio.on('message')
def handle_message(data):
    room_id = data['room_id']
    content = data['message']
    msg_type = data['msg_type']
    message = Message(room_id=room_id, user_id=current_user.id, content=content, msg_type=msg_type)
    db.session.add(message)
    db.session.commit()
    emit('message', {
        'message': content,
        'msg_type': msg_type,
        'username': current_user.username
    }, room=room_id)
