# Project 1

## Description:
This application let's you import books from books.csv file to your heroku postgres database by import.py. On the website registered user can search by ISBN, name of the book and authors name. If app matches book from db, user can write review (one per book). It also fetches Goodreads rating if aviable. Developers can use api route to get response in json format about the book requested by ISBN number. 

## How to run:

First install all needed packages:

```
pip install requirements.txt
```

The url you can find in your Heroku postgres database
Set up in env file:

```
FLASK_APP=application.py
DATABASE_URL="Your postgress url"
KEY="Your postgres key"
```
Install requirements:

```
pip install requirements.txt
```

Import books to your database:

```
python import.py
```

To run:

```
flask run
```

## Requirements

- [x] Registration: Users should be able to register for your website, providing (at minimum) a username and password.
- [x] Login: Users, once registered, should be able to log in to your website with their username and password.
- [x] Logout: Logged in users should be able to log out of the site.
- [x] Import: Provided for you in this project is a file called books.csv, which is a spreadsheet in CSV format of 5000 different books. Each one has an ISBN number, a title, an author, and a publication year. In a Python file called import.py separate from your web application, write a program that will take the books and import them into your PostgreSQL database. You will first need to decide what table(s) to create, what columns those tables should have, and how they should relate to one another. Run this program by running python3 import.py to import the books into your database, and submit this program with the rest of your project code.
- [x] Search: Once a user has logged in, they should be taken to a page where they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!
- [x] Book Page: When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.
- [x] Review Submission: On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.
- [x] Goodreads Review Data: On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.
- [x] API Access: If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON should follow the format:
