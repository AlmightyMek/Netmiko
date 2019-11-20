from netmiko import ConnectHandler
'''
Netmiko Documentation

https://github.com/ktbyers/netmiko/blob/develop/README.md
https://pynet.twb-tech.com/blog/automation/netmiko.html
========================================================

Purpose of this script:

This script connects to an IOS devie, opens a command file,
Runs the show commands in that file, and then prints the output
========================================================

__author__ = 'Emeka Nwangwu'
__author_email__ = 'enwangwu@cisco.com'
'''

#This is to verify we get an int for user_input_PORT

'''
Verifying Host Input

def verify_host_input(prompt_HOST):
    Calo_Locations = ["513E"]
    value_Host = strg(input(prompt_HOST))
    try:
        if any (value_Host in Calo_Locations == True
            return prompt_HOST
    else:
        print('Please enter a vaild location (513E, etc...)')
'''

def get_non_strg_int(prompt_PORT):
    while True:
        try:
            value_PORT = int(input(prompt_PORT))
        except ValueError:
            print("Sorry, I didn't understand that. Please enter an Interger!")
            continue
        except (KeyboardInterrupt, UnboundLocalError):
            print('\nKeyboard Interrupt Detected Exiting ...')
            exit()
        else:
            break
    return value_PORT

#Get user input to make the telnet connection
user_input_HOST = input("Enter the name of the COMM Server: ")
user_input_PORT = get_non_strg_int("Enter the COMM Port of the host: ")
user_input_PING = input("Enter the name of the interface you want to ping the FTP server from: ")

HOST = user_input_HOST
PORT = user_input_PORT
PING = user_input_PING

#Here we are parsing in device information needed for
#Netmiko to make a telnet connection

cisco_ios = {
    'device_type': 'cisco_ios_telnet',
    #'username': 'Mek',
    #'password': 'cisco',
    'host': HOST,
    'port': PORT,
    #'ip': '10.201.180.117'
    #'secret': ''
}

#This is to setup the connection to the devices
#Be sure to pass the devices name into the ConnectHandler()
net_connect = ConnectHandler(**cisco_ios)

#This will find then print the prompt of the device
prompt = net_connect.find_prompt()
print (prompt + '\n')

#This will open the config file then parse the lines into a list
#then we close the file with f.close()

with open('Verifications_IOS.txt') as f:
    verification_test = f.read().splitlines()

print('Perfoming device verification with the following commands...\n')

for k in range(len(verification_test)):
    print(verification_test[k])
print()
f.close()

#Here we are storing the list of commands from the txt file in a variable
show_commands = verification_test
send_ping = ('ping vrf ' + user_input_PING + ' 10.88.7.12')
output = ""

#This loops through the items in the list 'show_commands';
#Netmiko then sends the commands to the device with the .send_command() method

for i in range (len(show_commands)):
    print(net_connect.find_prompt())
    output = net_connect.send_command(show_commands[i])
    print (output + '\n')

print(net_connect.find_prompt())
output = net_connect.send_command(send_ping)
print(output + '\n')

net_connect.disconnect()
#output = net_connect.send_command(show_commands)

print("Verification Complete!")
exit()
