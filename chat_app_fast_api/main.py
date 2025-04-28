from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import socketio

app = FastAPI()
templates = Jinja2Templates(directory="templates")
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
socket_app = socketio.ASGIApp(sio)
app.mount("/socket.io", socket_app)
connected_clients = set()

rooms = {}

@sio.event
async def connect(session_id,environment):
    connected_clients.add(session_id)
    print(f"Client Connected:{session_id}")

@sio.event
async def disconnect(session_id,environment):
    connected_clients.discard(session_id)
    print(f"Client Disconnected:{session_id}")
    

@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@sio.on('join')
async def handle_join(session_id,data):
    room = data['room']
    
    if room not in rooms:
        rooms[room] = set()
        
    rooms[room].add(session_id)
    
    await sio.enter_room(session_id, room)
    await sio.emit('joined_room', {"room": room}, room=room)
    
    print(f"CONNTECT TO ROOM:{room} SESSION ID:{session_id}")  


@sio.on('leave')
async def handle_leave(session_id,data):
    room = data['room']
    if room in rooms:
        
        rooms[room].discard(session_id)
        
        await sio.emit('left_room',{"room":room},room=room)
        await sio.leave_room(session_id,room)
        
        print(f"DISCONNTECTED FROM ROOM:{room} SESSION ID:{session_id}")  
        
@sio.on('send_message')
async def send_message(session_id,data):
    room = data['room']
    if room in rooms:
        message = data['message']
        
        await sio.emit('message_received',{'room':room,'message':message,'session_id': session_id },room=room)
        
        print(f"USER {session_id} sent message: {message}")
       