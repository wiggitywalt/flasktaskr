#project/users/views.py

###############
### imports ###
###############

from functools import wraps
from flask import flash, redirect, render_template, \
  request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError

from .forms import RegisterForm, LoginForm
from project import db, bcrypt
from project.models import User

###############
### config  ###
###############

users_blueprint = Blueprint('users', __name__)


###############
### helpers ###
###############

def login_required(test):
  @wraps(test)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return test(*args, **kwargs)
    else:
      flash('You need to login first, nimrod.')
      return redirect(url_for('users.login'))
  return wrap

###############
### routes  ###
###############

@users_blueprint.route('/all_users/')
@login_required
def allusers():
  all_users = db.session.query(User).all()
  return render_template(
    'all_users.html',
    all_users=all_users,
    username = session['user_name']
  )

@users_blueprint.route('/logout/')
@login_required
def logout():
  session.pop('logged_in', None)
  session.pop('user_id', None)
  session.pop('role', None)
  session.pop('user_name', None)

  flash('Goodbye')
  return redirect(url_for('users.login'))

@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
  error = None
  form = LoginForm(request.form)
  if request.method == 'POST':
    if form.validate_on_submit():
      user = User.query.filter_by(name=request.form['name']).first()
      if user is not None and bcrypt.check_password_hash(user.password,request.form['password']):
        session['logged_in'] = True
        session['user_id'] = user.id
        session['role'] = user.role
        session['user_name'] = user.name
        login_msg = 'Welcome, ' + user.name
        flash(login_msg)
        return redirect(url_for('tasks.tasks'))
      else:
        error = 'Invalid credentials.'
  return render_template('login.html', form=form, error=error)

@users_blueprint.route('/register/', methods=['GET','POST'])
def register():
  error=None
  form = RegisterForm(request.form)
  if request.method == 'POST':
    if form.validate_on_submit():
      new_user = User(
        form.name.data,
        form.email.data,
        bcrypt.generate_password_hash(form.password.data),
        )
      try:
        db.session.add(new_user)
        db.session.commit()
        flash('Thanks for registering. Login!')
        return redirect(url_for('users.login'))
      except IntegrityError:
        error = 'That username or email exists.'
        return render_template('register.html',form=form, error=error)
  return render_template('register.html', form=form, error=error)































