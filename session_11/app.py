from flask import Flask , render_template
from flask_socketio import SocketIO , emit
from ai import send_message_to_llm , chain , HumanMessage , AIMessage , chat_history
app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')



@socketio.on('human-message-send')
def handle_human_message(data):
    message = data['message']
    if message:
        chat_history.append(HumanMessage(message))
        llm_response = chain.stream({'input':message,'history':chat_history})
        whole_response = " "
        emit('generate_ai_chat_bubble')
        for chunk in llm_response:
            whole_response.join(chunk.content) 
            emit('llm_response_chunk',{'llm_response_chunk':chunk.content})
        chat_history.append(AIMessage(whole_response))    
        emit('generate_ai_chat_bubble_over')    
            
        

if __name__ == "__main__":
    socketio.run(app,debug=True)