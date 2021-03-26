# RBCP Libaray/command for python3

Yet another RBCP program using python3.

Library: SitcpRbcp.py

command line tool: cmdrbcp.py3

## cmdrbcp.py3

### command line options

```
% cmdrbcp.py3 -h
usage: cmdrbcp.py3 [-h] [-d] [-l FILENAME] [-i] [ip_address] [port]

positional arguments:
  ip_address            IP Address
  port                  Port Number

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           debug (not used)
  -l FILENAME, --load FILENAME
                        non-interactive. Load this file and excute the
                        commands in that file
  -i, --interactive     After load and execute via -l option, switch to
                        interactive mode

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
```

### interactive shell mode command

```
% ./cmdrbcp.py3
Trying IP address: 192.168.10.16, Port: 4660
Type help to get available commands.  Type q to quit
help <command> displays each <command> help.  Example: help rd
command/filename completion by TAB key, history and command line editing available
Good luck!
RBCP> help

Documented commands (type help <topic>):
========================================
EOF  help  load  q  quit  rd  setip  setport  showipport  wr  wrb  wrs  wrw

RBCP> help wrb
Usage: wrb address data
       write one byte data to address
RBCP> help rd
Read a register and print its value in HEX.
Usage: rd address [length]
       default length is 1 bytes
RBCP> rd 0xffffff10 1
rd address 0xffffff10 (dec 4294967056), length 1
0x 01
RBCP> wrb 0xffffff10 0
wr address 0xffffff10 (dec 4294967056), data 0x0, format >B
RBCP> rd 0xffffff10 1
rd address 0xffffff10 (dec 4294967056), length 1
0x 00
RBCP> q
%
```
