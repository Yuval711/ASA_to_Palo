#!/usr/local/bin/python3


'''
This script will create a service objects config syntax for Palo Alto.

You need to create a file with the list of TCP ports named: TCP_port_list.txt

Example:
8080
443
21


this will make the following result:

set service UDP-8080 protocol udp port 8080
set service UDP-8080 protocol udp override no
set service UDP-443 protocol udp port 443
set service UDP-443 protocol udp override no
set service UDP-21 protocol udp port 21
set service UDP-21 protocol udp override no

you can copy and paste it to the firewall
'''

with open('/Users/yuva2331/Yuval-Python/ASA_to_Palo-prep/UDP_port_list.txt') as f:
    info = f.read().splitlines()
    for port in info:
        print('set service UDP-' + port + ' protocol udp port '  + port)
        print('set service UDP-' + port + ' protocol udp override no')
