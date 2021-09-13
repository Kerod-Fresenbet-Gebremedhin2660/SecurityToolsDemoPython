from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, IPAddress, URL
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, DOCUMENTS


class OSFPForm(FlaskForm):
    ip = StringField("IP Address :   ", validators=[DataRequired(), IPAddress()])
    submit = SubmitField('Detect OS')


class PortScannerForm(FlaskForm):
    ip = StringField("IP Address : ", validators=[IPAddress()])
    scanType = SelectField(label="Type of Scan : ", choices=[(1, 'Known Ports'), (2, 'All Ports')])
    submit = SubmitField('Scan Ports')


class SpooferForm(FlaskForm):
    ip = StringField("Destination IP Address :   ", validators=[DataRequired(), IPAddress()])
    submit = SubmitField('Send Spoofed Packet')


class HarvestingForm(FlaskForm):
    url = StringField("URL : ", validators=[DataRequired(), URL()])
    submit = SubmitField('Harvest')


class NetworkScanForm(FlaskForm):
    submit = SubmitField('Scan Network')


class FileUploadForm(FlaskForm):
    file = FileField('Upload PDF',
                     validators=[FileRequired(), FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDF\'s or Images only')])
    submit = SubmitField('Analyze')
