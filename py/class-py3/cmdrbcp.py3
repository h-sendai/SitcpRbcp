#!/usr/bin/env python3

import os
import sys
import time # for sleep
import cmd
import SitcpRbcp
import socket
import glob
import argparse
import signal

target_ip_address = '192.168.10.16'
target_port       = 4660

# _append_slash_if_dir():
# use in complete_load() (load command filename completion)
# From stackovewflow: https://stackoverflow.com/questions/16826172/
#                     https://stackoverflow.com/a/27256663
# Question by jinserk: https://stackoverflow.com/users/2392124/jinserk
# Answer by meffie: https://stackoverflow.com/users/1070181/meffie
# CC BY-SA 3.0 https://creativecommons.org/licenses/by-sa/3.0/
def _append_slash_if_dir(p):
    if p and os.path.isdir(p) and p[-1] != os.sep:
        return p + os.sep
    else:
        return p

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
    def help_q(self):
        print('Quit this command')
    def do_q(self, line):
        sys.exit()
    #do_q = do_quit
        
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
        # self.print_hex('abcd')
        global target_ip_address
        global target_port
        print('Current IP address and port for RBCP: %s port %d' % (target_ip_address, target_port))

    ###### rd command ######
    def help_rd(self):
        print('Read a register and print its value in HEX.')
        print('Usage: rd address [length]')
        print('       default length is 1 bytes')
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
            print('0x ', end = '')
            for i in data:
                print('%02X' % i, end=' ')
            print()

    ###### wr command ######
    def help_wr(self):
        print('Write to a register')
        print('Usage: wr address value [format] (length will be calculate according to format automatically)')
        print('       You may prefix 0x (hex), 0b (bin)')
        print('       format is a python struct package format chars')
        print('Example: wr 0x0 0x01    will try to write address 0x0, value 0x01')
        print('         wr 0x0 0x01 >B will try to write address 0x0, value 0x01')
        print('         wr 0x0 0x01 >I will try to write address 0x0, value 0x00000001 (>I: as int. 4 bytes)')
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
        rbcp = SitcpRbcp.SitcpRbcp()
        #rbcp.set_verify_mode()
        rbcp.set_timeout(0.5)
        try:
            rbcp.write_register_f(target_ip_address, address, format, value)
        except socket.error as e:
            print(e)
        except Exception as e:
            print(e)

    ##### wrb command #####
    def help_wrb(self):
        print('Usage: wrb address data')
        print('       write one byte data to address')
    def do_wrb(self, args):
        n_args = len(args.split())
        if n_args != 2:
            print('usage: wrb address byte_data')
            return 0
        address, value_string = args.split()
        self.do_wr(args + ' >B')

    ##### wrs command #####
    def help_wrs(self):
        print('Usage: wrs address data')
        print('       write one short bytes (2 bytes) to address')
    def do_wrs(self, args):
        n_args = len(args.split())
        if n_args != 2:
            print('usage: wrs address byte_data')
            return 0
        address, value_string = args.split()
        self.do_wr(args + ' >H')

    ##### wrw command #####
    def help_wrw(self):
        print('Usage: wrw address data')
        print('       write one word bytes (4 bytes) to address')
    def do_wrw(self, args):
        n_args = len(args.split())
        if n_args != 2:
            print('usage: wrw address byte_data')
            return 0
        address, value_string = args.split()
        self.do_wr(args + ' >I')

    ##### load command #####
    def help_load(self):
        print('load file and execute the lines')
        print('Usage: load filename')
        print('       read filename and excute it as if typed on the prompt line.')
        print('       Lines start with "#" in the file will be ignored (comment).')
        print('       You can complete the filename by hitting TAB.')
    def do_load(self, args):
        with open(args, 'r') as f:
            for line in f:
                if line[0] == '#': # comment
                    continue
                cmd.Cmd.onecmd(self, line)

    ##### load filename completion #####
    # complete_load():
    # From stackovewflow: https://stackoverflow.com/questions/16826172/
    #                     https://stackoverflow.com/a/27256663
    # Question by jinserk: https://stackoverflow.com/users/2392124/jinserk
    # Answer by meffie: https://stackoverflow.com/users/1070181/meffie
    # CC BY-SA 3.0 https://creativecommons.org/licenses/by-sa/3.0/
    def complete_load(self, text, line, begidx, endidx):
        before_arg = line.rfind(" ", 0, begidx)
        if before_arg == -1:
            return # arg not found

        fixed = line[before_arg+1:begidx]  # fixed portion of the arg
        arg = line[before_arg+1:endidx]
        pattern = arg + '*'

        completions = []
        for path in glob.glob(pattern):
            path = _append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))
        return completions

    # Don't re-execute previous command if enter empty lines
    # From stackovewflow: https://stackoverflow.com/questions/16479029/
    #                     https://stackoverflow.com/a/21066546
    # Question by Fatih Karatana: https://stackoverflow.com/users/209623/fatih-karatana
    # Answer by John Doe: https://stackoverflow.com/users/1987886/john-doe
    # CC BY-SA 3.0 https://creativecommons.org/licenses/by-sa/3.0/
    def emptyline(self):
        pass

def sig_int(signo, frame):
    sys.exit(0)

def main():
    global target_ip_address
    global target_port
    global cmdline_options

    signal.signal(signal.SIGINT, sig_int)

    cmd_example = '''
Example:
% cmdrbcp.py3
    interactive command.  Use 192.168.10.16 and port 4660.
% cmdrbcp.py3 192.168.10.10
    interactive command.  Use 192.168.10.10 and port 4660.
% cmdrbcp.py3 192.168.10.10 4559
    interactive command.  Use 192.168.10.10 and port 4559.
% cmdrbcp.py3 -l cmd.txt
    non-interactive command.  Read cmd.txt and execute it,
    then exit.
% cmdrbcp.py3 -l cmd.txt -i
    Read cmd.txt and execute it, then switch to interactive mode.

Use help or help <topic> command to get commands under interactive shell.
'''

    parser = argparse.ArgumentParser(description = 'Yet another RBCP program using python3',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog = cmd_example)
    parser.add_argument('-d',
                        '--debug',
                        dest = 'debug',
                        action = 'store_true',
                        help = 'debug (not used)')
    parser.add_argument('-l',
                        '--load',
                        dest = 'filename',
                        type = str,
                        help = 'non-interactive.  Load this file and excute the commands in that file')
    parser.add_argument('-i',
                        '--interactive',
                        dest = 'interactive',
                        action = 'store_true',
                        help = 'After load and execute via -l option, switch to interactive mode')
    parser.add_argument(dest = 'ip_address',
                        type = str,
                        nargs = '?',
                        default = '192.168.10.16',
                        help = 'IP Address')
    parser.add_argument(dest = 'port',
                        type = int,
                        nargs = '?',
                        default = 4660,
                        help = 'Port Number')

    command_options = parser.parse_args()
    
    target_ip_address = command_options.ip_address
    target_port       = command_options.port

    p = MyCmd()
    if command_options.filename:
        p.do_load(command_options.filename)
        if command_options.interactive:
            pass
        else:
            sys.exit(0)

    # then enter/switch to interactive mode
    p.intro  = 'Trying IP address: %s, Port: %d\n' % (target_ip_address, target_port)
    p.intro += 'Type help to get available commands.  Type q to quit\n'
    p.intro += 'help <command> displays each <command> help.  Example: help rd\n'
    p.intro += 'command/filename completion by TAB key, history and command line editing available\n'
    p.intro += 'Good luck!'
    p.cmdloop()

if __name__ == '__main__':
    main()
