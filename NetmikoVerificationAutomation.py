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

def get_non_strg_int(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Sorry, I didn't understand that. Please enter an Interger!")
            continue
        except (KeyboardInterrupt, UnboundLocalError):
            print('\nKeyboard Interrupt Dected Exiting ...')
            exit()
        else:
            break
    return value

#Get user input to make the telnet connection
user_input_HOST = input("Enter the name fo the COMM Server: ")
user_input_PORT = get_non_strg_int("Enter the COMM Port of the host: ")

HOST = user_input_HOST
PORT = user_input_PORT

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
output = ""

#This loops through the items in the list 'show_commands';
#Netmiko then sends the commands to the device with the .send_command() method

for i in range (len(show_commands)):
    print(net_connect.find_prompt())
    output = net_connect.send_command(show_commands[i])
    print (output + '\n')
net_connect.disconnect()
#output = net_connect.send_command(show_commands)

print("Verification Complete!")
