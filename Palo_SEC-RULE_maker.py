#!/usr/local/bin/python3

#this script will convert a CVS file with info to a Palo Alto security rule form

'''

Before you start:

create a file named rules_info.csv with the following columns:
rule_name, dest_zone, src_addr, dest_addr, service

Example:

allow_access_to_16.27, FW-INSIDE, 52.101.37.97, 172.24.16.27, TCP-80
allow_access_to_16.27, FW-INSIDE, 52.101.37.97, 172.24.16.27, TCP-443
allow_access_to_16.28, FW-INSIDE, 52.101.37.97, 172.24.16.27, TCP-80
allow_access_to_16.28, FW-INSIDE, 52.101.37.97, 172.24.16.27, TCP-443

!!NOTE: This script assume that the source is coming through the OUTSIDE zone ony!!
'''


def print_sec_rule():
    print('set rulebase security rules ' + rule_name + ' to ' + dest_zone)
    print('set rulebase security rules ' + rule_name + ' from OUTSIDE')
    print('set rulebase security rules ' + rule_name + ' source ' + src_addr)
    print('set rulebase security rules ' + rule_name + ' destination ' + dest_addr)
    print('set rulebase security rules ' + rule_name + ' source-user any')
    print('set rulebase security rules ' + rule_name + ' category any')
    print('set rulebase security rules ' + rule_name + ' application any')
    print('set rulebase security rules ' + rule_name + ' service ' + service)
    print('set rulebase security rules ' + rule_name + ' source-hip any')
    print('set rulebase security rules ' + rule_name + ' destination-hip any')
    print('set rulebase security rules ' + rule_name + ' action allow')
    print('')


with open('/Users/yuva2331/Yuval-Python/ASA_to_Palo-prep/rules_info.csv') as f:
    info = f.read().splitlines()
    for i in info:
        rule_name, dest_zone, src_addr, dest_addr, service = i.split(',')
        print_sec_rule()
