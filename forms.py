from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, IPAddress, URL


class OSForm(FlaskForm):
    ip = StringField("IP Address :   ", validators=[DataRequired(), IPAddress()])
    submit = SubmitField('Detect OS')


class OSForm2(FlaskForm):
    ip = StringField("IP Address : ", validators=[DataRequired(), IPAddress()])
    scanType = SelectField(label="Type of Scan : ", choices=[(1, 'Known Ports'), (2, 'All Ports')])
    submit = SubmitField('Scan Ports')


class OSForm3(FlaskForm):
    ip = StringField("Destination IP Address :   ", validators=[DataRequired(), IPAddress()])
    submit = SubmitField('Send Spoofed Packet')


class OSForm4(FlaskForm):
    url = StringField("URL : ", validators=[DataRequired(), URL()])
    submit = SubmitField('Harvest')


class OSForm5(FlaskForm):
    submit = SubmitField('Scan Network')