from scapy.all import *
from scapy.layers.inet import IP, TCP, ICMP
import ipaddress, netifaces, random

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
    return str(ip + random.randint(2, 254))


def ping_with_spoofed_address(dest_ipaddr, spoofed_addr=None):
    print("The spoofed address sent from the route is: ", spoofed_addr)
    addr_spoofed = spoofed_addr or get_spoofed_address()
    network = IP(src=addr_spoofed, dst=dest_ipaddr)
    return srloop(network, timeout=12)


