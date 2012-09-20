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
