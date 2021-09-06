from typing import Dict
import nmap
import json

scanner = nmap.PortScanner()


def DetectOS(ipaddress: str) -> Dict:
    os_info = dict()

    try:
        result = scanner.scan(ipaddress, arguments="-O")['scan'][ipaddress]['osmatch'][0]
    except KeyError as e:
        result = None

    if result is None:
        os_info['detected'] = False
        return os_info

    json_result = json.dumps(result, separators=(',', ':'))
    payload_1 = json.loads(json_result)

    json_result_2 = json.dumps(payload_1["osclass"])
    payload_2 = json.loads(json_result_2)

    os_info['name'] = payload_1["name"]
    os_info['type'] = payload_2[0]["type"]
    os_info['vendor'] = payload_2[0]["vendor"]
    os_info['osfamily'] = payload_2[0]["osfamily"]
    os_info['osgen'] = payload_2[0]["osgen"]
    os_info['accuracy'] = payload_2[0]["accuracy"]
    os_info['cpe'] = payload_2[0]["cpe"]
    os_info['detected'] = True

    return os_info
