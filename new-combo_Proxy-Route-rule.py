#!/usr/bin/python3

import csv

'''
create a file named proxy-route-rule-info.csv with the following columns:
seq_number,PeerID,LOCAL_NET_OBJ,src_zone_name,REMOTE_NET_OBJ,TunnelID

Example:

seq_number,PeerID,LOCAL_NET_OBJ,src_zone_name,REMOTE_NET_OBJ,TunnelID,
1,141.57.50.11,172.24.10.0/24,FW-INSIDE,172.25.10.0/24,10
2,141.57.50.11,172.24.20.0/24,FW-DMZ,172.25.20.0/24,10,10
3,141.57.50.11,172.24.30.0/24,FW-APP,172.25.30.0/24,10,10
4,141.57.50.11,172.24.10.0/24,FW-INSIDE,172.26.10.0/24,10
5,141.57.50.11,172.24.20.0/24,FW-DMZ,172.26.20.0/24,10,10
6,141.57.50.11,172.24.30.0/24,FW-APP,172.26.30.0/24,10,10

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
    print (f'set network virtual-router default routing-table ip static-route PEER-{PeerID}-R{seq_number} destination {REMOTE_NET_OBJ}')
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

def print_subnet_obj(subnet):
    subnet_obj_name = subnet.replace('/','_')
    print(f'set address N-{subnet_obj_name} ip-netmask {subnet}')

def print_host_obj(host):
    host_net = host.replace('/32','')
    print(f'set address H-{host_net} ip-netmask {host}')

subnet_obj = set()
host_obj = set()

local_nets_set = set() #collect local nets blocks
remote_nets_set = set() #collect remote net blocks
local_zone = set() #collect zone names

#-- creating Address-Objects
print('========================')
print('ADDRESS-OBJECT Section')
print('========================')
with open('proxy-route-rule-info.csv') as f:
    info = csv.reader(f)
    next(info)
    for seq_number,PeerID,LOCAL_NET_OBJ,src_zone_name,REMOTE_NET_OBJ,TunnelID in info:
        # if 'N-' or 'H-' in LOCAL_NET_OBJ or REMOTE_NET_OBJ:
        #     existing_obj.add(LOCAL_NET_OBJ)
        #     existing_obj.add(REMOTE_NET_OBJ)
        if '/' in LOCAL_NET_OBJ:
            subnet_obj.add(LOCAL_NET_OBJ)
        if '/' in REMOTE_NET_OBJ:
            subnet_obj.add(REMOTE_NET_OBJ)
        if '/' not in LOCAL_NET_OBJ:
            host_obj.add(LOCAL_NET_OBJ + '/32')
        if '/' not in REMOTE_NET_OBJ:
            host_obj.add(REMOTE_NET_OBJ + '/32')
        if '/32' in LOCAL_NET_OBJ:
            host_obj.add(LOCAL_NET_OBJ)
        if '/32' in REMOTE_NET_OBJ:
            host_obj.add(REMOTE_NET_OBJ)

for i in subnet_obj:
    print_subnet_obj(i)
for i in host_obj:
    print_host_obj(i)


#-- createing security policy
print('=====================')
print('STATIC ROUTE Section')
print('=====================')
with open('proxy-route-rule-info.csv') as f:
    info = csv.reader(f)
    next(info)   # skip header
    for seq_number,PeerID,LOCAL_NET_OBJ,src_zone_name,REMOTE_NET_OBJ,TunnelID in info:
        rule_name_in = 'ALLOW-PEER-' + PeerID + '-INBOUND' #construct inbound rule name
        rule_name_out = 'ALLOW-PEER-' + PeerID + '-OUTBOUND' #construct outbound rule name
        local_nets_set.add(LOCAL_NET_OBJ) #append ip blocks to list above
        remote_nets_set.add(REMOTE_NET_OBJ) #append ip blocks to list above
        local_zone.add(src_zone_name) #append zone names to list above
        print_static_route(PeerID,seq_number,TunnelID,REMOTE_NET_OBJ) #-- createing static route

# Convert to sorted lists so output is consistent
local_nets = sorted(local_nets_set)
remote_nets = sorted(remote_nets_set)

#-- creating proxy-id's
print('==================')
print('PROXY ID Section')
print('==================')
seq_number = 1 
for a in local_nets:
    for b in remote_nets:
        print_proxy_id(PeerID,seq_number,local_nets,remote_nets)
        seq_number += 1

#convert lists to Palo Alto format
local_nets =  "[ " + " ".join(local_nets) + " ]" 
remote_nets = "[ " + " ".join(remote_nets) + " ]"
zone_names  = "[ " + " ".join(local_zone) + " ]"

print('========================')
print('SECURITY POLICY Section')
print('========================')
#-- creating security policy 
print_sec_rule_in(rule_name_out,zone_names,local_nets,remote_nets)
print_sec_rule_out(rule_name_in,zone_names,remote_nets,local_nets)
