const roomSelect = document.getElementById("roomSelect");
const joinBtn = document.getElementById("joinBtn");
const leaveBtn = document.getElementById("leaveBtn");
const statusMessage = document.getElementById("statusMessage");
const sendBtn = document.getElementById("sendBtn");
const messageInput = document.getElementById("messageInput");
const messages = document.getElementById("messages");
const socket = io();
let fingerprint = '';
import generateFingerprint from './fingerprint.js';

socket.on("connect", () => {
  console.log("Connected to server");
});
socket.on("disconnect", () => {
  console.log("Disconnected from server");
});

roomSelect.addEventListener("change", () => {
  const selectedRoom = roomSelect.value;
  if (selectedRoom) {
    joinBtn.disabled = false;
    statusMessage.style.display = "none";
  } else {
    joinBtn.disabled = true;
  }
});

joinBtn.addEventListener("click", async () => {
  const selectedRoom = roomSelect.value;
  if (selectedRoom) {
    fingerprint = await generateFingerprint();
    socket.emit("join", { room: selectedRoom, fingerprint });
  } else {
    statusMessage.textContent = "Please select a room";
    statusMessage.className = "alert alert-danger mt-3";
    statusMessage.style.display = "block";
  }
});

socket.on("joined", (data) => {
  const selectedRoom = roomSelect.value;
  statusMessage.textContent = `You have joined the ${selectedRoom} room`;
  statusMessage.className = "alert alert-success mt-3";
  statusMessage.style.display = "block";
  joinBtn.disabled = true;
  leaveBtn.disabled = false;
  sendBtn.disabled = false;
  roomSelect.disabled = true;
});

sendBtn.addEventListener("click", () => {
  const message = messageInput.value;
  const isInRoom = roomSelect.value != null;
  if (message && isInRoom) {
    socket.emit("send_message", { room: roomSelect.value, message, fingerprint });
  }
});

socket.on("show_message", (data) => {
  const message = document.createElement("div");
  message.classList.add("message-bubble");

  if (data.fingerprint === fingerprint) {
    message.classList.add("message-sent");
  } else {
    message.classList.add("message-received");
  }

  message.textContent = data.message;
  messages.appendChild(message);
  messageInput.value = "";
  messages.scrollTop = messages.scrollHeight;
});

leaveBtn.addEventListener("click", () => {
  const selectedRoom = roomSelect.value;
  socket.emit("leave", { room: selectedRoom });
});

socket.on("left", (data) => {
  const selectedRoom = roomSelect.value;
  statusMessage.textContent = `You have left the room ${selectedRoom}`;
  statusMessage.className = "alert alert-warning mt-3";
  statusMessage.style.display = "block";
  joinBtn.disabled = false;
  leaveBtn.disabled = true;
  roomSelect.disabled = false;
  roomSelect.value = "";
  while (messages.lastElementChild) {
    messages.removeChild(messages.lastElementChild);
  }
});
