#project/test.py

import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):

  ########################
  ###setup and teardown###
  ########################

  #executed prior to each test
  def setUp(self):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(basedir, TEST_DB)
    self.app = app.test_client()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()


  def test_form_is_present_on_login_page(self):
    response = self.app.get('/')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Please sign in to access your task list', response.data)

  def login(self, name, password):
    return self.app.post('/',data=dict(name=name, password=password), follow_redirects=True)

  def test_users_cannot_login_unless_registered(self):
    response = self.login('foo', 'bar')
    self.assertIn(b'Invalid user name and or password, bitch')

  def register(self, name, email, password, confirm):
    return self.app.post(
      'register/',
      data=dict(name=name, email=email, password=password,
        confirm=confirm),
        follow_redirects=True
      )

  def test_users_can_login(self):
    self.register('walters', 'walter@me.com', 'python', 'python')
    response = self.login('walters','python')
    self.assertIn('welcome!', response.data)

  def test_invalid_form_data(self):
    self.register('walters', 'walter@me.com', 'python', 'python')
    response = self.login('alert("alert!");', 'foo')
    self.assertIn(b'invalid shit', response.data)

    # def test_users_can_register(self):
    #   new_user = User("walters", "walt@me.com", "walterskitty")
    #   db.session.add(new_user)
    #   db.session.commit()
    #   test = db.session.query(User).all()
    #   for t in test:
    #     t.name
    #   assert t.name != "walters"

    # def test_user_setup(self):
    #   new_user = User("walty", "walt.kimbrough@email.org", "waltybits")
    #   db.session.add(new_user)
    #   db.session.commit()

if __name__ == "__main__":
  unittest.main()
