# bgp_rpki_parsing

python netmiko based script to parse the `show bgp rpki origin-as validity invalid` output from Cisco IOS-XR router and report the invalid prefixes as HTML report. 

Requirements
  * Python3.6 or above
  * Netmiko
  * Pandas
  * Matplotlib
  * Jinja2
 
## Install steps
```
pip3 install netmiko pandas numpy jinja2 matplotlib
git clone https://github.com/saravana815/pyscripts.git
cd pyscripts/bgp_rpki_parsing
```

## Usage
```
[sargandh:SARGANDH-3QLQC]$ python3 bgp_rpki_parsing.py -h
usage: bgp_rpki_parsing.py [-h] --host HOST --user USER --password PASSWORD

optional arguments:
  -h, --help           show this help message and exit
  --host HOST          router ip address
  --user USER          router login username
  --password PASSWORD  router login password
[sargandh:SARGANDH-3QLQC]$
[sargandh:SARGANDH-3QLQC]$  python3 bgp_rpki_parsing.py --host <router_IP> --user <user_name> --password <password>
[sargandh:SARGANDH-3QLQC]$
[sargandh:SARGANDH-3QLQC]$ ls -ltr bgp_rpki_report_10.51.117.224*
-rwxrwxrwx 1 sargandh sargandh 11717 Feb  1 13:24 bgp_rpki_report_10.51.117.224_20210201_132407.html <<---BGP RPKI report file
[sargandh:SARGANDH-3QLQC]$
```

## Sample HTML report

[Sample Report](https://htmlpreview.github.io/?https://github.com/saravana815/pyscripts/blob/master/bgp_rpki_parsing/report.html)
