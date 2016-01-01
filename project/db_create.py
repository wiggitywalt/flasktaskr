#project/db_create.py
from views import db
from models import User
from datetime import date

#create the db and db table
db.create_all()

#insert data
# db.session.add(Task("Finish the tutorial", date(2015,12,27), 10, 1))
# db.session.add(Task("Finish Real Python", date(2015,12,28), 10, 1))

db.session.commit()

# import sqlite3

# from _config import DATABASE_PATH

# with sqlite3.connect(DATABASE_PATH) as connection:
#   #get a cursor object used to execute SQL commands
#   c = connection.cursor()

#   # create the table
#   c.execute(""" CREATE TABLE tasks(task_id INTEGER PRIMARY KEY
#     AUTOINCREMENT,
#     name TEXT NOT NULL, due_date TEXT NOT NULL, priority
#     INTEGER NOT NULL,
#     status INTEGER NOT NULL)""")

#   # dummy data
#   c.execute(
#     'INSERT INTO tasks(name,due_date,priority,status)'
#     'VALUES("FINISH this here tutorial", "12/25/2015", 10, 1)'
#     )

#   c.execute(
#     'INSERT INTO tasks(name,due_date,priority,status)'
#     'VALUES("FINISH REal Python Course 2", "12/25/2015", 10, 1)'
#     )


