#!/usr/local/bin/python3

'''
create a file named nat_ips.csv with the following columns:
private, zone, public

Example:

10.104.90.120,FW-COLO,72.32.133.19
10.104.90.125,FW-COLO,72.32.133.20
10.104.8.120,FW-COLO,72.32.133.22
10.201.87.113,FW-COLO,72.32.133.23

!! NOTE:this is to assume that the source is coming through the OUTSIDE zone!
'''



def print_nat():
    print ('set rulebase nat rules SRC-' + public + ' from ' + zone)
    print ('set rulebase nat rules SRC-' + public + ' source ' + 'H-' + private)
    print ('set rulebase nat rules SRC-' + public + ' to OUTSIDE')
    print ('set rulebase nat rules SRC-' + public + ' destination any')
    print ('set rulebase nat rules SRC-' + public + ' service any')
    print ('set rulebase nat rules SRC-' + public + ' source-translation static-ip translated-address ' + 'H-' + public )
    print ('set rulebase nat rules SRC-' + public + ' source-translation static-ip bi-directional no')
    print ('set rulebase nat rules SRC-' + public + ' tag SRC-NAT')
    print ()
    print ('set rulebase nat rules DST-' + public + ' from OUTSIDE')
    print ('set rulebase nat rules DST-' + public + ' source any')
    print ('set rulebase nat rules DST-' + public + ' to OUTSIDE')
    print ('set rulebase nat rules DST-' + public + ' destination ' + 'H-' + public)
    print ('set rulebase nat rules DST-' + public + ' service any')
    print ('set rulebase nat rules DST-' + public + ' destination-translation dns-rewrite direction forward' )
    print ('set rulebase nat rules DST-' + public + ' destination-translation translated-address ' + 'H-' + private )
    print ('set rulebase nat rules DST-' + public + ' tag DST-NAT')
    print ()

with open('/Users/yuva2331/Yuval-Python/ASA_to_Palo-prep/nat_ips.csv') as f:
	info = f.read().splitlines()
	for i in info:
    	    private, zone, public = i.split(',')
    	    print_nat()
