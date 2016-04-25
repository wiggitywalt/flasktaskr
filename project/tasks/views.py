# project/tasks/views.py

import datetime
from functools import wraps
from flask import flash, redirect, render_template, \
    request, session, url_for, Blueprint

from .forms import AddTaskForm
from project import db
from project.models import Task

##############
### config ###
##############

tasks_blueprint = Blueprint('tasks', __name__)

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


def get_tasks(status):
  return db.session.query(Task).filter_by(status=status).order_by(Task.due_date.asc())

def open_tasks():
  return db.session.query(Task).filter_by(status="1").order_by(Task.due_date.asc())

def closed_tasks():
  return db.session.query(Task).filter_by(status="0").order_by(Task.due_date.asc())
###############
### routes ####
###############

@tasks_blueprint.route('/tasks/')
@login_required
def tasks():
  form = AddTaskForm(request.form)
  open_tasks = db.session.query(Task).filter_by(status="1").order_by(Task.due_date.asc())
  closed_tasks = db.session.query(Task).filter_by(status="0").order_by(Task.due_date.asc())
  return render_template(
    'tasks.html',
    form=form,
    open_tasks=open_tasks,
    closed_tasks=closed_tasks,
    username = session['user_name']
  )

@tasks_blueprint.route('/add/', methods=['GET', 'POST'])
@login_required
def new_task():
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

  return render_template(
    'tasks.html',
    form=form,
    error=error,
    open_tasks=get_tasks('1'),
    closed_tasks=get_tasks('0')
    )



@tasks_blueprint.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
  new_id = task_id
  task = db.session.query(Task).filter_by(task_id=new_id)
  if session['user_id'] == task.first().user_id or session['role'] == 'admin':
    task.update({"status": "0"})
    db.session.commit()
    flash("The task is complete. Nicely done.")
    return redirect(url_for('tasks.tasks'))
  else:
    flash("Unauthorized. You can only update your tasks. Duh.")
    return redirect(url_for('tasks.tasks'))

@tasks_blueprint.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
  new_id = task_id
  task = db.session.query(Task).filter_by(task_id=new_id)
  if session['user_id'] == task.first().user_id or session['role'] == "admin":
    task.delete()
    db.session.commit()
    flash("The task was deleted.")
    return redirect(url_for('tasks.tasks'))
  else:
    flash("You can only delete your tasks. Nimrod.")
    return redirect(url_for('tasks.tasks'))
