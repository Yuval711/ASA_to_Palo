#!/opt/homebrew/bin/python3

'''
This will make the CLI version of test security policy
you will need to give it 4 variables and in the FOLLOWING ORDER:

sourceIP, sourceZone destinationIP, destinationZone, port.

example:

make-spt.py <sourceIP> <sourceZone> <destinationIp> <destinationZone> <port number> 

live sample:
yuva2331$make-spt.py 172.24.10.41 FW-inside 10.47.20.1 FW-app 443


to get the zone for the IP: run 

Palo_alto-FW>test routing fib-lookup virtual-router default ip 172.24.10.42

the above will give you the interface, now check the interface to find the zone:


Palo_alto-FW>show interface ethernet1/2.501 | match Zone


'''

import sys


info = []

for arg1 in sys.argv[1:]:
    info.append(arg1)

print('forward:')
print(f'test security-policy-match from {info[1]} source {info[0]} to {info[3]} destination {info[2]} destination-port {info[4]} protocol 6')
print(' ')
print('return:')
print(f'test security-policy-match from {info[3]} source {info[2]} to {info[1]} destination {info[0]} destination-port {info[4]} protocol 6')