# from socket import getservbyport
# from typing import Tuple
# import netifaces
# import socket
# from threading import Thread
#
#
# class ThreadWithReturnValue(Thread):
#     def __init__(self, group=None, target=None, name=None,
#                  args=(), kwargs={}, Verbose=None):
#         Thread.__init__(self, group, target, name, args, kwargs)
#         self._return = None
#
#     def run(self):
#         print(type(self._target))
#         if self._target is not None:
#             self._return = self._target(*self._args,
#                                         **self._kwargs)
#
#     def join(self, *args):
#         Thread.join(self, *args)
#         return self._return
#
#
# def get_ip_address():
#     interfaces = netifaces.interfaces()
#     for i in interfaces:
#         if i.__contains__('w'):
#             return netifaces.ifaddresses(i)[2][0]['addr']
#     return None
#
#
# def all_ports_scan(target: str = get_ip_address(), port_range: Tuple = (0, 65535)):
#     ports = dict()
#     for port in range(port_range[0], port_range[1]):
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.settimeout(1)
#         conn = s.connect_ex((target, port))
#         try:
#             if conn == 0:
#                 ports[getservbyport(port)] = True
#             else:
#                 ports[getservbyport(port)] = False
#         except OSError:
#             continue
#         finally:
#             s.close()
#     return ports
#
#
# def threaded_scan():
#     ip_addr = get_ip_address()
#     t1 = ThreadWithReturnValue(name="thread-1", target=all_ports_scan, args=(ip_addr, (0, 13107),))
#     t2 = ThreadWithReturnValue(name="thread-2", target=all_ports_scan, args=(ip_addr, (13108, 26214),))
#     # t3 = threading.Thread(name="thread-3", target=all_ports_scan, args=(get_ip_address(), (26215, 39322)))
#     # t4 = threading.Thread(name="thread-4", target=all_ports_scan, args=(get_ip_address(), (39323, 52430)))
#     # t5 = threading.Thread(name="thread-5", target=all_ports_scan, args=(get_ip_address(), (52431, 65535)))
#
#     t1.start()
#     t2.start()
#     # t3.start()
#     # t4.start()
#     # t5.start()
#
#     t1.join()
#     t2.join()
#     # t3.join()
#     # t4.join()
#     # t5.join()
#
#
# print(get_ip_address())
# threaded_scan()
