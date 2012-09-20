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
