#!/opt/homebrew/bin/python3


info = []

sourceIP = input('what is your source IP?\n')
info.append(sourceIP)
sourceZone = input('what is the source zone?\n')
info.append(sourceZone)
destinationIP = input('what is the destination IP?\n')
info.append(destinationIP)
destinationZone = input('what is the destination zone?\n')
info.append(destinationZone)
port = input('what is the port being tested?\n')
info.append(port)


print('forward:')
print(' ')
print(f'test security-policy-match from {info[1]} source {info[0]} to {info[3]} destination {info[2]} destination-port {info[4]} protocol 6')
print(' ')
print('reverse:')
print(f'test security-policy-match from {info[3]} source {info[2]} to {info[1]} destination {info[0]} destination-port {info[4]} protocol 6')