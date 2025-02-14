#!/usr/local/bin/python3

import sys


'''
This script will create a UDP service object syntax for Palo Alto.

You can run the script with the UDP port.

Example:

palo_tcp_single_obj_maker.py 8080

this will make the following result:

set service UDP-8080 protocol udp port 8080
set service UDP-8080 protocol udp override no

you can copy and paste it to the firewall
'''

for arg in sys.argv[1:]:
    port = arg

print('set service UDP-' + port + ' protocol udp port '  + port)
print('set service UDP-' + port + ' protocol udp override no')
