from flask import Flask, render_template, flash, make_response, request, redirect
from flask_bootstrap import Bootstrap
from config import Config
from forms import OSForm, OSForm2, OSForm3, OSForm4, OSForm5, OSForm6
from ip_spoofer.ipSpoofer import get_spoofed_address, get_ip_address, ping_with_spoofed_address
from os_detection.detectOSNmap import DetectOS
from os_detection.detectOSScapy import DetectOS as DOS2
from email_harvester.emailHarvester import harvest_emails, refiner_links
from port_scan.portScanner import known_ports_scan, all_ports_scan
from network_scanner.networkScanner import net_scan
from meta_data_analyzer.pdf_analyzer import pdf_analyze, pdf_analyze_file
from turbo_flask import Turbo
from werkzeug.utils import secure_filename
import os, pickle

UPLOAD_FOLDER = '/home/kpc/PycharmProjects/security-proj-1/uploads'
ALLOWED_EXTENSIONS = {'pdf'}


app = Flask(__name__)
turbo = Turbo(app)
app.config.from_object(Config)
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = OSForm()
    osinfo = None
    if form.validate_on_submit():
        flash('Processing Your Request')
        ip = form.ip.data
        osinfo = DetectOS(ip)
    return render_template("index.html", form=form, osinfo=osinfo)


@app.route('/icmp', methods=['GET', 'POST'])
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
            if ip is not None:
                result = known_ports_scan(str(ip))
            else:
                result = known_ports_scan()
                print(result)
        elif scan_type == 2:
            if ip is not None:
                result = all_ports_scan(str(ip))
            else:
                result = all_ports_scan()
        if turbo.can_stream():
            turbo.append(render_template('portscan.html', form=form, result=result))

    return render_template("portscan.html", form=form, result=result)


@app.route('/spoofer', methods=['GET', 'POST'])
def spoofer():
    form = OSForm3()
    result = None
    ip_real_spoofed = dict()
    ip_real_spoofed['ip_real'] = get_ip_address()
    with open("spoofed_addr.pkl", "wb") as f:
        pickle.dump(get_spoofed_address(), f)
    ip_spoofed = pickle.load(open("spoofed_addr.pkl", "rb"))
    ip_real_spoofed['spoofed_ip_address'] = pickle.load(open("spoofed_addr.pkl", "rb"))
    if form.validate_on_submit():
        flash('Processing Your Request')
        ip = form.ip.data
        result = ping_with_spoofed_address(dest_addr=str(ip), spoofed_addr=ip_real_spoofed['spoofed_ip_address'])
    return render_template('spoofer.html', ipr=ip_real_spoofed['ip_real'], sip=ip_real_spoofed['spoofed_ip_address'], form=form, result=result)


@app.route('/networkscan', methods=['GET', 'POST'])
def netscan():
    form = OSForm5()
    result = None
    if form.validate_on_submit():
        result = net_scan()
    return render_template('networkscan.html', form=form, result=result)


@app.route('/emailharvester', methods=['GET', 'POST'])
def harvestemails():
    form = OSForm4()
    result = None
    if form.validate_on_submit():
        flash('Processing Your Request')
        url = form.url.data
        result = harvest_emails(url)
        if len(result) == 0:
            result = None
            flash('Connection Error Most Likely, No Results could be fetched')
    return render_template("emailharvester.html", form=form, result=result)


@app.route('/linkharvester', methods=['GET', 'POST'])
def harvestlinks():
    form = OSForm4()
    result = None
    if form.validate_on_submit():
        flash('Processing Your Request')
        url = form.url.data
        result = refiner_links(url)
    return render_template("linkharvester.html", form=form, result=result)


@app.route('/pdfanalysis', methods=['GET','POST'])
def pdfanalysis():
    form = OSForm6()
    pdf_data = None
    if form.validate_on_submit():
        file = form.file.data
        print(file)
        file_name = secure_filename(file)
        file.save(os.path.join(
            app.instance_path, 'uploads', file_name
        ))
        pdf_data = pdf_analyze_file(os.path.abspath(file))
        print("PDF Data: ",pdf_data)
    return render_template("pdfanalysis.html", form=form, data=pdf_data)


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
