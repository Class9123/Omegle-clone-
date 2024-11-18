

html1="""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WhatsApp Friends</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f0f2f5;
    }
    header {
      background-color: #128C7E;
      color: #fff;
      padding: 20px;
      text-align: center;
      position: relative;
      overflow: hidden;
      letter-spacing: 2px;
    }
    header::after {
      content: '';
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
      background-color: rgba(0, 0, 0, 0.2);
      z-index: -1;
      transition: transform 0.5s ease;
      transform: translateY(-100%);
    }
    header:hover::after {
      transform: translateY(0);
    }
    h1 {
      margin: 0;
      font-size: 24px;
      position: relative;
      z-index: 1;
      transition: color 0.5s ease;
    }
    header:hover h1 {
      color: #25D366;
    }
    .container {
      padding: 20px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-around;
    }
    .friend {
      display: flex;
      align-items: center;
      margin-bottom: 20px;
      background-color: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      transition: transform 0.3s ease;
      width: 90%;
    }
    .friend:hover {
      transform: translateY(-5px);
    }
    .friend img {
      width: 70px;
      height: 70px;
      border-radius: 50%;
      margin-right: 20px;
      border: 2px solid #25D366;
      padding: 5px;
      background-color: white;
    }
    .friend-info {
      flex-grow: 1;
      padding: 20px 0;
    }
    .friend-name {
      font-weight: bold;
      font-size: 18px;
      margin-bottom: 5px;
      max-width: 130px;
      word-wrap: break-word;
    }
    .friend-status {
      color: #888;
      font-size: 14px;
    }
    .add-user-btn {
      background-color: #25D366;
      color: #fff;
      padding: 10px;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      margin-bottom: 20px;
      transition: background-color 0.3s ease;
      font-size: 24px;
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 50px;
      height: 50px;
    }
    .add-user-btn:hover {
      background-color: #128C7E;
    }
   .user-form {
      display: none;
      background-color: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      padding: 20px;
      width: calc(100% - 60px );
      position: absolute;
      top: 50%;
      animation: expandForm 0.5s ease;
      transition: opacity 0.5s ease;
      opacity: 0;
      margin: 10px;
    }
    .user-form input {
      width: calc(100% - 10px);
      margin-bottom: 10px;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
      transition: all 0.3s ease;
      animation: placeholderAnim 1.5s infinite;
    }
    .user-form input:focus {
      border-color: #25D366;
      box-shadow: 0 0 5px #25D366;
    }
    .user-form input::placeholder {
      color: #888;
      transition: color 0.5s ease;
    }
    .user-form input:focus::placeholder {
      color: transparent;
    }
    .user-form button {
      background-color: #075e54;
      color: #fff;
      padding: 10px 20px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
    .user-form button:hover {
      background-color: #128C7E;
    }
    @keyframes expandForm {
      from {
        opacity: 0;
        transform: scale(0);
      }
      to {
        opacity: 1;
        transform: scale(1);
      }
    }
    @keyframes placeholderAnim {
      0% {
        transform: translateY(0);
      }
      50% {
        transform: translateY(-8px);
      }
      100% {
        transform: translateY(0);
      }
    }
    input {
      outline: none;
    }
    #close {
      color: black;
      font-size: 16px;
      position: relative;
      left: 90%;
      background-color: transparent;
    }
    .user-form button:hover {
      background-color: #128C7E;
    }
    span {
      letter-spacing: 6px;
    }
   .error{
      margin-bottom:15px;
   }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.5/socket.io.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
<body>
  <header>
    <h1><span>Ftalk</span> <br>Your no. {{ u_number }}</h1>
  </header>
  <div class="container" id="container">
    {% for d in data %}
      <div class="friend" onclick="go_Tochat('{{ d }}')">
        <img src="https://source.unsplash.com/random?w=100&h=100&fit=crop">
        <div class="friend-info">
          <div class="friend-name">{{ d }}</div>
          <div class="friend-status number"></div>
        </div>
      </div>
    {% endfor %}
  </div>
  <button class="add-user-btn" onclick="showForm()">+</button>
  <div class="user-form" id="userForm">
    <button id="close" class="close-btn" onclick="closeForm()">&times;</button>
    <div>
      <input type="text" placeholder="Enter number" id="f_number" required>
      <span id="error" class="error"></span><br><br>
      <button onclick="add_friend()">Add</button>
    </div>
  </div>
  <script>
    var u = "{{ u_number }}";
    var socket = io();

    function go_Tochat(d) {
      window.location.href = `/chat/${d}`;
    }

    function add_friend() {
      var data = { u_number: u, f_number: document.getElementById("f_number").value };
      socket.emit("add", data);
      document.getElementById("f_number").value = "";
      document.getElementById("error").textContent = "";
    }

    function showForm() {
      var form = document.getElementById("userForm");
      form.style.display = "block";
      setTimeout(function() {
        form.style.opacity = 1;
      }, 100);
    }

    function closeForm() {
      var form = document.getElementById("userForm");
      form.style.opacity = 0; // Fade out the form
      setTimeout(function() {
        form.style.display = "none"; // Hide the form after fading out
      }, 500);
      document.getElementById("f_number").value = "";
      document.getElementById("error").textContent = "";
    }

    socket.on("not_found", function(data) {
      document.getElementById("error").textContent = data;
    });

    socket.on("redirect", function() {
      window.location.reload();
      window.location.href = "/";
    });
  </script>
</body>
</html>

"""
# HTML templates as global variables

html="""
<!DOCTYPE
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Class 10 Facebook</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.5/socket.io.js"></script>
  <style>
:root {
    --body-color: #f0f4f9;
    --header-bg: linear-gradient(45deg, white, gray);
    --you-bg: #990011ff;
    /* Light green background for user's messages */
    --friend-bg: #00203fff;
    /* White background for friend's messages */
  }

    body {
      background-color: var(--body-color);
      margin: 0;
      font-family: Arial, sans-serif;
      display: flex;
      flex-direction: column;
      height: 100vh;
    }

    .header {
      box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.4);
      padding: 10px;
      background-image: var(--header-bg);
      position: sticky;
      top: 0;
      display: flex;
      align-items: center;
      z-index: 1;
    }

    .friend-profile {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      margin-right: 10px;
    }

    .friend-name {
      font-size: 20px;
      font-weight: bold;
    }

    .chat {
      flex: 1;
      overflow-y: auto;
      padding: 10px;
      margin-bottom: 60px;
      /* Footer height + some padding */
    }

    .message {
      display: flex;
      flex-direction: column;
      margin-bottom: 20px;
    }

    .you {

      align-self: flex-end;
    }

    .friend {
      align-self: flex-start;
    }

    .message-content {
      display: flex;
      flex-direction: column;
      box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
      border-radius: 15px;
      padding: 10px;
      max-width: 70%;
      word-wrap: break-word;
      margin-bottom: 3px;
      margin: 0,2px,0,2px;
      background-color: var(--friend-bg);
    }

    .message-content.you {
      color: white;
      color: #a07855ff;
      background-color: var(--you-bg);
    }
    .message-content.friend {
      color: #a07855ff;
      background-color: var(--friend-bg);
      align-items: flex-end;
    }

    footer {
      display: flex;
      align-items: center;
      background-color: white;
      padding: 10px;
      position: fixed;
      bottom: 0;
      width: 100%;
      box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }

    .input-box {
      flex: 1;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 20px;
      outline: none;
      margin-right: 10px;
      font-size: 16px;
    }

    .send {
      background-color: #ce4a7eff;
      border: none;
      border-radius: 10%;
      padding: 10px;
      box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
      cursor: pointer;
    }

    .send i {
      font-size: 18px;
      color: gray;
      margin-right: 10px;
    }

    .send:hover {
      animation: an1 0.3s;
    }

    @keyframes an1 {
      0% {
        transform: rotate(0deg);
      }
      50% {
        transform: rotate(180deg);
      }
      100% {
        transform: rotate(0deg);
      }
    }

    .scroll-button {
      display: none;
      position: fixed;
      bottom: 80px;
      /* Adjusted for better positioning */
      right: 20px;
      background-color: #f7ced7ff;
      border: none;
      border-radius: 50%;
      padding: 15px;
      box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
      cursor: pointer;
      z-index: 1;

    }

    .scroll-button i {
      font-size: 18px;
      color: #6e4c1eff;

    }
    .date {
      font-size: 10px;
      color: gray;
    }
    .date span {
      font-size: 15px;
      margin: 2px;
    }
  </style>
</head>
<body>
  <div class="header">
    <img class="friend-profile" src="">
    <label class="friend-name">Dev &times;</label>
    your no. 98727267
  </div>
  <div id="chat" class="chat">
    {% for j in chats %}
      <div class='message'>
        <div class="message-content {{j[0]}}">
          <div class="date">
            D:{{j[2][0]}} <br> &#9201; {{j[2][1]}}
          </div>
          {{j[1]}}
        </div>
      </div>
    {% endfor %}
  </div>
  <footer>
    <input class="input-box" placeholder="Message" id="message_input" type="text">
    <button class="send" id="sendbtn">
      <i class="fas fa-paper-plane"></i>
    </button>
  </footer>
  <button id="scrollButton" class="scroll-button" onclick="scrollToBottom()">
    <i class="fas fa-arrow-down"></i>
  </button>
  <script>
    var f = "{{ f_number }}";
    var u = "{{ u_number }}";
    var socket = io();
    var chat = document.getElementById('chat');
    var scrollButton = document.getElementById('scrollButton');
    var messageInput = document.getElementById('message_input');

    function sendMessage() {
      var message = messageInput.value.trim();
      if (message === "") {
        return;
      }
      var data = {
        message: message,
        f_number: f,
        u_number: u
      };
      socket.emit('send_message', data);
    }

    function addMessage(message) {
      var messageDiv = document.createElement("div");
      messageDiv.classList.add("message");
      messageDiv.innerHTML = `
        <div class="message-content friend">
          <div class="date">
            D:${message.date} <br> &#9201; ${message.time}
          </div>
          ${message.message}
        </div>
      `;
      chat.appendChild(messageDiv);
      showScrollButtonIfNeeded();
    }

    function scrollToBottom() {
      chat.scrollTop = chat.scrollHeight;
    }

    function showScrollButtonIfNeeded() {
      if (chat.scrollTop + chat.clientHeight < chat.scrollHeight - 1) {
        scrollButton.style.display = 'block';
      } else {
        scrollButton.style.display = 'none';
      }
    }

    messageInput.addEventListener('keyup', function(event) {
      if (event.key === 'Enter') {
        sendMessage();
      }
    });

    document.getElementById("sendbtn").addEventListener("click", sendMessage);

    document.getElementById("scrollButton").addEventListener("click", scrollToBottom);

    socket.emit('join_room', {
      u_number: u,
      f_number: f
    });

    socket.on("date_time", function(date_time) {
      var messageDiv = document.createElement("div");
      messageDiv.classList.add("message");
      messageDiv.innerHTML = `
        <div class="message-content you">
          <div class="date">
            D:${date_time.date} <br> &#9201; ${date_time.time}
          </div>
          ${date_time.message}
        </div>
      `;
      chat.appendChild(messageDiv);
      messageInput.value = '';
      scrollToBottom();
    });

    socket.on('receive_message', function(message) {
      addMessage(message);
    });

    chat.addEventListener('scroll', function() {
      showScrollButtonIfNeeded();
    });

    messageInput.addEventListener('focus', function() {
      if (scrollButton.style.display !== 'none') {
        scrollButton.click();
      }
    });

    scrollToBottom();
  </script>
</body>

</html>
"""
from flask import Flask, render_template_string, request, session, redirect 
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
import random 
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hbcguf FF for diff FjdjsjsjsjF ft f"
app.config['SESSION_TYPE'] = 'filesystem'
CORS(app)
sio = SocketIO(app)

rooms = [] 
used_numbers = set()
database = {}

def get_room_name(n1, n2):
    return str(int(n1) + int(n2))
	
def generate_number():
    global used_numbers
    while True:
        number = random.randint(10000000, 99999999)
        if number not in used_numbers:
            used_numbers.add(number)
            return "98" + str(number)

def get_date():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d ")
    time = now.strftime("%I:%M %p")
    return (date, time)
	
@app.route('/')
def index():
    session.permanent = True    		
    if session.get("number") is not None:
        number = session['number']
        if not (number in database):
            number = generate_number()
            session["number"] = number 
            database[number] = { "number": number, "friends": {} }
    else: 
        number = generate_number()
        session['number'] = number
        database[number] = { "number": number, "friends": {} }
    data = list(database[number]['friends'].keys())
    return render_template_string(html1, data=data, u_number=number)

@app.route("/chat/<f_number>")
def chat(f_number):
    if not(session.get('number')):
        return redirect('/')
    u = session["number"]
    f = f_number
    if not (u in database and f in database):
        return redirect("/")
    chats = database[u]['friends'][f]
    return render_template_string(html, chats=chats, f_number=f, u_number=u)

# For chatting 
@sio.on("join_room")
def handle_join(data):
    u = data["u_number"]
    f = data["f_number"]
    room = get_room_name(u, f)
    join_room(room)
    #("room joined", room)

@sio.on("send_message")
def handle_message(data):
    u = data["u_number"]
    f = data["f_number"]
    message = data["message"]
    #("m",message)
    dt = get_date()
    database[u]['friends'][f].append(("you", message, dt))
    database[f]["friends"][u].append(("friend", message, dt))
    date = {  "message": message , "date": dt[0], "time": dt[1] }
    #("\nreached\n")
    emit("date_time", date, sid=request.sid)
    message = { "message": message, "date": dt[0], "time": dt[1] }
    room_name = get_room_name(u, f)
    emit("receive_message", message, skip_sid=request.sid, room=room_name)

# For adding new friends 
@sio.on("add")
def add(data):
    u = data['u_number'].strip()
    f = data['f_number'].strip()
    u = str(u)
    f = str(f)
    if u == f:
        data = "This is your own number"
        emit("not_found", data, sid=request.sid)
        return 
    elif not f in database:
        data = "user not found"
        emit("not_found", data, sid=request.sid)
        return 
    if f in database:
        room_name = get_room_name(u, f)
        if not room_name in rooms:
            dt = get_date()
            database[u]['friends'][f] = [("you", "hi", dt)]
            database[f]['friends'][u] = [("friend", "hi", dt)]
            rooms.append(room_name)
            join_room(room_name)
            emit("redirect", sid=request.sid)

if __name__ == '__main__':

    sio.run(app, debug=True)
    
    
    
