import socket
from socket import getservbyport
import netifaces


def get_ip_address():
    interfaces = netifaces.interfaces()
    for i in interfaces:
        if i.__contains__('w'):
            return netifaces.ifaddresses(i)[2][0]['addr']
    return None


def all_ports_scan(target=get_ip_address(), port_range=65535):
    ports = dict()
    for port in range(0, port_range):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        conn = s.connect_ex((target, port))
        try:
            if conn == 0:
                ports[getservbyport(port)] = True
            else:
                ports[getservbyport(port)] = False
        except OSError as e:
            continue
        finally:
            s.close()
    return ports


def known_ports_scan(target=get_ip_address()):
    ports = dict()
    for port_num, port in get_known_ports().items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        conn = s.connect_ex((target, port_num))
        try:
            if conn == 0:
                ports[getservbyport(port_num)] = True
            else:
                ports[getservbyport(port_num)] = False
        except OSError as e:
            continue
        finally:
            s.close()
    return ports


def get_known_ports():
    known_ports = dict()
    for i in range(1024):
        try:
            known_ports[i] = getservbyport(i)
        except OSError as e:
            continue
    return known_ports

