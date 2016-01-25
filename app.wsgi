path = '/home/wiggitywalt/flasktaskr'

if path not in sys.path:
  sys.path.append(path)


from project import app as application
