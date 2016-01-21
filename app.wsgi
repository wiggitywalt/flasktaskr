path = '/home/wiggitywalt/flasktaskr'

if path not in sys.path:
  sys.path.append(path)


from flask_app import app as application
