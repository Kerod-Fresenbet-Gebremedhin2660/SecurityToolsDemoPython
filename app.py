import os
import pickle

from flask import Flask, render_template, flash, make_response
from flask_bootstrap import Bootstrap
from config import Config
from email_harvester.emailHarvester import harvest_emails, refiner_links
from forms import OSFPForm, PortScannerForm, SpooferForm, HarvestingForm, NetworkScanForm, FileUploadForm
from ip_spoofer.ipSpoofer import get_spoofed_address, get_ip_address, ping_with_spoofed_address
from meta_data_analyzer.pdf_analyzer import pdf_analyze_file
from meta_data_analyzer.image_analyzer import image_analyzer
from network_scanner.networkScanner import net_scan
from os_detection.detectOSNmap import DetectOS
from os_detection.detectOSScapy import DetectOS as DOS2
from port_scan.portScanner import known_ports_scan, all_ports_scan
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = OSFPForm()
    osinfo = None
    if form.validate_on_submit():
        ip = form.ip.data
        osinfo = DetectOS(ip)
    return render_template("index.html", form=form, osinfo=osinfo)


@app.route('/icmp', methods=['GET', 'POST'])
def scapy():
    form = OSFPForm()
    osname = None
    if form.validate_on_submit():

        ip = form.ip.data
        osname = DOS2(ip)
        if osname is None:
            osname = "Could Not Identify"
        print("THE OS NAME IS: ", osname)
    return render_template("scapy.html", form=form, osname=osname)


@app.route('/portscan', methods=['GET', 'POST'])
def portscan():
    form = PortScannerForm()
    result = None
    if form.validate_on_submit():

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
    return render_template("portscan.html", form=form, result=result)


@app.route('/spoofer', methods=['GET', 'POST'])
def spoofer():
    form = SpooferForm()
    result = None
    ip_dict = dict()
    ip_dict['ip_real'] = get_ip_address()

    with open("spoofed_addr.pkl", "wb") as f:
        pickle.dump(get_spoofed_address(), f)

    ip_dict['spoofed_ip_address'] = pickle.load(open("spoofed_addr.pkl", "rb"))

    spoofed_net_addr: str = ip_dict['spoofed_ip_address']
    spoofed_net_addr = spoofed_net_addr[0:10]

    if form.validate_on_submit():
        ip = form.ip.data
        print("The spoofed ip inside the view function: ", ip_dict['spoofed_ip_address'])
        result = ping_with_spoofed_address(dest_addr=str(ip), spoofed_addr=ip_dict['spoofed_ip_address'])
    return render_template('spoofer.html', ipr=ip_dict['ip_real'], sip=ip_dict['spoofed_ip_address'],
                           form=form, spoofed_net_addr=spoofed_net_addr, result=result)


@app.route('/networkscan', methods=['GET', 'POST'])
def netscan():
    form = NetworkScanForm()
    result = None
    if form.validate_on_submit():
        result = net_scan()
    return render_template('networkscan.html', form=form, result=result)


@app.route('/emailharvester', methods=['GET', 'POST'])
def harvestemails():
    form = HarvestingForm()
    result = None
    if form.validate_on_submit():

        url = form.url.data
        result = harvest_emails(url)
        if len(result) == 0:
            result = None

    return render_template("emailharvester.html", form=form, result=result)


@app.route('/linkharvester', methods=['GET', 'POST'])
def harvestlinks():
    form = HarvestingForm()
    result = None
    if form.validate_on_submit():
        url = form.url.data
        result = refiner_links(url)
    return render_template("linkharvester.html", form=form, result=result)


@app.route('/pdfanalysis', methods=['GET', 'POST'])
def pdfanalysis():
    form = FileUploadForm()
    pdf_data = None
    if form.validate_on_submit():
        file = form.file.data
        file_name = secure_filename(file.filename)
        file.save(os.path.join(
            app.root_path, 'uploads/', file_name
        ))
        pdf_data = pdf_analyze_file('uploads/' + file_name)
    return render_template("pdfanalysis.html", form=form, data=pdf_data)


@app.route('/imageanalysis', methods=['GET', 'POST'])
def imageanalysis():
    form = FileUploadForm()
    image_data = None
    if form.validate_on_submit():
        file = form.file.data
        file_name = secure_filename(file.filename)
        file.save(os.path.join(
            app.root_path, 'imageuploads/', file_name
        ))
        image_data = image_analyzer(app.root_path + '/imageuploads/' + file_name)
    return render_template("pdfanalysis.html", form=form, data=image_data)


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
