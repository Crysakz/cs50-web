import os

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, send, join_room, leave_room


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# TODO:
# Send message func
# Make better data structure for room
# Store last 100 messages per room
# Leave room function



rooms = ["general"]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect(url_for("chat"))
    else:
        return render_template("index.html")


@app.route("/chat")
def chat():
    return render_template("chat.html", rooms=rooms)


@socketio.on("submit room")
def add_room(data):
    room_name = data["roomName"]

    if room_name not in rooms:
        rooms.append(room_name)
        emit("add room", room_name, broadcast=True)
    else:
        # Alerts only user, who tried adding existing room
        emit("room already exist", room_name)


@socketio.on('join')
def on_join(data):
    """ User can join specific room, and message about
    joining will be displayed to all users in the room """
    username = data['username']
    room = data['room']
    join_room(room)
    emit("joined", (username, room), broadcast=True, room=room)


@socketio.on('leave')
def on_leave(data):
    # TODO
    """
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)
    """

if __name__ == '__main__':
    socketio.run(app)
