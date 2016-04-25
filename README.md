# flasktaskr
going along tutorial to learn flask

To add connection / fk to users: use backref in models.py
i.e., to tie the fk "user_id" in messages (or tasks) table to full user name, use this:
  messages = db.relationship('Message', backref='poster')
  db.relationship ties user_id to backref name of 'poster'

TO RUN:
#DO This
