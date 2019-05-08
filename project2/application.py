import os
import time

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from rooms import Rooms


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


rooms = {"general": Rooms("general")}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect(url_for("chat"))
    else:
        return render_template("index.html")


@app.route("/chat")
def chat():
    return render_template("chat.html", rooms=rooms.keys())


@socketio.on("submit room")
def add_room(data):
    room = data["room"]

    if room not in rooms:
        rooms[room] = Rooms(room)
        emit("add room", room, broadcast=True)
    else:
        # Alerts only user, who tried adding room
        emit("room already exist")


@socketio.on("join")
def on_join(data):
    """ User can join specific room, and message about
    joining will be displayed to all users in the room, and displays
     old messages stored in room"""
    username = data["username"]
    room = data["room"]
    messages = rooms[room].messages
    users = rooms[room].users.values()

    join_room(room)

    emit("display messages and online users", (messages, list(users)))
    if username not in users:
        rooms[room].append_user(username, request.sid)
    emit("joined", (username, room), room=room)


@socketio.on("message")
def send_message(data):
    room = data["room"]
    message = data["message"]
    user = data["username"]

    epoch = time.localtime()
    time_string = time.strftime("%H:%M", epoch)

    if room in rooms:
        room_object = rooms.get(room)
        room_object.append_message([user, message, time_string])
        room_object.enforce_max_messages()
        emit("message", (message, user, time_string), room=room)


@socketio.on("leave")
def on_leave(data):
    room = data["room"]
    username = data["username"]
    emit("user left room", username, room=room)

    rooms[room].remove_user(request.sid)
    leave_room(room)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
