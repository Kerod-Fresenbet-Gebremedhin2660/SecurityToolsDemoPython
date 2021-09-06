from scapy.all import *
from scapy.layers.inet import ICMP, IP


def DetectOS(ipaddress: str) -> str or None:
    ip_packet = IP(dst=ipaddress)
    response = sr1(ip_packet, timeout=12)

    if response is None:
        return None
    elif IP in response:
        if response.getlayer(IP).ttl <= 64:
            return "linux"
        elif response.getlayer(IP).ttl > 64:
            return "windows"


print(DetectOS("192.168.0.154"))
