from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('send_notification')
def send_notification(message):
    emit('new_notification',{'message':message},broadcast=True)
    
    


if __name__ == '__main__':
    socketio.run(app)