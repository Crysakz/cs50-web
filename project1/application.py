import os

from flask import Flask, session, render_template, request, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def validate_register(username, password, password2):
    """ Function to validate Registration form on the server side """
    if (not username or not password) or not password2:
        return False
    elif password != password2:
        return False 
    return True

""" TODO Error Hanlder for custom error, like not same passwords or not filled input fields eg... """

@app.route("/")
def index():
    """ Landing Page """ 
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register User """ 
    if request.method == "POST":
        if validate_register(request.form["username"], request.form["password"], request.form["password2"]):
            print("succes") #TODO
        else:
            return render_template("register.html", alert="Please fill all fields")
        return render_template("index.html")
    else:
        return render_template("register.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Login  User """ 
    if request.method == "POST":
        return render_template("index.html")
    else:
        return render_template("login.html")
