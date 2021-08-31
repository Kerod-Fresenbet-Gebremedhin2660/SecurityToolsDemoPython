from scapy.all import *
from scapy.layers.inet import ICMP, IP


def DetectOS(ipaddress: str) ->str:
    ip_packet = IP(dst=ipaddress)/ICMP()
    response = sr1(ip_packet, timeout=2)

    if response is None:
        return None
    elif IP in response:
        if response.getlayer(IP).ttl <= 64:
            return "Linux"
        elif response.getlayer(IP).ttl >64:
            return "Windows"

