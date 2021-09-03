from scapy.all import *
from scapy.layers.inet import IP, TCP, ICMP
import ipaddress, netifaces, random
from scapy.layers.l2 import Ether


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


def ping_with_spoofed_address(dest_ipaddr):
    spoofed_addr = get_spoofed_address()

    ethernet = Ether()
    network = IP(src=spoofed_addr, dst=dest_ipaddr)
    transport = ICMP()
    pkt = ethernet / network / transport

    return srloop(pkt, iface=netifaces.interfaces()[-1])


