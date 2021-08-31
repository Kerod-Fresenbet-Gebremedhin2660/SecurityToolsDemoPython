from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, IPAddress


class OSForm(FlaskForm):
    ip = StringField("IP Address :   ", validators=[DataRequired(), IPAddress()])
    submit = SubmitField('Detect OS')

