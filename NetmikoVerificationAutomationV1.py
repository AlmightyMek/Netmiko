import netmiko
import GetUserInput
import signal
import sys
import json
import argparse

'''
Netmiko Documentation

https://github.com/ktbyers/netmiko/blob/develop/README.md
https://pynet.twb-tech.com/blog/automation/netmiko.html
========================================================
Grellem Youtube Script
https://github.com/grelleum/youtube-network-automation/blob/
master/08.Completing_Command_Runner/v1.Output_to_Screen/cmdrunner.py#L23
========================================================

Purpose of this script:

This script connects to an IOS devie, opens a command file,
then excutes a ping to the FTP Server

Then it Runs the show commands in that file, and then prints the output
========================================================

__author__ = 'Emeka Nwangwu'
__author_email__ = 'enwangwu@cisco.com'
'''

#Get user input from the ArgumentParser, then use
# the filse to make the telnet connections with Netmiko

def get_files():
    parser = argparse.ArgumentParser(description='''Script to connect
    to cisco devices and run show commands''')

    parser.add_argument('devices', action='store',
    help = 'Location of device file')
    parser.add_argument('commands', action='store',
    help = 'Location of the command file')

    args = parser.parse_args()
    #This will open the files parsed and store them in variables
    with open (args.commands) as cmd_file:
        commands = cmd_file.readlines()
        cmd_file.close()

    with open (args.devices) as dev_file:
        devices = dev_file.readlines()
        dev_file.close()

    return commands, devices

def exception_catch():
    #Catching Netmiko netmiko_exceptions as well as Python Exceptions
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

    netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

def device_verification():
    #This is to setup the connection to the devices and loop through the commands
    #Be sure to pass the devices into the TelnetConnection()

    for device in get_files()[1]:
        try:
            print('~' * 79)
            net_connect = netmiko.base_connection.TelnetConnection(**device)
            print('Connecting to device: ' + (net_connect.set_base_prompt()))
            #PING = GetUserInput.get_ping()[0]
            #send_ping = 'ping vrf {} 10.88.7.12'.format(PING)

            for command in get_files()[0]:
                print('## Output of ' + command)
                print(net_connect.set_base_prompt() + '#')
                print(net_connect.send_command(get_files()[0]))
                print()

            #if PING not in GetUserInput.get_ping()[1]:
                #print(net_connect.set_base_prompt() + '#')
                #print(net_connect.send_command(send_ping))

            #else:
                #pass

            net_connect.disconnect()
            print("\nVerification Complete!")

        except ConnectionRefusedError:
            print("No connection could be made because the target machine actively refused it. \
        Please clear the console lines of the devices and try again.")
            exit()

        except netmiko_exceptions as e:
            print('Failed to connect to ', device['host'], e)

def main():
    get_files()
    exception_catch()
    device_verification()

if __name__ ==  '__main__':
    main()
