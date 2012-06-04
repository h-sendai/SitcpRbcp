#!/usr/bin/env python

import sys

try:
    import sitcprbcp
except ImportError, e:
    print 'Error: need sitcprbcp python module'
    sys.exit(e)

def main():
    ip_address = '192.168.0.16'
    address    = 0x1ad
    length     = 1
    data       = '\x20'
    id         = 100

    if (sitcprbcp.write_registers(ip_address, address, length, data, id) < 0):
        print 'error'
    else:
        print 'OK'
    
if __name__ == '__main__':
    main()
