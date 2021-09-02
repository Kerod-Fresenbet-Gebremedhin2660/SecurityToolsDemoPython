from dominate.tags import img
from flask import Flask, render_template, flash, make_response
from flask_bootstrap import Bootstrap
from flask_nav import Nav, register_renderer
from flask_nav.elements import *
from navbar import JustDivRenderer

from config import Config
from forms import OSForm, OSForm2, OSForm3
from ip_spoofer.ipSpoofer import get_spoofed_address, get_ip_address, ping_with_spoofed_address
from os_detection.detectOSNmap import DetectOS
from os_detection.detectOSScapy import DetectOS as DOS2
from port_scan.portScanner import known_ports_scan, all_ports_scan

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)

nav = Nav()

logo = img(src="../static/favicon/favicon-32x32.png")

navbar = Navbar(
    logo,
    View('OS f 1', 'index'),
    View('OS f 2', 'scapy'),
    View('Port Scan', 'portscan'),
    View('Spoofer', 'spoofer'),
    View('Network Scan', 'netscan'),
    View('Email Harvester', 'harvestemails'),
    View('About Us', 'aboutus'),
)
register_renderer(app, 'just_div', JustDivRenderer)
nav.register_element('top', navbar)
nav.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = OSForm()
    osinfo = None
    if form.validate_on_submit():
        flash('Processing Your Request')
        ip = form.ip.data
        osinfo = DetectOS(ip)
    return render_template("index.html", form=form, osinfo=osinfo)


@app.route('/scapy', methods=['GET', 'POST'])
def scapy():
    form = OSForm()
    osname = None
    if form.validate_on_submit():
        flash('Processing Your Request')
        ip = form.ip.data
        osname = DOS2(ip)
        if osname is None:
            osname = "Could Not Identify"
        print("THE OS NAME IS: ", osname)
    return render_template("scapy.html", form=form, osname=osname)


@app.route('/portscan', methods=['GET', 'POST'])
def portscan():
    form = OSForm2()
    result = None
    if form.validate_on_submit():
        flash('Processing Your Request')
        ip = form.ip.data
        scan_type = int(form.scanType.data)
        if scan_type == 1:
            result = known_ports_scan(str(ip))
        elif scan_type == 2:
            result = all_ports_scan(str(ip))
    return render_template("portscan.html", form=form, result=result)


@app.route('/spoofer')
def spoofer():
    form = OSForm3()
    result = None
    ip_real = get_ip_address()
    spoofed_ip_address = get_spoofed_address()
    if form.validate_on_submit():
        flash('Processing Your Request')
        ip = form.ip.data
        result = ping_with_spoofed_address(str(ip))
    return render_template('spoofer.html', ipr=ip_real, sip=spoofed_ip_address, form=form, result=result)


@app.route('/networkscan')
def netscan():
    return render_template('networkscan.html')


@app.route('/emailharvester')
def harvestemails():
    return render_template("emailharvester.html")


@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('404.html'), 404)
    return resp


@app.errorhandler(500)
def server_error(error):
    resp = make_response(render_template('404.html'), 404)
    return resp


if __name__ == '__main__':
    app.run(debug=True)
