#!/opt/homebrew/bin/python3

import csv

'''
create a file named proxy-route-rule-info.csv with the following columns:
seq_number,PeerID,LOCAL_NET_OBJ,REMOTE_NET_OBJ,TunnelID,src_zone_name

Example:

seq_number,PeerID,LOCAL_NET_OBJ,REMOTE_NET_OBJ,TunnelID,src_zone_name
1,141.57.50.11,N-172.24.10.0_24,N-172.25.10.0_24,10,FW-INSIDE
2,141.57.50.11,N-172.24.20.0_24,N-172.25.20.0_24,10,FW-DMZ
3,141.57.50.11,N-172.24.30.0_24,N-172.25.30.0_24,10,FW-APP
4,141.57.50.11,N-172.24.10.0_24,N-172.26.10.0_24,10,FW-INSIDE
5,141.57.50.11,N-172.24.20.0_24,N-172.26.20.0_24,10,FW-DMZ
6,141.57.50.11,N-172.24.30.0_24,N-172.26.30.0_24,10,FW-APP

!! MAKE SURE TO CREATE THE OBJECTS FOR THE LOCAL AND REMOTE NETWORKS!!

'''

local_nets_collect = [] #collect local nets blocks
remote_nets_collect = [] #collect remote net blocks
local_zone_collect = [] #collect zone names

def print_proxy_id():
    print ('set network tunnel ipsec PEER-' + PeerID + ' auto-key proxy-id PROXY-ID-' + seq_number + ' protocol any')
    print ('set network tunnel ipsec PEER-' + PeerID + ' auto-key proxy-id PROXY-ID-' + seq_number + ' local ' + LOCAL_NET_OBJ)
    print ('set network tunnel ipsec PEER-' + PeerID + ' auto-key proxy-id PROXY-ID-' + seq_number + ' remote ' + REMOTE_NET_OBJ)
    print ('')

def print_static_route():
    print ('set network virtual-router default routing-table ip static-route PEER-' + PeerID + '-R' + seq_number + ' interface tunnel.' + TunnelID)
    print ('set network virtual-router default routing-table ip static-route PEER-' + PeerID + '-R' + seq_number + ' metric 10')
    print ('set network virtual-router default routing-table ip static-route PEER-' + PeerID + '-R' + seq_number + ' destination ' + REMOTE_NET_OBJ)
    print ('set network virtual-router default routing-table ip static-route PEER-' + PeerID + '-R' + seq_number + ' route-table unicast')
    print ('set network virtual-router default routing-table ip static-route PEER-' + PeerID + '-R' + seq_number + ' bfd profile None')
    print ('')

def print_sec_rule_out():
    print('set rulebase security rules ' + rule_name_out + ' to VPN-S2S')
    print('set rulebase security rules ' + rule_name_out + ' from ' + zone_names)
    print('set rulebase security rules ' + rule_name_out + ' source' + str(local_nets))
    print('set rulebase security rules ' + rule_name_out + ' destination' + str(remote_nets))
    print('set rulebase security rules ' + rule_name_out + ' source-user any')
    print('set rulebase security rules ' + rule_name_out + ' category any')
    print('set rulebase security rules ' + rule_name_out + ' application any')
    print('set rulebase security rules ' + rule_name_out + ' any')
    print('set rulebase security rules ' + rule_name_out + ' source-hip any')
    print('set rulebase security rules ' + rule_name_out + ' destination-hip any')
    print('set rulebase security rules ' + rule_name_out + ' action allow')
    print('')

def print_sec_rule_in():
    print('set rulebase security rules ' + rule_name_out + ' to ' + zone_names)
    print('set rulebase security rules ' + rule_name_out + ' from VPN-S2S')
    print('set rulebase security rules ' + rule_name_out + ' source' + str(remote_nets))
    print('set rulebase security rules ' + rule_name_out + ' destination' + str(local_nets))
    print('set rulebase security rules ' + rule_name_out + ' source-user any')
    print('set rulebase security rules ' + rule_name_out + ' category any')
    print('set rulebase security rules ' + rule_name_out + ' application any')
    print('set rulebase security rules ' + rule_name_out + ' any')
    print('set rulebase security rules ' + rule_name_out + ' source-hip any')
    print('set rulebase security rules ' + rule_name_out + ' destination-hip any')
    print('set rulebase security rules ' + rule_name_out + ' action allow')
    print('')


with open('proxy-route-rule-info.csv') as f:
    info = csv.reader(f)
    next(info)
    for seq_number,PeerID,LOCAL_NET_OBJ,REMOTE_NET_OBJ,TunnelID,src_zone_name in info:
        print_proxy_id()

with open('proxy-route-rule-info.csv') as f:
    info = csv.reader(f)
    next(info)
    for seq_number,PeerID,LOCAL_NET_OBJ,REMOTE_NET_OBJ,TunnelID,src_zone_name in info:
        print_static_route()


with open('proxy-route-rule-info.csv') as f:
    info = csv.reader(f)
    next(info)   # skip header
    for seq_number,PeerID,LOCAL_NET_OBJ,REMOTE_NET_OBJ,TunnelID,src_zone_name in info:
        rule_name_in = 'ALLOW-' + PeerID + '-INBOUND' #construct inbound rule name
        rule_name_out = 'ALLOW-' + PeerID + '-OUTBOUND' #construct outbound rule name
        local_nets_collect.append(LOCAL_NET_OBJ) #append ip blocks to list above
        remote_nets_collect.append(REMOTE_NET_OBJ) #append ip blocks to list above
        local_zone_collect.append(src_zone_name) #append zone names to list above

#converts lists to sets to ensure uniquness
local_nets = list(set(local_nets_collect)) 
remote_nets = list(set(remote_nets_collect))
zone_names = list(set(local_zone_collect))

#convert lists to Palo Alto format
local_nets =  "[ " + " ".join(local_nets_collect) + " ]" 
remote_nets = "[ " + " ".join(remote_nets_collect) + " ]"
zone_names = "[ " + " ".join(local_zone_collect) + " ]"


print_sec_rule_in()
print_sec_rule_out()