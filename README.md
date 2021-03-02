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
git clone https://github.com/saravana815/bgp_rpki_parsing.git
cd bgp_rpki_parsing
```

## Usage
```
usage: bgp_rpki_parsing.py [-h] --host HOST --user USER --password PASSWORD
                           [--report_dir REPORT_DIR]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           router ip address
  --user USER           router login username
  --password PASSWORD   router login password
  --report_dir REPORT_DIR
                        directory to place report files (Default dir : ./report/)
                        
[sargandh:SARGANDH-3QLQC]$
[sargandh:SARGANDH-3QLQC]$ python3  bgp_rpki_parsing.py --host 10.51.117.224 --user root --password ciscopass
[sargandh:SARGANDH-3QLQC]$
[sargandh:SARGANDH-3QLQC]$ ls -lh report/
total 32K
-rwxrwxrwx 1 sargandh sargandh 3.9K Feb  4 14:40 bgp_rpki_report_10.51.117.224_20210204_144054.html  <<--- report file 
-rwxrwxrwx 1 sargandh sargandh  27K Feb  4 14:40 plot_10.51.117.224_20210204_144054.svg              <<--- report graph
[sargandh:SARGANDH-3QLQC]$
```

## Sample HTML report

[Sample Report](https://htmlpreview.github.io/?https://github.com/saravana815/bgp_rpki_parsing/blob/master/report/bgp_rpki_report_10.51.117.224_20210204_144054.html)
