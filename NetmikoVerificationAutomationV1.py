import netmiko
import GetUserInput
import signal
import sys
import json
import argparse
import os

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

    parser.add_argument('commands', action ='store',
    help = 'Location of the command file')

    #This is to make sure --vrf and --ping are not both used
    groups = parser.add_mutually_exclusive_group(required=False)

    groups.add_argument('--vrf', action = 'store_true', help =
    'Ping RCDNs FTP Server 10.88.7.12 using the Managment VRF, otherwise the default VRF will be used with --ping')

    groups.add_argument('--ping',action ='store_true', help =
    'Ping 10.88.7.12, the RCDN FTP Server')

    args = parser.parse_args()
    #mutal_error = parser.error('Cannot pass both --vrf and --ping, please choose one')

    #This will open the files parsed and store them in variables
    with open (args.commands) as cmd_file:
        commands = cmd_file.readlines()
        cmd_file.close()

    with open (args.devices) as dev_file:
        devices = json.load(dev_file)
        dev_file.close()

        vrf = args.vrf
        ping = args.ping

    return commands, devices, vrf, ping

def exception_catch():
    #Catching Netmiko netmiko_exceptions as well as Python Exceptions
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

    netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

    return netmiko_exceptions


def device_verification():
    #This is to setup the connection to the devices and loop through the commands
    #Be sure to pass the devices into the TelnetConnection()

    #Path for the NET_TEXTFSM templates

    #This will sepfiic how we ping the FTP server (10.88.7.12) based on the Parse


    for device in get_files()[1]:
        try:
            print('~' * 79)
            net_connect = netmiko.base_connection.TelnetConnection(**device)
            host_name = net_connect.set_base_prompt()

            print('\nConnecting to device: ' + host_name)


            for command in get_files()[0]:
                print('## Output of ' + command)
                print(net_connect.set_base_prompt() + '#')
                print(net_connect.send_command(command))
                print()

            #If vrf == True and --ping == False, we'll ping with the Mgmt Vrf for IOS

            if any (i['device_type'] == 'cisco_ios_telnet' and get_files()[2]
            == True for i in get_files()[1]):
                get_vrf = (net_connect.send_command('show vrf', use_textfsm=True))
                mgmt_vrf = get_vrf[0]['name']

                send_ping_vrf = (net_connect.send_command('ping vrf {} 10.88.7.12'.format(mgmt_vrf)))
                print('## Output of ' + 'ping vrf {} 10.88.7.12'.format(mgmt_vrf))
                print(net_connect.set_base_prompt() + '#')
                print(send_ping_vrf)

            #If vrf == False and --ping == True, we'll ping with the default Vrf for IOS

            elif get_files()[2]  == False and get_files()[3] == True:
                print('## Output of ping 10.88.7.12')
                print(net_connect.set_base_prompt() + '#')
                send_ping_default = (net_connect.send_command('ping 10.88.7.12'))
                print(send_ping_default)

            net_connect.disconnect()
            print("\nVerification Complete for {}".format(host_name) + "\n")

        except ConnectionRefusedError:
            print("No connection could be made because the target machine actively refused it. \
        Please clear the console lines of the devices and try again.")
            exit()

        except exception_catch()[0] as e:
            print('Failed to connect to ', device['host'], e)


def main():
    get_files()
    exception_catch()
    device_verification()


if __name__ ==  '__main__':
    main()
