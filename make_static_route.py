#!/usr/bin/python3

'''
create a file named static-route-info.csv with the following columns:
Route_number,PeerID,TunnelID,REMOTE_NET

Example:

1,209.151.143.147,25,10.10.100.0/24
2,209.151.143.147,25,10.10.110.0/24
3,209.151.143.147,25,10.10.120.0/24
4,209.151.143.147,25,10.10.130.0/24
5,209.151.143.147,25,10.10.140.0/24
6,209.151.143.147,25,10.10.150.0/24
7,209.151.143.147,25,10.10.160.0/24
8,209.151.143.147,25,10.10.170.0/24

'''

def print_static_route():
    print ('set network virtual-router default routing-table ip static-route PEER-' + PeerID + '-R' + Route_number + ' interface tunnel.' + TunnelID)
    print ('set network virtual-router default routing-table ip static-route PEER-' + PeerID + '-R' + Route_number + ' metric 10')
    print ('set network virtual-router default routing-table ip static-route PEER-' + PeerID + '-R' + Route_number + ' destination ' + REMOTE_NET)
    print ('set network virtual-router default routing-table ip static-route PEER-' + PeerID + '-R' + Route_number + ' route-table unicast')
    print ('set network virtual-router default routing-table ip static-route PEER-' + PeerID + '-R' + Route_number + ' bfd profile None')
    print ('')


with open('/home/yuval/Python_Projects/static-route-info.csv') as f:
        info = f.read().splitlines()
        for i in info:
            Route_number, PeerID, TunnelID, REMOTE_NET = i.split(',')
            print_static_route()
