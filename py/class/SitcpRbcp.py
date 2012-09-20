#!/usr/bin/env python

r"""Slow control module for SiTCP

This module allows you to use SiTCP RBCP (Remote Bus Control Protocol).
The specification of the SiTCP RBCP is avaiable at
http://http://e-sys.kek.jp/tech/sitcp/

Sample code for read:

#!/usr/bin/env python

import sys
import socket
import SitcpRbcp

def main():
    rbcp = SitcpRbcp.SitcpRbcp()
    rbcp.set_timeout(0.5)
    ip_address = '192.168.0.32'
    try:
        mac_address = rbcp.read_registers(ip_address, address = 0x80, length = 6)
    except socket.error, e:
        sys.exit(e)
    except Exception, e:
        sys.exit(e)
    else:
        print ip_address,
        for i in mac_address:
            print '%02X' % (ord(i)),
        print

if __name__ == '__main__':
    main()

Sample code for write:

#!/usr/bin/env python

import sys
import socket
import struct
import SitcpRbcp

def main():
    rbcp = SitcpRbcp.SitcpRbcp()
    rbcp.set_verify_mode()
    rbcp.set_timeout(0.5)
    ip_address = '192.168.0.32'
    speed_data = struct.pack('>B', 0x20)

    try:
        rbcp.write_registers(ip_address, address = 0x1ad, length = 1, id = 10, data = speed_data)
    except socket.error, e:
        sys.exit(e)
    except Error, e:
        sys.exit('error')
    else:
        print "speed data write done"

if __name__ == '__main__':
    main()

"""

import sys
import socket
import struct

class SitcpRbcp:
    "SitcpRbcp (slow control) class"

    def __init__(self):
        self.verify_on_write = False
        self.verbose         = False
        self.timeout         = 2.0

    def set_timeout(self, timeout):
        self.timeout = timeout

    def set_verbose(self):
        """Set verbose mode"""
        self.verbose = True

    def unset_verbose(self):
        self.verbose = False

    def set_verify_mode(self):
        self.verify_on_write = True

    def unset_verify_mode(self):
        self.verify_on_write = False

    def _send_recv_command_packet(self, command, ip_address, address, length, id, data = ''):
        ver_type = 0xff
        if (command == 'READ'):
            cmd_flag = 0xc0
        elif (command == 'WRITE'):
            cmd_flag = 0x80
        else:
            raise ValueError, \
            'Unknown command in _send_recv_command_packet.  \
This is a bug of the SitcpRbcp module (not a bug of user program)'
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error, e:
            raise socket.error, e
        request_packet = struct.pack('>BBBBI', ver_type, cmd_flag, id, length, address)
        if command == 'WRITE':
            request_packet += data

        s.settimeout(self.timeout)
        port = 4660

        try:
            s.sendto(request_packet, (ip_address, port))
        except socket.error, e:
            raise socket.error, e

        try:
            reply_packet = s.recvfrom(len(request_packet) + length)[0]
            # [1] contains (host, port) tuple
        except socket.error, e:
            s.close()
            raise socket.error, e

        reply_header = reply_packet[0:8]
        reply_data   = reply_packet[8:]

        # check reply header
        (reply_ver_type, reply_cmd_flag, reply_id, reply_length, reply_address) = \
            struct.unpack('>BBBBI', reply_header)
        if reply_ver_type != 0xff:
            raise ValueError, 'reply packet Ver/Type is not 0xff (but %02x)' % (reply_ver_type)
        ackbit_mask = 0x80
        if (reply_cmd_flag & ackbit_mask) != ackbit_mask:
            raise ValueError, 'reply packet does not have Ack bit'
        if reply_length != length:
            raise ValueError, 'reply length (%d) does not match with the request length (%d)' % (reply_length, length)
        if reply_address != address:
            raise ValueError, 'reply address (%08x) does not match with the request address (%08x)' % (reply_address, address)
            
        if command == 'READ':
            return reply_data

        if command == 'WRITE':
            for i in range(0, length):
                if data[i] != reply_data[i]:
                    raise ValueError,\
                        'original data and reply data does not match: orig: %02x, reply: %02x' \
                        % (data[i], reply_data[i])
                if self.verify_on_write:
                    if self.verbose:
                        sys.stderr.write('verify mode on')
                    try:
                        re_read_data = self.read_registers(ip_address, address, length)
                    except:
                        raise
                    for i in range (0, length):
                        if data[i] != re_read_data[i]:
                            raise ValueError,\
                            'original data and reply data does not match: orig: %02x, reply: %02x' \
                            % (data[i], re_read_data[i])
        try:
            s.close()
        except socket.error, e:
            raise socket.error, e

    def read_registers(self, ip_address, address, length, id = 1):
        #self.ip_address = ip_address
        #self.address    = address
        #self.length     = length
        #self.id         = id
        if self.verbose:
            print 'ip_address: %s, address: %d, length: %d, timeout: %.3f ' % \
                (ip_address, address, length, self.timeout)
                #(self.ip_address, self.address, self.length, self.timeout)
        data = self._send_recv_command_packet('READ', ip_address, address, length, id)
        return data

    def write_registers(self, ip_address, address, length, id = 1, data = ''):
        #self.ip_address = ip_address
        #self.address    = address
        #self.length     = length
        #self.id         = id
        #self.data       = data
        if self.verbose:
            print 'ip_address: %s, address: %d, length: %d, timeout: %.3f ' % \
                (ip_address, address, length, self.timeout)
        #self._send_recv_command_packet('READ', self.ip_address, self.address, self.length, self.id, self.data)
        self._send_recv_command_packet('WRITE', ip_address, address, length, id, data)
        return 0
        
def main():
    rbcp = SitcpRbcp()
    rbcp.set_verify_mode()
    #rbcp.set_verbose()
    rbcp.set_timeout(0.5)
    ip_address = '192.168.0.32'
#    try:
#        mac_address = rbcp.read_registers(ip_address, address = 0x80, length = 6)
#    except socket.error, e:
#        sys.exit(e)
#    except Exception, e:
#        sys.exit(e)
#    else:
#        for i in mac_address:
#            print '%02X' % (ord(i)),
#        print
    speed_data = struct.pack('>B', 0x20)
    try:
        rbcp.write_registers(ip_address, address = 0x1ad, length = 1, id = 10, data = speed_data)
    except socket.error, e:
        sys.exit(e)
    except Error, e:
        sys.exit('error')
    else:
        print "speed data write done"

if __name__ == '__main__':
    main()
