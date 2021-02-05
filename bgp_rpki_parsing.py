#!/bin/env python3

import os, re, argparse
import bgp_rpki_utils as bgprpki
from pprint import pprint
from netmiko import ConnectHandler

parser = argparse.ArgumentParser()
parser.add_argument('--host', help='router ip address', required=True)
parser.add_argument('--user', help='router login username', required=True)
parser.add_argument('--password', help='router login password', required=True)
parser.add_argument('--report_dir', help='directory where report files placed', required=False, default='./report')
args = parser.parse_args()

cisco1 = {
    "device_type": "cisco_xr",
    "host": args.host,
    "username": args.user,
    "password": args.password,
    "global_delay_factor": 2
}

# Show bgp origin-as validity command execution
command1 = "show bgp origin-as validity invalid"
command2 = "show bgp ipv6 unicast origin-as validity invalid"

with ConnectHandler(**cisco1) as net_connect:
    net_connect.find_prompt()
    output1 = net_connect.send_command('term length 0')
    output1 = net_connect.send_command(command1)
    output2 = net_connect.send_command(command2)

bgp_prefixes = bgprpki.parse_sh_bgp_origin_as_invalid_ipv4(output1)
bgp_prefixes_ipv6 = bgprpki.parse_sh_bgp_origin_as_invalid_ipv6(output2)
# pprint(bgp_prefixes);# pprint(bgp_prefixes_ipv6)
bgp_prefixes.extend(bgp_prefixes_ipv6)
bgprpki.bgp_rpki_report(args.host, bgp_prefixes, args.report_dir)
