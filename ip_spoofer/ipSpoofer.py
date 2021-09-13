import ipaddress
import netifaces
from random import randint

from scapy.all import *
from scapy.layers.inet import IP


def get_ip_address_alt():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0] or None


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


def get_broadcast():
    interfaces = netifaces.interfaces()
    for i in interfaces:
        if i.__contains__('w'):
            return netifaces.ifaddresses(i)[2][0]['broadcast']
    return None


def check_ip_address():
    return get_ip_address() == get_ip_address_alt()


def get_spoofed_address():
    ip = ipaddress.ip_address(get_broadcast())
    return str(ip + randint(2, 254))


def ping_with_spoofed_address(dest_addr, spoofed_addr):
    print("The spoofed address sent to the function is: ", spoofed_addr)
    network = IP(src=spoofed_addr, dst=dest_addr)
    return srloop(network, timeout=12)
