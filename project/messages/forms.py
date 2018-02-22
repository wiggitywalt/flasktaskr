 #project/messages/forms.py

from flask_wtf import Form
from wtforms import DateField, IntegerField, TextAreaField, StringField

from wtforms.validators import DataRequired

class AddMessageForm(Form):
    message_id = IntegerField()
    message_type = StringField('Task Name')
    message = TextAreaField('Blog message', validators=[DataRequired()])
    
    status = IntegerField('Status')
