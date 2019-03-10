import os
import requests

from flask import Flask, session, render_template, request, url_for, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError, DataError

from werkzeug.security import generate_password_hash, check_password_hash

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

# Check for API key enviroment varable
if not os.getenv("KEY"):
    raise RuntimeError("Goodreads API is not set")


def validate_register(username, password, password2):
    """ Function to validate Registration form on the server side """
    if (not username or not password) or not password2:
        return False, "Please fill all fields"
    elif password != password2:
        return False, "Passwords dont match!"
    elif len(password) < 5 or len(password2) < 5:
        return False, "Minimum length of password is 5 chars"
    return True, "Succesfully registered"


def validate_login(username, password):
    """ Validate credential before sending SQL requests """
    message = "Invalid username or password"
    if not username or not password:
        return False, message
    elif len(password) < 5:
        return False, message
    return True, "Welcome back"


@app.route("/", methods=["GET", "POST"])
def index():
    """ Landing Page, If user is logged in, he can search for books.
    Othervise he will be redirected to log in page."""

    if request.method == "POST":
        search = request.form["search"]

        if not search:
            return render_template("index.html",
                                   user=True,
                                   alert="Please fill the Search  field!")

        # Fixes users and database casing by using UPPER function
        rows = db.execute("""SELECT * FROM books WHERE UPPER(isbn)
                         LIKE :search OR UPPER(title)
                         LIKE :search OR UPPER(author)
                         LIKE :search""",
                          {"search": "%" + search.upper() + "%"}).fetchall()

        if not rows:
            return render_template("index.html",
                                   user=True,
                                   alert="We dont know this book. Sorry! :(")

        return render_template("index.html", user=True, rows=rows)

    else:
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        else:
            return render_template("index.html", user=True)


@app.route("/books/<string:isbn>", methods=["GET", "POST"])
def books(isbn):
    if request.method == "GET":

        if session.get("user_id") is None:
            return redirect(url_for("login"))

        book = db.execute("SELECT * FROM books WHERE isbn=:isbn ",
                          {"isbn": isbn}).fetchone()

        if book:
            KEY = os.getenv("KEY")
            isbn = book[0]

            try:
                res = requests.get("https://www.goodreads.com/"
                                   "book/review_counts.json",
                                   params={"key": KEY, "isbns": isbn},
                                   timeout=10)
                rating = True
            except requests.exceptions.RequestException:
                rating = False

            if rating:
                res = res.json()
                rating = res["books"][0]["average_rating"]
                goodreads_book_id = res["books"][0]["id"]

            reviews = db.execute("""SELECT review, rating, user_id, username
                                  FROM reviews JOIN users
                                  ON reviews.user_id=users.id
                                  WHERE isbn_id=:isbn""",
                                 {"isbn": isbn}).fetchall()

            user_has_reviewed = False

            for user in reviews:
                if user["user_id"] == session.get("user_id"):
                    user_has_reviewed = True

            return render_template("book.html",
                                   book=book,
                                   rating=rating,
                                   goodreads_book_id=goodreads_book_id,
                                   user=True,
                                   user_review=reviews,
                                   user_session=session.get("user_id"),
                                   user_has_reviewed=user_has_reviewed)
        else:
            return render_template("book.html",
                                   alert="Sorry could find this book,"
                                   " did you use search function?",
                                   user=True)
    else:
        rating, review = request.form["rating"], request.form["review"]

        if not rating or not review:
            return render_template("book.html", alert="Please fill all fields")

        try:
            db.execute("""INSERT INTO reviews (rating, review, isbn_id, user_id)
                    VALUES (:rating, :review, :isbn, :user_id)""",
                       {"rating": rating,
                        "review": review,
                        "isbn": isbn,
                        "user_id": session.get("user_id")
                        })

            db.commit()
        except DataError:
            return render_template("book.html", alert="Review is too long!")

        return redirect(request.url)


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register User """
    if request.method == "POST":
        valid, message = validate_register(request.form["username"],
                                           request.form["password"],
                                           request.form["password2"])

        if valid:
            username = request.form["username"]
            password = generate_password_hash(request.form["password"],
                                              method='pbkdf2:sha256',
                                              salt_length=8)

            """ Check for if is username already in database,
            If yes, SQLAlchemy throws Integrity Error """
            try:
                user_query = db.execute("""INSERT INTO users (username, password)
                                        VALUES (:username, :password)
                                        RETURNING id""",
                                        {"username": username,
                                         "password": password})
                db.commit()

                user_id = user_query.fetchone()[0]
                session["user_id"] = user_id
                return redirect(url_for("index"))
            except IntegrityError:
                return render_template("register.html",
                                       alert="Username already exists")
        else:
            return render_template("register.html", alert=message)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Login user, uses Validation function and query database
    for check users credentials """

    session.clear()

    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]
        valid, message = validate_login(username, password)

        if valid:
            user = db.execute("SELECT * FROM users WHERE username = :username",
                              {"username": username}).fetchone()

            if user:
                # Werkzeug function to safely compare passwords
                if check_password_hash(user[2], password):
                    session["user_id"] = user[0]
                    return redirect(url_for("index"))
                else:
                    # IF the password is invalid
                    return render_template("login.html",
                                           alert="""Invalid username
                                           or password""")

            else:
                # IF the username is invalid
                return render_template("login.html",
                                       alert="Invalid username or password")

        else:
            # IF invalid length or invalid input
            return render_template("login.html", alert=message)
    else:
        # IF GET method
        return render_template("login.html")


@app.route("/logout")
def logout():
    """ Remove user id from session """
    session.clear()
    return redirect(url_for("index"))
