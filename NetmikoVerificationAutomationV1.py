import netmiko
import signal
import sys
import json
import argparse
import os
from datetime import datetime
from multiprocessing import Process

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


def device_verification(commands, devices, vrf, ping):
    #This is the main func to setup the connection to the devices and loop through the commands
    #Be sure to pass the devices into the TelnetConnection()

    for device in devices:
        try:
            print('~' * 79)
            net_connect = netmiko.base_connection.TelnetConnection(**device)
            host_name = net_connect.set_base_prompt()

            print('\nConnecting to device: ' + host_name)

            #Here we loop through the command file and print the output

            for command in commands:
                print('## Output of ' + command)
                print(net_connect.set_base_prompt() + '#')
                print(net_connect.send_command(command))
                print()

                #If vrf == True and --ping == False, we'll ping with the Mgmt Vrf for IOS
                #We call the ping_vrf() func for the command to run

            if any (i['device_type'] == 'cisco_ios_telnet' and vrf == True for i in devices):

                get_vrf = (net_connect.send_command('show vrf', use_textfsm=True))
                output_send_ping_vrf = net_connect.send_command(ping_vrf(get_vrf))

                print('## Output of ' + 'ping vrf {} 10.88.7.12'.format(get_vrf[0]['name']))
                print(net_connect.set_base_prompt() + '#')
                print(output_send_ping_vrf)

                #If vrf == False and --ping == True, we'll ping with the default Vrf for IOS

            elif  vrf == False and ping == True:

                print('## Output of ping 10.88.7.12')
                print(net_connect.set_base_prompt() + '#')
                output_send_ping_default = (net_connect.send_command('ping 10.88.7.12'))
                print(output_send_ping_default)

            net_connect.disconnect()
            print("\nVerification Complete for {}".format(host_name) + "\n")

        except ConnectionRefusedError:
            print('''No connection could be made because the target machine actively refused it.\n
            Please clear the console lines of the devices and try again''')
            exit()

        except exception_catch()[0] as e:
            print('Failed to connect to ', device['host'], e)

            return

def ping_vrf(get_vrf):
    mgmt_vrf = get_vrf[0]['name']
    send_ping_vrf = ('ping vrf {} 10.88.7.12'.format(mgmt_vrf))

    return send_ping_vrf


def main():
    startTime = datetime.now()

    get_files()
    exception_catch()
    device_verification(get_files()[0],get_files()[1],get_files()[2],get_files()[3])
    #proc = Process(target=device_verification, args=(get_files()[0],get_files()[1],get_files()[2],get_files()[3]))
    #proc.start()
    total_time = (datetime.now() - startTime)
    print()

    print('~' * 79)
    print('Script took {}'.format(total_time) + ' to complete')
    print('~' * 79)

if __name__ ==  '__main__':
    main()
