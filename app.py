from flask import Flask, render_template, flash, make_response
from flask_bootstrap import Bootstrap
from detectOS import DetectOS
from config import Config
from forms import OSForm

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index() -> "html":
    form = OSForm()
    osinfo = None
    if form.validate_on_submit():
        flash('Processing Your Request')
        ip = form.ip.data
        osinfo = DetectOS(ip)
    return render_template("index.html", form=form, osinfo=osinfo)


@app.route('/aboutus')
def aboutus() -> "html":
    return render_template("aboutus.html")


@app.errorhandler(404)
def not_found(error) -> "html":
    resp = make_response(render_template('notfound.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


if __name__ == '__main__':
    app.run(debug=True)
