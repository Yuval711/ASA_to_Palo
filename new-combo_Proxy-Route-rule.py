#!/usr/bin/python3

import csv

'''
create a file named proxy-route-rule-info.csv with the following columns:
seq_number,PeerID,LOCAL_NET_OBJ,src_zone_name,REMOTE_NET_OBJ,TunnelID

Example:

seq_number,PeerID,LOCAL_NET_OBJ,src_zone_name,REMOTE_NET_OBJ,TunnelID,
1,141.57.50.11,N-172.24.10.0_24,FW-INSIDE,N-172.25.10.0_24,10
2,141.57.50.11,N-172.24.20.0_24,FW-DMZ,N-172.25.20.0_24,10,10
3,141.57.50.11,N-172.24.30.0_24,FW-APP,N-172.25.30.0_24,10,10
4,141.57.50.11,N-172.24.10.0_24,FW-INSIDE,N-172.26.10.0_24,10
5,141.57.50.11,N-172.24.20.0_24,FW-DMZ,N-172.26.20.0_24,10,10
6,141.57.50.11,N-172.24.30.0_24,FW-APP,N-172.26.30.0_24,10,10

!! MAKE SURE TO CREATE THE OBJECTS FOR THE LOCAL AND REMOTE NETWORKS!!
'''

def print_proxy_id(PeerID,seq_number,local_nets,remote_nets):
    print (f'set network tunnel ipsec PEER-{PeerID} auto-key proxy-id PROXY-ID-{seq_number} protocol any')
    print (f'set network tunnel ipsec PEER-{PeerID} auto-key proxy-id PROXY-ID-{seq_number} local {a}')
    print (f'set network tunnel ipsec PEER-{PeerID} auto-key proxy-id PROXY-ID-{seq_number} remote {b}')
    print ('')

def print_static_route(PeerID,seq_number,TunnelID,REMOTE_NET_OBJ):
    print (f'set network virtual-router default routing-table ip static-route PEER-{PeerID}-R{seq_number} interface tunnel{TunnelID}')
    print (f'set network virtual-router default routing-table ip static-route PEER-{PeerID}-R{seq_number} metric 10')
    print (f'set network virtual-router default routing-table ip static-route PEER-{PeerID}-R{seq_number} destination{REMOTE_NET_OBJ}')
    print (f'set network virtual-router default routing-table ip static-route PEER-{PeerID}-R{seq_number} route-table unicast')
    print (f'set network virtual-router default routing-table ip static-route PEER-{PeerID}-R{seq_number} bfd profile None')
    print ('')

def print_sec_rule_out(rule_name_out,zone_names,local_nets,remote_nets):
    print(f'set rulebase security rules {rule_name_out} to VPN-S2S')
    print(f'set rulebase security rules {rule_name_out} from {zone_names}')
    print(f'set rulebase security rules {rule_name_out} source {local_nets}')
    print(f'set rulebase security rules {rule_name_out} destination {remote_nets}')
    print(f'set rulebase security rules {rule_name_out} source-user any')
    print(f'set rulebase security rules {rule_name_out} category any')
    print(f'set rulebase security rules {rule_name_out} application any')
    print(f'set rulebase security rules {rule_name_out} any')
    print(f'set rulebase security rules {rule_name_out} source-hip any')
    print(f'set rulebase security rules {rule_name_out} destination-hip any')
    print(f'set rulebase security rules {rule_name_out} action allow')
    print('')

def print_sec_rule_in(rule_name_in,zone_names,remote_nets,local_nets):
    print(f'set rulebase security rules {rule_name_in} to {zone_names}')
    print(f'set rulebase security rules {rule_name_in} from VPN-S2S')
    print(f'set rulebase security rules {rule_name_in} source {remote_nets}')
    print(f'set rulebase security rules {rule_name_in} destination {local_nets}')
    print(f'set rulebase security rules {rule_name_in} source-user any')
    print(f'set rulebase security rules {rule_name_in} category any')
    print(f'set rulebase security rules {rule_name_in} application any')
    print(f'set rulebase security rules {rule_name_in} any')
    print(f'set rulebase security rules {rule_name_in} source-hip any')
    print(f'set rulebase security rules {rule_name_in} destination-hip any')
    print(f'set rulebase security rules {rule_name_in} action allow')
    print('')


local_nets = set() #collect local nets blocks
remote_nets = set() #collect remote net blocks
local_zone = set() #collect zone names

#-- createing security policy
with open('proxy-route-rule-info.csv') as f:
    info = csv.reader(f)
    next(info)   # skip header
    for seq_number,PeerID,LOCAL_NET_OBJ,src_zone_name,REMOTE_NET_OBJ,TunnelID in info:
        rule_name_in = 'ALLOW-PEER-' + PeerID + '-INBOUND' #construct inbound rule name
        rule_name_out = 'ALLOW-PEER-' + PeerID + '-OUTBOUND' #construct outbound rule name
        local_nets.add(LOCAL_NET_OBJ) #append ip blocks to list above
        remote_nets.add(REMOTE_NET_OBJ) #append ip blocks to list above
        local_zone.add(src_zone_name) #append zone names to list above
        print_static_route(PeerID,seq_number,TunnelID,REMOTE_NET_OBJ) #-- createing static route

#-- creating proxy-id's
seq_number = 1 
for a in local_nets:
    for b in remote_nets:
        print_proxy_id(PeerID,seq_number,local_nets,remote_nets)
        seq_number += 1

#convert lists to Palo Alto format
local_nets =  "[ " + " ".join(local_nets) + " ]" 
remote_nets = "[ " + " ".join(remote_nets) + " ]"
zone_names  = "[ " + " ".join(local_zone) + " ]"

#-- creating security policy 
print_sec_rule_in(rule_name_out,zone_names,local_nets,remote_nets)
print_sec_rule_out(rule_name_in,zone_names,remote_nets,local_nets)
