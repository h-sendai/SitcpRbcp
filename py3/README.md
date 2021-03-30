# RBCP Libaray/command for python3

Yet another RBCP program using python3.

Library: SitcpRbcp.py

command line tool: cmdrbcp.py3

## cmdrbcp.py3 Setup

```
% git clone https://github.com/h-sendai/SitcpRbcp.git
```

Then create symbolic link file to cmdrbcp.py3
in the PATH searchable directory.
For example, if your PATH environment variable have
``$HOME/bin``; then

```
% cd $HOME/bin
% ln -s path/to/cmdrbcp.py3
% ls -l cmdrbcp.py3
```

### command line options

```
% cmdrbcp.py3 -h
usage: cmdrbcp.py3 [-h] [-d] [-q] [-t TIMEOUT] [-n BYTES_PER_LINE]
                   [-l FILENAME] [-i]
                   [ip_address] [port]

Yet another RBCP program using python3

positional arguments:
  ip_address            IP Address
  port                  Port Number

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           some debug printing
  -q, --quiet           do not print intro
  -t TIMEOUT, --timeout TIMEOUT
                        set timeout sec (default: 0.5 sec)
  -n BYTES_PER_LINE, --bytes-per-line BYTES_PER_LINE
                        print bytes per line in rd command (default: 8)
  -l FILENAME, --load FILENAME
                        non-interactive. Load this file and excute the
                        commands in that file
  -i, --interactive     After load and execute via -l option, switch to
                        interactive mode

Example:
% cmdrbcp.py3 -h
    display command usage, options and exit.
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

Use help or help <topic> command to get commands under interactive mode.
```

### interactive mode command

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
0x 01
RBCP> wrb 0xffffff10 0
RBCP> rd 0xffffff10 1
0x 00
RBCP> q
%
```

### Command line editing, command/filename completion and saving history

In interactive mode, like bash, you can edit the command line,
recall previous command by ctrl-p, incremental search by ctrl-s.
You can complete command or filename for load command by tab key.
Also command input in interactive mode will be saved in
~/.cmdrbcp_history.  This file will be read in the next invocation.
