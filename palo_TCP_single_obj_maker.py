#!/usr/local/bin/python3

import sys

'''
This script will create an address object syntax for Palo Alto.

You can run the script with the TCP port.

Example:

palo_tcp_single_obj_maker.py 8080

this will make the following result:

set service TCP-8080 protocol tcp port 8080
set service TCP-8080 protocol tcp override no

you can copy and paste it to the firewall
'''


for arg in sys.argv[1:]:
    port = arg

print('set service TCP-' + port + ' protocol tcp port '  + port)
print('set service TCP-' + port + ' protocol tcp override no')
