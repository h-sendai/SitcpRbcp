#!/usr/bin/env python

""" Python module to read/write SiTCP registers via RBCP

This module provides SiTCP registers read/write method via RBCP.
Speficication of RBCP (Remote Bus Control Protocol) is
available at the SiTCP Homepage (http://e-sys.kek.jp/tech/sitcp/).
"""

__all__     = ['read_registers', 'write_registers']
__author__  = 'Hiroshi Sendai'
__version__ = '0.00'
__date__    = 'June 4, 2012'

import os
import sys
import time # for sleep
import socket
import struct

def read_registers(ip_address, address, length, id = 1):
    """ Send read request to ip_address.  Register address is address,
    length of the registers is length.  You may specify optional RBCP id number.
    Returns register values as string.
    Read timeout of the reply packet is 2 seconds (fixed).
    Returns read bytes number if success.
    Throw exception (string) if errors.

    """

    try:
        rv = send_recv_command_packet('READ', ip_address, address, length, '', id)
    except:
        raise

    return rv

def write_registers(ip_address, address, length, data, id = 1):
    """ Send write request to ip_address.  You may specify optional RBCP id number.
    Read timeout of the reply packet is 2 seconds (fixed).
    Returns 0 if success.
    Throw exception (string) if errors.
    """

    try:
        rv = send_recv_command_packet('WRITE', ip_address, address, length, data, id)
    except:
        raise

    return rv

def send_recv_command_packet(command, ip_address, address, length, data, id):
    ver_type = 0xff
    if (command == 'READ'):
        cmd_flag = 0xc0 # for read
    elif (command == 'WRITE'):
        cmd_flag = 0x80
    else:
        raise ValueError, 'Unknown command (not READ nor WRITE) in send_recv_command_packet'
    request_packet = struct.pack('>BBBBI', ver_type, cmd_flag, id, length, address)
    if (command == 'WRITE'):
        request_packet += data

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)
    port = 4660
    s.sendto(request_packet, (ip_address, port))
    try:
        reply_packet = s.recvfrom(len(request_packet)+length)[0]
        # [1] contains (host, port)
    except socket.error, e:
        s.close()
        raise socket.error, e

    reply_header = reply_packet[0:8]
    reply_data = reply_packet[8:]
    
    # check reply header 
    (reply_ver_type, reply_cmd_flag, reply_id, reply_length, reply_address) = \
        struct.unpack('>BBBBI', reply_header)
    if (reply_ver_type != 0xff):
        raise ValueError, 'reply packet Ver/Type is not 0xff'
    ackbit_mask = 0x80
    if ((reply_cmd_flag & ackbit_mask) != ackbit_mask):
        raise ValueError, 'reply packet does not have ackbit'
    if (reply_length != length):
        raise ValueError, 'reply length does not match with original length'
    if (reply_address != address):
        raise ValueError, 'reply address does not match with original address'

    # READ Command
    if (command == 'READ'):
        return reply_data

    # WRITE Command
    if (command == 'WRITE'):
        for i in range(0, length):
            if data[i] != reply_data[i]:
                raise ValueError, 'orignal data and reply data does not match.'
        # Re-read and verify
        try:
            re_read_data = read_registers(ip_address, address, length)
        except:
            raise
        for i in range (0, length):
            if data[i] != re_read_data[i]:
                raise ValueError, 'orignal data and re-read data does not match'
        return 0

def main():
    data = read_registers('192.168.0.16', 0x80, 6, 100)
    for i in data:
        print '%02x' % (ord(i)),
    print
    
if __name__ == '__main__':
    main()
