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

'''

subnet_obj = set()
host_obj = set()

def print_subnet_obj(subnet):
	subnet_obj_name = subnet.replace('/','_')
	print(f'set address N-{subnet_obj_name} ip-netmask {subnet}')

def print_host_obj(host):
	host_net = host.replace('/32','')
	print(f'set address H-{host_net} ip-netmask {host}')

with open('proxy-route-rule-info.csv') as f:
	info = csv.reader(f)
	next(info)
	for seq_number,PeerID,LOCAL_NET_OBJ,src_zone_name,REMOTE_NET_OBJ,TunnelID in info:
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
