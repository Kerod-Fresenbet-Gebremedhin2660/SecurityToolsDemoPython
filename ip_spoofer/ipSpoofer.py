import netifaces
from scapy.all import *
from scapy.layers.inet import IP, TCP


def get_ip_address_alt() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def get_ip_address():
    interfaces = netifaces.interfaces()
    for i in interfaces:
        if i.__contains__('w'):
            return netifaces.ifaddresses(i)[2][0]['addr']
    return None


def get_net_mask():
    interfaces = netifaces.interfaces()
    for i in interfaces:
        if i.__contains__('w'):
            return netifaces.ifaddresses(i)[2][0]['netmask']
    return None


def check_ip_address():
    return get_ip_address() == get_ip_address_alt()


def spoof_address(src_ipaddr, dest_ipaddr):
    spoofed_packet = IP(src_ipaddr, dest_ipaddr) / TCP



