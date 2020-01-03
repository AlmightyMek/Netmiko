import netmiko
import signal
import sys
import json
import argparse
import os
from datetime import datetime
import concurrent.futures

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
then excutes a ping to the FTP Server in requsted

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
    help = 'Name of the device file')

    parser.add_argument('commands', action ='store',
    help = 'Name of the command file')

    #This is to make sure --vrf and --ping are not both used
    groups = parser.add_mutually_exclusive_group(required=False)

    #groups.add_argument('--vrf', action = 'store_true', help =
    #'Ping RCDNs FTP Server 10.88.7.12 using the Managment VRF, otherwise the default VRF will be used with --ping')

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

        #vrf = args.vrf
        ping = args.ping

    return commands, devices, ping

def exception_catch():
    #Catching Netmiko netmiko_exceptions as well as Python Exceptions
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

    netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

    return netmiko_exceptions

def ping_vrf(get_vrf):
    mgmt_vrf = get_vrf[0]['name']
    send_ping_vrf = ('ping vrf {} 10.88.7.12'.format(mgmt_vrf))

    return send_ping_vrf

def device_verification(devices):
    #This is the main func to setup the connection to the devices and loop through the commands
    #Be sure to pass the devices into the TelnetConnection()

        try:
            print('~' * 79)
            net_connect = netmiko.base_connection.TelnetConnection(**devices)
            host_name = net_connect.set_base_prompt()

            print('\nConnecting to device: ' + host_name)

            #Here we loop through the command file and print the output
            verification_output_filename = ('verification-{}'.format(host_name))
            print('Writing the output of the show commands to ' + verification_output_filename + '.txt')
            print()

            with open(verification_output_filename + '.txt', 'w') as verification_file:
                for command in get_files()[0]: #Commands
                    verification_file.write('## Output of ' + command + '\n\n')
                    verification_file.write(net_connect.send_command(command) + '\n\n')


                #ping_logic handels the commands needed to ping the FTP server
                #If ping == True then we'll call the ping_logic func
                     #Ping
                if get_files()[2] == True:
                    verification_file.write('## Output of ' + 'ping 10.88.7.12' '\n\n')
                    verification_file.write(ping_logic(net_connect))

            net_connect.disconnect()
            print("Verification Complete for {}".format(host_name) + "\n")

        except ConnectionRefusedError:
            print('''No connection could be made because the target machine actively refused it.\n
            Please clear the console lines of the devices and try again''')
            exit()

        except exception_catch()[0] as e:
            print('Failed to connect to ', device['host'], e)

            return net_connect


def ping_logic(net_connect,ping=get_files()[2]):

    #With the list comp we are checking for the IOS device type and the running the commands accordingly
    #Will need to add slighty differnet commands depending on the OS

    if any (d['device_type'] == 'cisco_ios_telnet' for d in get_files()[1]):

        #ping_vrf will handle the vrf commands

        get_vrf = net_connect.send_command('show vrf', use_textfsm=True)
        output_send_ping_vrf = net_connect.send_command(ping_vrf(get_vrf))
        return output_send_ping_vrf

        #Otherwise we ping via the default vrf

    if any ('0/') in output_send_ping_vrf:
        output_send_ping_default = net_connect.send_command('ping 10.88.7.12')
        return output_send_ping_default


def main():
    startTime = datetime.now()

    get_files()
    exception_catch()

    #This will open mulitple threads for the device_verification func and loop through the devices

    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.map(device_verification, get_files()[1])

    total_time = (datetime.now() - startTime)
    print()

    print('~' * 79)
    print('Script took {}'.format(total_time) + ' to complete')
    print('~' * 79)

if __name__ ==  '__main__':
    main()
