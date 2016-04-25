#project/api/views.py

from functools import wraps
from flask import flash, redirect, jsonify, \
    session, url_for, Blueprint, make_response

from project import db
from project.models import Task
from project.models import Message

################
#### config ####
################

api_blueprint = Blueprint('api', __name__)

#################
#### helpers ####
#################

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

#################
#### routes #####
#################

##tasks##
@api_blueprint.route('/api/v1/tasks/')
def api_tasks():
  results = db.session.query(Task).limit(10).offset(0).all()
  json_results = []
  for result in results:
    data = {
      'task_id': result.task_id,
      'task_name': result.name,
      'due date': str(result.due_date),
      'priority': result.priority,
      'posted date': str(result.posted_date),
      'status': result.status,
      'user id': result.user_id
      }
    json_results.append(data)
  return jsonify(items=json_results)

@api_blueprint.route('/api/v1/tasks/<int:task_id>')
def task(task_id):
  result = db.session.query(Task).filter_by(task_id=task_id).first()
  if result:
    result = {
    'task_id': result.task_id,
    'task_name': result.name,
    'due date': str(result.due_date),
    'priority': result.priority,
    'posted date': str(result.posted_date),
    'status': result.status,
    'user id': result.user_id
    }
    code = 200

  else:
    result = {"error" : "Element does not exist"}
    code = 404
  return make_response(jsonify(result), code)

##messages##
@api_blueprint.route('/api/v1/messages/')
def api_messages():
  results = db.session.query(Message).offset(0).all()
  json_results = []
  for result in results:
    data = {
      'message_id': result.message_id,
      'message': result.message,
      'posted date': str(result.posted_date),
      'status' : str(result.status),
      'user id': result.user_id
      }
    json_results.append(data)
  return jsonify(items=json_results)

@api_blueprint.route('/api/v1/messages/<int:message_id>')
def message(message_id):
  result = db.session.query(Message).filter_by(message_id=message_id).first()
  if result:
    result = {
      'message_id': result.message_id,
      'message': result.message,
      'posted date': str(result.posted_date),
      'status': result.status,
      'user id': result.user_id
    }
    code = 200
  else:
    result = {"error" : "Element does not exist"}
    code = 404
  return make_response(jsonify(result), code)
