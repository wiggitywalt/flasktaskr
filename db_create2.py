#db_create2.py

from project import db

db.create_all()

db.session.commit()
