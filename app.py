html = """
<!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Class 10 Facebook</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="sKP4alsXsHG6lsdaSyAEvSi1PgLGpTITHkd6UvzOyJU" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400..800&family=Baloo+Bhai+2:wght@400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.5/socket.io.js"></script>
  <style>
:root {
    --body-color: #f0f4f9;
    --header-bg: linear-gradient(45deg, black,white, gray );
    --you-bg: #C6E7FF;
    /* Light green background for user's messages */
    --friend-bg: #FFF6E9;
    /* White background for friend's messages */
  }
  
  .header{
    color: green;
    font-weight: 300;
    font-size: 20px;
    text-align: center;
    height: 10vw;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    width: 100vw;
    background-image: var(--header-bg);
  }

    body {
      background-color: var(--body-color);
      margin: 0;
      font-family: Arial, sans-serif;
      display: flex;
      flex-direction: column;
      height: 100vh;
      font-family: "Baloo Bhai 2", sans-serif;
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
      overflow-wrap: break-word;
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
      word-break: break-word;
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


  </style>
</head>
<body>
  <div class="header"> Omegle clone </div>
  <div id="chat" class="chat">
  </div>
  <footer>
    <input class="input-box" placeholder="Message" id="mess" type="text">
    <button class="send" id="btn" onclick="send()">
      <i class="fas fa-paper-plane"></i>
    </button>
  </footer>
  
<script>
  const socket = io();
  var room;
  var can_msg = false; // Initialize can_msg as false
  
  var dis = document.getElementById('chat');
  var btn = document.getElementById("btn");
  var input = document.getElementById("mess");

  // Initially disable the button
  btn.disabled = true;
  input.disabled = true;

  socket.on("Your_room", (data) => {
    room = data["room"];
    can_msg = data["can_msg"];
    
    // Enable or disable the button based on can_msg
    btn.disabled = !can_msg;
    input.disabled = !can_msg ;
    
  });
  
 

  function send() {
    if (typeof room == "undefined" || !can_msg) return; // Prevent sending messages if can_msg is false
    let message = input.value.trim();
    if (message === "") return;
    input.value = "";
    let data = [room, message];
    addmsg("you", message);
    socket.emit("send_message", data);
  }

  socket.on("message", (data) => {
    addmsg("friend", data);
  });
  
  socket.on("clean_room", (data) => {
    if (typeof room == "undefined") return;
    if (room == data) {
      window.location.reload();
    }
  });

  function addmsg(clas, msg) { // you or friend
    const newDiv = document.createElement('div');
    newDiv.className = 'message';
    newDiv.innerHTML = `
      <div class="message-content ${clas}">
         ${msg}
      </div>    
    `;
    dis.appendChild(newDiv);
  }
  
</script>
</body>
</html>

"""

from flask import Flask, render_template_string, session , request 
from flask_socketio import SocketIO, emit , join_room
from flask_cors import CORS
import random 

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.secret_key ="5364+&42_gsbvj"
sio = SocketIO(app,cors_allowed_origins="*")

# schema 
# db = { room : #ocuupied True / False , .. }
db = {}  

# utility functions
def get_room():
	a="1234567890abcdefghijklmnopqrsruvwxyz@#£_&-"
	while True:
		st = ""
		for _ in range (10):
			st+=random.choice(a)
		if st not in db :  return st
	

@app.route('/')
def index():
	session.permanent = True 
	session.clear()
	return render_template_string(html)

@app.route("/alive")
def alive():
	return "Alive"
		
@sio.on('connect')
def connect ():
	rooms = [ room for room in db if db[room] == False ]
	print ()
	print ('Connected')
	print ()
	can_msg = False
	if not rooms:
		room = get_room()
		# initializing not occupied 
		db [room ] = False 
		join_room(room)
		emit ("partner_not_found")
	else:
		room =random.choice( rooms )
		db[ room ] = True 
		join_room ( room )
		can_msg = True 
		msg = "A user connected to your room "
		emit ('alert' , msg   , room = room )
		
	session ["room"] = room
	data = { "room":room , "can_msg":can_msg  }
	# your room or the room that you have joined
	emit("Your_room" , data , room = room)
	
@sio.on('disconnect')
def disconnect():
	print ()
	print ('disconnected')
	print ()
	room = session ["room"]
	print (room)
	if room in db:
		db.pop(room)
		emit("clean_room", room , broadcast= True)

@sio.on("send_message")
def send_message(data):
	room = data[0]
	message  = data[1]
	emit ( "message" , message , room = room , 
skip_sid = request.sid )
	
if __name__ == "__main__":
    sio.run(app, debug=True)
