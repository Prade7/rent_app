from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    messages = db.relationship('Message', backref='conversation', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)



from flask_socketio import SocketIO, send, join_room, leave_room
from flask import request

# socketio = SocketIO(app)

@socketio.on('message')
def handle_message(data):
    sender = User.query.filter_by(username=data['username']).first()
    conversation = Conversation.query.get(data['conversation_id'])
    message = Message(text=data['message'], sender_id=sender.id, conversation_id=conversation.id)
    db.session.add(message)
    db.session.commit()
    send(data['message'], room=data['room'])



@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)
