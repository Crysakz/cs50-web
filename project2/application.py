import os

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

online_users = []
rooms = []


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
    rooms.append(room_name)
    emit("add room", room_name, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
