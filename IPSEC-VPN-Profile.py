#!//usr/bin/python3

#=====================
# DH_group_choice 
DH_Group =  {
    "1" : "no-pfs",
    "2" : "group1",
    "3" : "group2",
    "4" : "group5",
    "5" : "group14",
    "6" : "group15",
    "7" : "group16",
    "8" : "group19",
    "9" : "group20",
    "10" : "group21",
}

print('The Following are the options for DH group:')
print('''
  choice#:  group:
  --------  ------
    1       no-pfs
    2       group1
    3       group2
    4       group5
    5       group14
    6       group15
    7       group16
    8       group19
    9       group20
    10      group21
  ''')

dh_choice = input('what is the choice# for DH group?\n')

if dh_choice in DH_Group:
    dh_answer = DH_Group[dh_choice]
    print(f"You selected: {dh_answer}")
    print('')
    if dh_answer == 'no-pfs':
        dh_name = 'no-pfs'
    elif dh_answer == 'group1':
        dh_name = 'DH1'
    elif dh_answer == 'group2':
        dh_name = 'DH2'
    elif dh_answer == 'group5':
        dh_name = 'DH5'
    elif dh_answer == 'group14':
        dh_name = 'DH14'
    elif dh_answer == 'group15':
        dh_name = 'DH15'
    elif dh_answer == 'group16':
        dh_name = 'DH16'
    elif dh_answer == 'group19':
        dh_name = 'DH19'
    elif dh_answer == 'group20':
        dh_name = 'DH20'
    elif dh_answer == 'group21':
        dh_name = 'DH21'
else:
    print("Invalid choice. please start over")
    exit()

#======================
# AUTH_Group section
AUTH_Group = {
'1' : 'md5',
'2' : 'sha1',
'3' : 'sha256',
'4' : 'sha384',
'5' : 'sha512' 
}

print('The following are the options for Authentication/hash:')
print('''
  choice#:  Auth method
  -----     -----
    1       md5
    2       sha1
    3       sha256
    4       sha384
    5       sha512
  ''')
auth_choice = input('what is your choice# for authentication method?\n')

if auth_choice in AUTH_Group:
    auth_answer = AUTH_Group[auth_choice]
    print(f"You selected: {auth_answer}")
    print('')
else:
    print("invalid choice. please start over")
    exit()

#======================
# Encryption section

Encry_Group = {
    '1' : '3des',
    '2' : 'aes128-cbc',
    '3' : 'aes192-cbc',
    '4' : 'aes-256-cbc',
    '5' : 'aes-128-gcm',
    '6' : 'aes-256-gcm'
}

print('The following are the options for Encrytion:')
print('''

 choice#:  Encryption method
 --------  -----------------
    1      3des
    2      aes-128-cbc
    3      aes-192-cbc
    4      aes-256-cbc
    5      aes-128-gcm
    6      aes-256-gcm

''')

encry_choice = input('what is your chice# for encryption method?\n')

if encry_choice in Encry_Group:
    encry_answer = Encry_Group[encry_choice]
    print(f"You selected: {encry_answer}")
    print('')
    if encry_answer == '3des':
        encry_name = '3DES'
    elif encry_answer == 'aes-128-cbc':
        encry_name = 'AES128'
    elif encry_answer == 'aes-192-cbc':
        encry_name = 'AES192'
    elif encry_answer == 'aes-256-cbc':
        encry_name = 'AES256'
    elif encry_answer == 'aes-128-gcm':
        encry_name = 'AES128gcm'
    elif encry_answer == 'aes-256-gcm':
        encry_name = 'AES256gcm'
else:
    print("invalid choice. please start over")
    exit()

#================
#Life time section

lifetime_options = {
'1':'hours 24',
'2':'hours 8',
'3':'hours 4',
'4':'hours 1'
}

print('''specify the life time in hours. the follwing is a simple conversion

  choice#    hours     seconds
  --------   -------   --------
     1       24 hours  86400
     2       8 hours   28800
     3       4 hours   14400
     4       1 hour    3600
''')

lifetime_choice = input('enter your choice for lifetime in hours?\n')

if lifetime_choice in lifetime_options:
    lt_answer = lifetime_options[lifetime_choice]
    print(f"You selected: {lt_answer}")
    print('')
    if lt_answer == 'hours 24':
        lt_name = '24Hr'
    elif lt_answer == 'hours 8':
        lt_name = '8Hr'
    elif lt_answer == 'hours 4':
        lt_name = '4Hr'
    elif lt_answer == 'hours 1':
        lt_name = '1Hr'
else:
    print("invalid choice. please start over")
    exit()

print(f'''here is your set selection:
    DH Group - {dh_answer}
    Encryption selection - {encry_answer}
    Authentication - {auth_answer}
    Lifetime - {lt_answer}
''')

ike_set_name = (f'{encry_name}-{auth_answer}-{dh_name}-{lt_name}')

final_set = input(' do these settings look ok for the tunnel ikev2 settings? (Yes/No)\n')
if 'Yes' in final_set:
    print(f'your new set will be named: {ike_set_name}')
elif 'yes' in final_set:
    print(f'your new set will be named: {ike_set_name}')
else:
    print('please run the script again')

print(' ')
print('* here is your Ike set configuration:')
print(' ')
print (f'set network ike crypto-profiles ipsec-crypto-profiles {ike_set_name.upper()} esp authentication {auth_answer}')
print (f'set network ike crypto-profiles ipsec-crypto-profiles {ike_set_name.upper()} dh-group {dh_answer}')
print (f'set network ike crypto-profiles ipsec-crypto-profiles {ike_set_name.upper()} esp encryption {encry_answer}')
print (f'set network ike crypto-profiles ipsec-crypto-profiles {ike_set_name.upper()} lifetime {lt_answer}')
