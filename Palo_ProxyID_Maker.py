#!/usr/local/bin/python3

'''
create a file named proxy-id-info.csv with the following columns:
seq_number,PeerID,LOCAL_NET_OBJ,REMOTE_NET_OBJ

Example:

1,47.19.18.194,172.16.96.0/22,N-10.200.1.0/24
2,47.19.18.194,172.16.96.0/22,N-10.200.1.0/24
3,47.19.18.194,172.24.16.0/22,N-10.200.1.0/24
4,47.19.18.194,172.24.32.0/22,N-10.200.1.0/24

'''

def print_proxy_id():
    print ('set network tunnel ipsec PEER-' + PeerID + ' auto-key proxy-id PROXY-ID-' + seq_number + ' protocol any')
    print ('set network tunnel ipsec PEER-' + PeerID + ' auto-key proxy-id PROXY-ID-' + seq_number + ' local ' + LOCAL_NET)
    print ('set network tunnel ipsec PEER-' + PeerID + ' auto-key proxy-id PROXY-ID-' + seq_number + ' remote ' + REMOTE_NET)

with open('/Users/yuva2331/Yuval-Python/ASA_to_Palo-prep/proxy-id-info.csv') as f:
	info = f.read().splitlines()
	for i in info:
    	    seq_number, PeerID, LOCAL_NET, REMOTE_NET = i.split(',')
    	    print_proxy_id()
