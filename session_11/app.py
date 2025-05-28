from flask import Flask , render_template
from flask_socketio import SocketIO
from ai import send_message_to_llm
app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')



@socketio.on('human-message-send')
def handle_human_message(data):
    message = data['message']
    if message:
        llm_response = send_message_to_llm(message)
        socketio.emit('llm_reponse',{'llm_response':llm_response.content})
        

if __name__ == "__main__":
    socketio.run(app,debug=True)