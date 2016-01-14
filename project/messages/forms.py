 #project/messages/forms.py

from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, \
    SelectField

from wtforms.validators import DataRequired

class AddMessageForm(Form):
  message_id = IntegerField()
  message = StringField('Blog message', validators=[DataRequired()])
  posted_date = DateField(
    'Date Due (mm/dd/yyyy)',
    validators=[DataRequired()], format='%m/%d/%Y'
    )
  status = IntegerField('Status')

