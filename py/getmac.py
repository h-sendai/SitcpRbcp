#!/usr/bin/env python

import os
import sys
import time # for sleep
import socket
import struct

def main():
    ver_type = 0xff
    cmd_flag = 0xc0 # for read
    id       = 1
    length   = 6
    address  = 0x80 # NEUNET mac_address
    request_packet = struct.pack('>BBBBI', ver_type, cmd_flag, id, length, address)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.5)
    host = '192.168.0.16'
    port = 4660
    s.sendto(request_packet, (host, port))
    try:
        reply_packet = s.recvfrom(len(request_packet)+length)[0]
        # [1] contains (host, port)
    except socket.error, e:
        s.close()
        sys.exit(e)

    header = reply_packet[0:8]
    data   = reply_packet[8:]
    print 'header:',
    for i in header:
        print '%02x' % (ord(i)),
    print
    print 'data:',
    for i in data:
        print '%02x' % (ord(i)),
    print

    (reply_ver_type, reply_cmd_flag, reply_id, reply_length, reply_address) = struct.unpack('>BBBBI', header)
    print 'ver_type: 0x%02x' % (ver_type)
    print 'cmd_flag: 0x%02x' % (reply_cmd_flag)
    print 'id:       0x%02x' % (reply_id)
    print 'length:   0x%02x' % (reply_length)
    print 'address:  0x%08x' % (reply_address)
    format = '>%dB' % (len(data))
    data_tuple = struct.unpack(format, data)
    print 'data:    ',
    for i in data_tuple:
        print '%02x' % (i),

if __name__ == '__main__':
    main()
