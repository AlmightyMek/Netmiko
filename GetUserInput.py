import telnetlib
import sys
import json

#These methods collect user input

def get_files():

    try:
        if len(sys.argv) < 3:
            print('Usage: Auto.py commands.txt devices.json')
            exit()

        with open(sys.argv[1]) as cmd_file:
            commands = cmd_file.readlines()
            cmd_file.close()

        with open(sys.argv[2]) as dev_file:
            devices = json.load(dev_file)
            dev_file.close()

    except KeyboardInterrupt:
            print('Exiting ...')
            exit()
    return commands, devices


def get_ping():
    while True:
        try:
            user_input_PING = input('Enter the name of the interface you want to ping the FTP server from. Type ("skip") to skip: ')
            PING = user_input_PING
            skip = ['skip','Skip','SKIP']

        except KeyboardInterrupt:
            print('Exiting ...')
            exit()
        else:
            break
    return (PING, skip)
