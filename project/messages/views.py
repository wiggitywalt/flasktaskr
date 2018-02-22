# project/messages/views.py

import datetime
from functools import wraps
from flask import flash, redirect, render_template, request, session, url_for, Blueprint

from sqlalchemy.sql import table, column
from .forms import AddMessageForm

from project import db
from project.models import Message

##############
### config ###
##############

messages_blueprint = Blueprint('messages', __name__)

###############
### helpers ###
###############

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
          return test(*args, **kwargs)
        else:
          flash('You need to login first.')
          return redirect(url_for('users.login'))
    return wrap

###############
### routes ####
###############

@messages_blueprint.route('/')
def allmessages():
    form = AddMessageForm(request.form)
    all_messages = db.session.query(Message).order_by(Message.message_type.desc()).all()
    return render_template(
      'messages.html',
      entries=all_messages,
      form = form
    )

@messages_blueprint.route('/newmessage/', methods=['GET','POST'])
@login_required
def new_message():
    error = None
    form = AddMessageForm(request.form)
    if request.method == 'POST':
      if form.validate_on_submit():
        new_message = Message(
          form.message.data,
          form.message_type.data,
          session['user_id']
        )
        db.session.add(new_message)
        db.session.commit()
        flash('New entry was successful.')
        return redirect(url_for('messages.allmessages'))
