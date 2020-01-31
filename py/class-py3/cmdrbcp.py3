#!/usr/bin/env python3

import os
import sys
import time # for sleep
import cmd
import SitcpRbcp
import socket

target_ip_address = '192.168.10.16'
target_port       = 4660

class MyCmd(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'RBCP> '

    def print_hex(self, s):
        for i in s.split():
            print(i)
        
    ###### EOF command (C-d) ######
    def help_EOF(self):
        print('Quit this command (also C-d)')
    def do_EOF(self, line):
        sys.exit()

    ###### quit command ######
    def help_quit(self):
        print('Quit this command')
    def do_quit(self, line):
        sys.exit()

    ###### q command ######
#    def help_q(self):
#        print 'Quit this command'
#    def do_q(self, line):
#        sys.exit()
    do_q = do_quit
        
    ###### setip command ######
    def help_setip(self):
        print('Set ip address of the readout module.  current IP address %s' % target_ip_address)
    def do_setip(self, args):
        global target_ip_address
        if len(args.split()) == 0:
            print('Command Error: Need IP address to set')
            print('Usage: setip IP_ADDRESS (for example, setip 192.168.0.1)')
            return 0
        target_ip_address = args
        print('Set readout module IP address: %s' % target_ip_address)

    ###### setport command ######
    def help_setport(self):
        print('Set port of the readout module for RBCP.  current port is %d' % target_port)
    def do_setport(self, args):
        global target_port
        if len(args.split()) == 0:
            print('Command Error: Need port number to set')
            print('Usage: setport port (for example, setport 4601)')
            return 0
        target_port = int(args, 0)
        print('Set readout module port for RBCP: %d' % target_port)

    ###### showipport command ######
    def help_showipport(self):
        print('Print current readout module IP address and Port for RBCP')
    def do_showipport(self, args):
        self.print_hex('abcd')
        global target_ip_address
        global target_port
        print('Current IP address and port for RBCP: %s port %d' % (target_ip_address, target_port))

    ###### rd command ######
    def help_rd(self):
        print('Read register(s)')
        print('Usage: rd address [length]')
    def do_rd(self, args):
        n_args = len(args.split())
        if n_args == 1:
            address_string = args
            length_string  = '1'
        elif n_args == 2:
            address_string, length_string = args.split()
        else:
            print('Command Error: Too many arguments')
            print('Usage: rd address [length]')
            return 0

        address = int(address_string, 0)
        length  = int(length_string, 0)
        print('rd address 0x%0x (dec %d), length %d' % (address, address, length))
        rbcp = SitcpRbcp.SitcpRbcp()
        rbcp.set_timeout(0.5)
        try:
            data = rbcp.read_registers(target_ip_address, address, length)
        except socket.error as e:
            #sys.exit(e)
            print(e)
        except Exception as e:
            #sys.exit(e)
            print(e)
        else:
            for i in data:
                print('%02X' % i, end=' ')
            print()

    ###### wr command ######
    def help_wr(self):
        print('Write register(s)')
        print('Usage: wr address value [format] (length will be calculate automatically)')
        print('       You may prefix 0x (hex), 0b (bin)')
    def do_wr(self, args):
        n_args = len(args.split())
        if n_args == 2:
            address_string, value_string = args.split()
            format = '>B'
        elif n_args == 3:
            address_string, value_string, format = args.split()
        else:
            print('Comment Error: Too many arguments')
            print('Usage: wr address value [format]')
            print('If format is not specified, try to write as byte')
            return 0

        address = int(address_string, 0)
        value   = int(value_string, 0)
        print('wr address 0x%0x (dec %d), data 0x%0x, format %s' % (address, address, value, format))

def main():
    global target_ip_address
    global target_port
    if len(sys.argv) == 2:
        target_ip_address = sys.argv[1]
    if len(sys.argv) == 3:
        target_ip_address = sys.argv[1]
        target_port = int(sys.argv[2], 0)

    p = MyCmd()
    p.intro  = 'Trying IP address: %s, Port: %d\n' % (target_ip_address, target_port)
    p.intro += 'Type help to get available commands.  Type q to quit\n'
    p.intro += 'command completion by TAB key, history and command line editing available\n'
    p.intro += 'Good luck!'
    p.cmdloop()

if __name__ == '__main__':
    main()
