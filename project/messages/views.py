# project/messages/views.py

import datetime
from functools import wraps
from flask import flash, redirect, render_template, \
    request, session, url_for, Blueprint

# from .forms import AddTaskForm
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

@messages_blueprint.route('/allmessages/')
@login_required
def allmessages():
  all_messages = db.session.query(Message).all()
  return render_template(
    'messages.html',
    entries=all_messages,
    username = session['user_name']
  )




































