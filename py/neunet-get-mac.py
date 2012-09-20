#!/usr/bin/env python

import sys

try:
    import sitcprbcp
except ImportError, e:
    print 'Error: need sitcprbcp python module'
    sys.exit(e)

def main():
    ip_address = '192.168.0.32'
    address    = 0x80
    length     = 6
    id         = 100

    data = sitcprbcp.read_registers(ip_address, address, length, id)
    for i in data:
        print '%02x' % (ord(i)),
    print
    
if __name__ == '__main__':
    main()
