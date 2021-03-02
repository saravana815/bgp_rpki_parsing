import os, re
import pandas as pd
import numpy as np
import jinja2

from pprint import pprint
from datetime import datetime
from pathlib import Path

def parse_sh_bgp_origin_as_invalid_ipv4(output):
    prefix_start_flag = False
    match1 = []; match2 = []; bgp_prefixes = []

    #pat1 "*> 1.1.1.0/24         217.46.30.8              5             0 4000 6000 i"
    #pat2 "*                     217.46.30.10             5             0 5000 6000 i"
    pat1 = re.compile(r"^[\S]*\s+(\d+\.\d+\.\d+\.\d+\/\d+)\s+(\d+\.\d+\.\d+\.\d+)\s")
    pat2 = re.compile(r"^[\S]*\s+(\d+\.\d+\.\d+\.\d+)\s")
    as_num = re.compile(r"(\d+)\s+")

    lines = output.splitlines()
    for line in lines:
        # print(line)
        if 'Network' in line:
            as_path_start_index = line.find('Path')
            # print('as_path_start_index', as_path_start_index)
            prefix_start_flag = True
            continue

        if prefix_start_flag == True:
            #match line with bgp prefix and nexthop on same line
            #*> 1.1.1.0/24         217.46.30.8              5             0 4000 6000 i
            if pat1.search(line):
                match1 = pat1.findall(line)
                prefix = match1[0][0]
                nexthop = match1[0][1]
                as_path = line[as_path_start_index:]
                as_list = as_num.findall(as_path)
                as_last = int(as_list[-1])
                bgp_prefixes.append([prefix,nexthop,as_last, 1])

            #match line with bgp nexthop on current line and prefix on previous line
            #*                     217.46.30.10             5             0 5000 6000 i
            elif pat2.search(line):
                match2 = pat2.findall(line)
                if len(match1) == 0:
                    print('ERROR: Not able to parse the CLI line correctly')
                    print('LINE: ', line)
                    exit(1)
                prefix = match1[0][0]
                nexthop = match2[0]
                as_path = line[as_path_start_index:]
                as_list = as_num.findall(as_path)
                as_last = int(as_list[-1])
                bgp_prefixes.append([prefix,nexthop,as_last, 1])

    return bgp_prefixes


def parse_sh_bgp_origin_as_invalid_ipv6(output):
    prefix_start_flag = False
    match1 = []; match2 = []; match3 = []; bgp_prefixes = []

    #pat1 "*  2001:200:600::/40  217.46.30.8                            0 4000 25846 51320 52325 59744 i"
    #pat2 "*>                    217.46.30.8                            0 5000 21969 i"
    #pat3 prefix on one line and nexthop on second line
    #     *> 2001:200:600:1000:2000:3000:4000:0/128
    #                  217.46.30.8                            0 4000 25846 51320 52325 59744 i

    pat1 = re.compile(r"^[\S]*\s+([0-9a-fA-F\:\/]+)\s+([0-9a-fA-F\.\:]+)\s")
    pat2 = re.compile(r"^[\S]*\s+[^0-9a-fA-F\:\/]+\s+([0-9a-fA-F\.\:]+)\s")
    pat3 = re.compile(r"^[\S]*\s+([0-9a-fA-F\:\/]+)$")
    as_num = re.compile(r"(\d+)\s+")

    lines = output.splitlines()
    for line in lines:
        # print(line)
        if 'Network' in line:
            as_path_start_index = line.find('Path')
            # print('as_path_start_index', as_path_start_index)
            prefix_start_flag = True
            continue

        if prefix_start_flag == True:
            #match line with bgp prefix and nexthop on same line
            #*  2001:200:600::/40  217.46.30.8                            0 4000 25846 51320 52325 59744 i
            if pat1.search(line):
                match1 = pat1.findall(line)
                prefix = match1[0][0]
                nexthop = match1[0][1]
                as_path = line[as_path_start_index:]
                as_list = as_num.findall(as_path)
                as_last = int(as_list[-1])
                bgp_prefixes.append([prefix,nexthop,as_last, 1])

            #match line with bgp nexthop on current line and prefix on previous line
            #*>                    217.46.30.8                            0 5000 21969 i
            elif pat2.search(line):
                match2 = pat2.findall(line)
                if len(match1) == 0:
                    print('ERROR: Not able to parse the CLI line correctly')
                    print('LINE: ', line)
                    exit(1)
                prefix = match1[0][0]
                nexthop = match2[0]
                as_path = line[as_path_start_index:]
                as_list = as_num.findall(as_path)
                as_last = int(as_list[-1])
                bgp_prefixes.append([prefix,nexthop,as_last, 1])

            #     *> 2001:200:600:1000:2000:3000:4000:0/128
            #                  217.46.30.8                            0 4000 25846 51320 52325 59744 i
            elif pat3.search(line):
                match3 = pat3.findall(line)
                #set prefix as pat1 matched prefix
                match1 = []
                match1.append([match3[0]])

    return bgp_prefixes


def bgp_rpki_report(host, bgp_prefixes, report_dir):
    # convert bgp_prefixes from python list to pandas dataframe
    df = pd.DataFrame(bgp_prefixes, columns = ['BGP Prefix', 'Nexthop', 'Source AS', 'Prefix Count'])
    df = (df.groupby(['Source AS'], as_index=True).agg({'Prefix Count': 'count', 'BGP Prefix':lambda x : '<BR>'.join(x)}))

    # prefix_count_list for graph plotting
    prefix_count_list = df['Prefix Count'].tolist()
    # timestamp for report files
    timenow = datetime.now().strftime('%Y%m%d_%H%M%S')
    # report file directory
    Path(report_dir).mkdir(parents=True, exist_ok=True)

    def color_negative_red(val):
        color = 'red'
        return f'color: {color}'
    styler = df.style.applymap(color_negative_red)

    # create bar chart from pandas dataframe
    # ax = df.plot.pie(y='Prefix Count', figsize=(8, 8), autopct='%1.1f%%')
    ax = df.plot.barh(figsize=(10, 200))
    for index, value in enumerate(prefix_count_list):
        ax.text(value, index, ' ' + str(value))
    fig = ax.get_figure()
    plot_file = f"{report_dir}/plot_{host}_{timenow}.svg"
    fig.savefig(plot_file)

    # Template handling
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))
    template = env.get_template('template.html')
    html = template.render(host=host, timenow=timenow, plot_file=f"plot_{host}_{timenow}.svg",  my_table=styler.render())

    # Write the HTML report file
    report_file = f"{report_dir}/bgp_rpki_report_{host}_{timenow}.html"
    with open(report_file, 'w') as f:
        f.write(html)
