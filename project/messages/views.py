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

@messages_blueprint.route('/')
def allmessages():
  all_messages = db.session.query(Message).all()
  return render_template(
    'messages.html',
    entries=all_messages
  )

@messages_blueprint.route('/newmessage/')
@login_required
def new_message():
  error = None
  form = AddTaskForm(request.form)
  if request.method == 'POST':
    if form.validate_on_submit():
      new_task = Task(
        form.name.data,
        form.due_date.data,
        form.priority.data,
        datetime.datetime.utcnow(),
        '1',
        session['user_id']
      )
      db.session.add(new_task)
      db.session.commit()
      flash('New entry was successful.')
      return redirect(url_for('tasks.tasks'))
