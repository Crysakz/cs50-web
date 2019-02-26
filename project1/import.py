import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    '''Import data to Database'''
    file = open("project1/books.csv", newline="")
    reader = csv.reader(file)

    header = next(reader) #skip first row

    
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", 
        {"isbn": isbn, "title": title, "author": author, "year": int(year)})

    db.commit() #important! For inserting is needed to commit the change to the database

if __name__ == "__main__":
    main()