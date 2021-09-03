import netifaces, ipaddress, os
from scapy.all import *
import scapy.all as scapy

TIMEOUT = 2
conf.verb = 0


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


def get_wild_card_mask():
    wildcard = ''
    interfaces = netifaces.interfaces()
    for i in interfaces:
        if i.__contains__('w'):
            netmask = str(netifaces.ifaddresses(i)[2][0]['netmask']).split('.')
            for octet in netmask:
                octet = 255 - int(octet)
                wildcard = wildcard + str(octet) + '.'
            return wildcard[:-1]
    return None


def get_ip_range():
    wild_card = get_wild_card_mask().split('.')
    ip_range = 1
    for i in wild_card:
        if int(i) == 0:
            continue
        else:
            ip_range *= int(i)
    return ip_range


def get_binary_ip_net_mask():
    return '.'.join([bin(int(x) + 256)[3:] for x in get_ip_address().split('.')]), '.'.join(
        [bin(int(x) + 256)[3:] for x in get_net_mask().split('.')])


def get_network_address():
    netaddr = []
    ip = get_ip_address().split('.')
    netmask = get_net_mask().split('.')
    j = 0
    for octet_ip in ip:
        while j < 4:
            netaddr.append(str(int(octet_ip) & int(netmask[j])))
            netaddr.append('.')
            break
        j += 1
    return ''.join(netaddr)[:-1]


def get_first_net_addr():
    return str(ipaddress.ip_address(get_network_address()) + 1)


def get_broadcast():
    interfaces = netifaces.interfaces()
    for i in interfaces:
        if i.__contains__('w'):
            return netifaces.ifaddresses(i)[2][0]['broadcast']
    return None


def scan(ip):
    arp_req_frame = scapy.ARP(pdst=ip)

    broadcast_ether_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

    answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout=0.1, verbose=False)[0]
    result = []
    for i in range(0, len(answered_list)):
        client_dict = {"ip": answered_list[i][1].psrc, "mac": answered_list[i][1].hwsrc}
        result.append(client_dict)

    return result


def net_scan():
    result = dict()
    dest_addr = get_first_net_addr()
    for i in range(get_ip_range()):
        if len(scan(dest_addr)) != 0:
            result[dest_addr] = scan(dest_addr)
        else:
            result[dest_addr] = None
        dest_addr = str(ipaddress.ip_address(dest_addr) + 1)
    return result


