from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, IPAddress, NumberRange


class OSForm(FlaskForm):
    ip = StringField("IP Address :   ", validators=[DataRequired(), IPAddress()])
    submit = SubmitField('Detect OS')


class OSForm2(FlaskForm):
    ip = StringField("IP Address : ", validators=[DataRequired(), IPAddress()])
    scanType = SelectField(label="Type of Scan", choices=[(1, 'Known Ports'), (2, 'All Ports')])
    submit = SubmitField('Scan Ports')
