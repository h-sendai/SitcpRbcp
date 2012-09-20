#!/usr/bin/env python

import sys
import struct
import socket # for try write_registers socket error

try:
    import sitcprbcp
except ImportError, e:
    print 'Error: need sitcprbcp python module'
    sys.exit(e)

def main():
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
        
    
if __name__ == '__main__':
    main()
