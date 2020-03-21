# network-automation

This scripts connnects to a Cisco device from a file, (other vendros should work) using netmiko, then run the commands from anotehr file that is speciied in the command line.

usage: NetmikoVerificationAutomationV1.py [-h] [--ping] devices commands

Script to connect to cisco devices and run show commands

positional arguments:
  devices     Name of the device file
  commands    Name of the command file

Ex Output : 

'''
## Output of show ver | inc image [513E.B.03-3800-01]
System image file is "flash:cat3k_caa-universalk9.16.09.04.SPA.bin"

## Output of show ip int br | inc up [513E.B.03-3800-01]

## Output of show cdp ne [513E.B.03-3800-01]
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone, 
                  D - Remote, C - CVTA, M - Two-port Mac Relay 

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID

Total cdp entries displayed : 0
'''

Afterwards it writes the output of these commands to a txt file in the directory that you run the script from.

Next feautrse will be the ability to add config commands. 
