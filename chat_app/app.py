from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('join')
def handle_join(data):
    room = data['room']
    fingerprint = data['fingerprint']
    print(f"User joined room: {room}")
    join_room(room)
    emit('joined', room=room , fingerprint=fingerprint)

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    print(f"user left {room}")
    emit('left', room=room)
    leave_room(room)
    
@socketio.on('send_message')
def handle_message(data):
    room = data['room']
    message = data['message']
    fingerprint = data['fingerprint']
    print(f"Message received in room {room}: {message}")
    emit('show_message', {'message': message, 'fingerprint': fingerprint}, room=room)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret'
    socketio.run(app, debug=True)
# app.py