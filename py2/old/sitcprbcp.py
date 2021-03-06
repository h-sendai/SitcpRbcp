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

import sys
import socket
import struct

def read_registers(ip_address, address, length, id = 1):
    """ Send read request to ip_address.
    Read timeout of the reply packet is 2 seconds (fixed).

    Parameters:
        ip_address
            IP address of the SiTCP equipment.
        address
            Register address.
        length
            Length of the registers to be read (by byte).
        id (optional)
            ID number of the RBCP.  If you omit this ID, 1 will be used.

    Return Value:
        Returns read data as python string.  You have to write decode
        routine as you like.
    
    Exception:
        Throw socket.error if socket error occurs.
        Throw VaeluError if RBCP violation occurs.

    Sample code 1:

    import socket # for "try read_registers()" timeout etc.
    import sitcprbcp

    try:
        data = read_registers('192.168.0.16', 0x80, 1)
    except socket.error, e:
        sys.exit(e)
    except:
        sys.exit('error')

    # struct.unpack() returns tuple (to get the first value, add [0]).
    register_value = struct.unpack('>B', data)[0]

    Sample code 2:

    import socket # for "try read_registers()" timeout etc.
    import sys
    import sitcprbcp

    try:
        data = read_registers('192.168.0.16', 0x80, 6, 100)
    except socket.error, e:
        sys.exit(e)
    except:
        sys.exit('error')

    for i in data:
        print '%02x' % (ord(i)),
    print

    """

    if length > 255:
        raise ValueError, 'Length too large: %d' % (length)
    if length <= 0:
        raise ValueError, 'Length too small: %d' % (length)

    try:
        rv = send_recv_command_packet('READ', ip_address, address, length, '', id)
    except:
        raise

    return rv

def write_registers(ip_address, address, length, data, id = 1, verify = 0):
    """ Send write request to ip_address.

    Parameters:
        ip_address
            IP address of the SiTCP equipment.
        address
            Register address.
        length
            Length of the registers to be written (by byte).
        data
            Python string to be written.
            Use struct.pack method to pack binary values (see sample code below).
        id (optional)
            ID number of the RBCP.  If you omit this ID, 1 will be used.
        verify (optional)
            You have to re-read the registers to lookup the write
            has been done successfully or not.  To re-read the registers,
            specify verify = 1.  Default is 0 (don't re-read).

    Return Values:
        Returns 0 if success.
        If error occurs, exception will be thrown.

    Exception:
        Throw socket.error if socket error occurs.
        Throw VaeluError if RBCP violation occurs.
        Throw VaeluError if re-read data does not match the orignal data.

    Sample code:

    import socket # for "try read_registers()" timeout etc.
    import struct # to pack binary data for write data
    import sys
    import sitcprbcp

    ip_address = '192.168.0.32'
    address    = 0x1ad
    length     = 1
    data       = struct.pack('>B', 0x20)
    id         = 100

    try:
        sitcprbcp.write_registers(ip_address, address, length, data, id, verify = 1)
    except socket.error, e:
        sys.exit(e)
    except ValueError, e:
        sys.exit(e)
    except:
        sys.exit('error')

    print 'OK'
    
    """
    if length > 255:
        raise ValueError, 'Length too large: %d' % (length)
    if length <= 0:
        raise ValueError, 'Length too small: %d' % (length)

    if len(data) != length:
        raise ValueError, 'Data length (%d) and Length (%d) does not match.' % (len(data), length)

    try:
        rv = send_recv_command_packet('WRITE', ip_address, address, length, data, id, verify)
    except:
        raise

    return rv

def send_recv_command_packet(command, ip_address, address, length, data, id, verify = 0):
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
        if verify != 0:
            try:
                re_read_data = read_registers(ip_address, address, length)
            except:
                raise
            for i in range (0, length):
                if data[i] != re_read_data[i]:
                    raise ValueError, 'orignal data and re-read data does not match'
    try:
        s.close()
    except socket.error, e:
        raise socket.error, e

    return 0

def main():
    data = read_registers('192.168.0.16', 0x80, 6, 100)
    for i in data:
        print '%02x' % (ord(i)),
    print
    
if __name__ == '__main__':
    main()
