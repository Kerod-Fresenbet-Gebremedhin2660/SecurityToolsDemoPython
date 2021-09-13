# from socket import getservbyport
# import netifaces, threading, socket
#
# def get_ip_address():
#     interfaces = netifaces.interfaces()
#     for i in interfaces:
#         if i.__contains__('w'):
#             return netifaces.ifaddresses(i)[2][0]['addr']
#     return None
#
#
# def all_ports_scan(target=get_ip_address(), port_range):
#     ports = dict()
#     for port in range(0, port_range):
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.settimeout(1)
#         conn = s.connect_ex((target, port))
#         try:
#             if conn == 0:
#                 ports[getservbyport(port)] = True
#             else:
#                 ports[getservbyport(port)] = False
#         except OSError as e:
#             continue
#         finally:
#             s.close()
#     return ports
#
#
# def threaded_scan():
#     thread1 = threading.Thread(name="thread1", target=all_ports_scan, args=(16000))
#     thread2 = threading.Thread(name="thread2", target=all_ports_scan, args=(32000))
#     thread3 = threading.Thread(name="thread3", target=all_ports_scan, args=())
#     thread4 = threading.Thread(name="thread4", target=all_ports_scan, args=())
#
