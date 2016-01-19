# project/__init__.py

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
import datetime


app = Flask(__name__)
app.config.from_pyfile('_config.py')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

#import blueprints
from project.users.views import users_blueprint
from project.tasks.views import tasks_blueprint
from project.api.views import api_blueprint
from project.messages.views import messages_blueprint

#register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(messages_blueprint)

#error http codes (404 and 500)
@app.errorhandler(404)
def not_found(error):
  now = datetime.datetime.now()
  r = request.url
  with open('error.log', 'a') as f:
    current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
    f.write("\n404 error at {}: {}".format(current_timestamp, r))
  return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
  now = datetime.datetime.now()
  r = request.url
  with open('error.log', 'a') as f:
    current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
    f.write("\n500 error at {}: {}".format(current_timestamp, r))
  return render_template('500.html'), 500
