#!/usr/bin/python3

import csv

'''
create a file named proxy-route-rule-info.csv with the following headers columns:
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

** For a Single host:
!! IF you add a single host to the csv file: DO NOT add '/32' at the end !!

'''


def print_proxy_id(PeerID,seq_number,local_nets_set,remote_nets_set):
    print (f'set network tunnel ipsec PEER-{PeerID} auto-key proxy-id PROXY-ID-{seq_number} protocol any')
    print (f'set network tunnel ipsec PEER-{PeerID} auto-key proxy-id PROXY-ID-{seq_number} local {a}')
    print (f'set network tunnel ipsec PEER-{PeerID} auto-key proxy-id PROXY-ID-{seq_number} remote {b}')
    # print ('')

def print_static_route(PeerID,seq_number,TunnelID,REMOTE_NET_OBJ):
    print (f'set network virtual-router default routing-table ip static-route PEER-{PeerID}-R{seq_number} interface tunnel.{TunnelID}')
    print (f'set network virtual-router default routing-table ip static-route PEER-{PeerID}-R{seq_number} metric 10')
    print (f'set network virtual-router default routing-table ip static-route PEER-{PeerID}-R{seq_number} destination {REMOTE_NET_OBJ}')
    print (f'set network virtual-router default routing-table ip static-route PEER-{PeerID}-R{seq_number} route-table unicast')
    print (f'set network virtual-router default routing-table ip static-route PEER-{PeerID}-R{seq_number} bfd profile None')
    print ('')

def print_sec_rule_out(rule_name_out,zone_names,local_nets,remote_nets):
    print(f'set rulebase security rules {rule_name_out} to VPN-S2S')
    print(f'set rulebase security rules {rule_name_out} from {zone_names}')
    print(f'set rulebase security rules {rule_name_out} source {remote_nets}')
    print(f'set rulebase security rules {rule_name_out} destination {local_nets}')
    # print(f'set rulebase security rules {rule_name_out} source {local_subnet_obj}')
    # print(f'set rulebase security rules {rule_name_out} destination {remote_subnet_obj}')
    print(f'set rulebase security rules {rule_name_out} source-user any')
    print(f'set rulebase security rules {rule_name_out} category any')
    print(f'set rulebase security rules {rule_name_out} application any')
    print(f'set rulebase security rules {rule_name_out} service any')
    print(f'set rulebase security rules {rule_name_out} source-hip any')
    print(f'set rulebase security rules {rule_name_out} destination-hip any')
    print(f'set rulebase security rules {rule_name_out} action allow')
    print('')

def print_sec_rule_in(rule_name_in,zone_names,remote_nets,local_nets):
    print(f'set rulebase security rules {rule_name_in} to {zone_names}')
    print(f'set rulebase security rules {rule_name_in} from VPN-S2S')
    print(f'set rulebase security rules {rule_name_in} source {local_nets}')
    print(f'set rulebase security rules {rule_name_in} destination {remote_nets}')
    print(f'set rulebase security rules {rule_name_in} source-user any')
    print(f'set rulebase security rules {rule_name_in} category any')
    print(f'set rulebase security rules {rule_name_in} application any')
    print(f'set rulebase security rules {rule_name_in} service any')
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

local_subnet = set()
remote_subnet = set()
local_host = set()
remote_host = set()

local_subnet_obj = set()
remote_subnet_obj = set()
local_host_obj = set()
remote_host_obj = set()

local_nets_set = set() #collect local nets blocks
remote_nets_set = set() #collect remote net blocks
local_zone = set() #collect zone names




# #-- creating Address-Objects
print('========================')
print('ADDRESS-OBJECT Section')
print('========================')
with open('proxy-route-rule-info.csv') as f:
    info = csv.reader(f)
    next(info)
    for seq_number,PeerID,LOCAL_NET_OBJ,src_zone_name,REMOTE_NET_OBJ,TunnelID in info:
        if '/' in LOCAL_NET_OBJ:
            local_subnet.add(LOCAL_NET_OBJ)
        if '/' in REMOTE_NET_OBJ:
            remote_subnet.add(REMOTE_NET_OBJ)
        if '/' not in LOCAL_NET_OBJ:
            local_host.add(LOCAL_NET_OBJ + '/32')
        if '/' not in REMOTE_NET_OBJ:
            remote_host.add(REMOTE_NET_OBJ + '/32')
        if '/32' in LOCAL_NET_OBJ:
            host_obj.add(LOCAL_NET_OBJ)
        if '/32' in REMOTE_NET_OBJ:
            host_obj.add(REMOTE_NET_OBJ)


for i in local_subnet:
    print_subnet_obj(i)
for i in remote_subnet:
    print_subnet_obj(i)
for i in local_host:
    print_host_obj(i)
for i in remote_host:
    print_host_obj(i)

#subnet objects setup
for i in local_subnet:
    i = 'N-'+i.replace('/','_')
    local_subnet_obj.add(i)
for i in remote_subnet:
    i = 'N-'+i.replace('/','_')
    remote_subnet_obj.add(i)

#hosts objects setup
for i in local_host:
    # i = 'H-'+i.replace('/','_')
    i = 'H-'+i.strip('/32')
    local_host_obj.add(i)
for i in remote_host:
    # i = 'H-'+i.replace('/','_')
    i = 'H-'+i.strip('/32')
    remote_host_obj.add(i)


# print(local_subnet_obj)
# print(remote_subnet_obj)
# print(local_host_obj)
# print(remote_host_obj)


# creating static route
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


local_subnet_obj = sorted(local_subnet_obj)
remote_subnet_obj = sorted(remote_subnet_obj)


print('==================')
print('IPSEC With PROXY ID Section')
print('==================')
print('**!!')
print('**!! BEFORE COPYING note: Ike Gateway MUST be present before proceeding !!**')
print('**!!')
print(f'set network tunnel ipsec PEER-{PeerID} auto-key ike-gateway PEER-{PeerID}')
seq_number = 1 
for a in local_nets_set:
    for b in remote_nets_set:
        print_proxy_id(PeerID,seq_number,local_nets_set,remote_nets_set)
        seq_number += 1
print(f'set network tunnel ipsec PEER-{PeerID} auto-key ipsec-crypto-profile <!!!! ENTER PHASE 1 SET NAME !!!!>')
print(f'set network tunnel ipsec PEER-{PeerID} tunnel-monitor enable no')
print(f'set network tunnel ipsec PEER-{PeerID} tunnel-interface tunnel.{TunnelID}')
print(f'set network tunnel ipsec PEER-{PeerID} disabled no')


#convert lists to Palo Alto format
local_nets =  "[ " + " ".join(local_subnet_obj) + " ]" 
remote_nets = "[ " + " ".join(remote_subnet_obj) + " ]"
zone_names  = "[ " + " ".join(local_zone) + " ]"

print('========================')
print('SECURITY POLICY Section')
print('========================')
#-- creating security policy 
print_sec_rule_out(rule_name_out,zone_names,remote_nets,local_nets)
print_sec_rule_in(rule_name_in,zone_names,local_nets,remote_nets)
