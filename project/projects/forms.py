 #project/projects/forms.py

from flask_wtf import Form
from wtforms import DateField, IntegerField, TextAreaField, StringField

from wtforms.validators import DataRequired

class AddProjectForm(Form):
    project_id = IntegerField()
    project_name = StringField('Project Name')
    project_desc = TextAreaField('Project Desc', validators=[DataRequired()])
    status = IntegerField('Status')
