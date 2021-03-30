#!/usr/bin/env python3
#!/usr/local/python3/bin/python3

import os
import sys
import time
import argparse
import SitcpRbcp

def print_postion_args():
    global args
    print(args)

def main():
    global args

    parser = argparse.ArgumentParser(description = 'Write shaper bytes', 
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', 
                        '--tcp-payload',
                        dest = 'tcp_payload_MiB',
                        type = int,
                        help = 'setting value (MiB/s in TCP Payload) time')
    parser.add_argument('raw_value', type = int, nargs = '?')
    args = parser.parse_args()
    
    if not args.tcp_payload_MiB and not args.raw_value:
        parser.print_help()
        sys.exit(1)

    if args.tcp_payload_MiB:
        write_value = int(args.tcp_payload_MiB*1024*1024*8/1000/1000/0.9492)
    else:
        write_value = args.raw_value

    if write_value > 10000:
        sys.exit('Write value Too Large: %d' % (write_value))

    rbcp = SitcpRbcp.SitcpRbcp()
    rbcp.set_verify_mode()
    rbcp.set_timeout(1.0)
    rbcp.write_register_f('192.168.10.10', 0xffffff40, '>H', write_value)

if __name__ == '__main__':
    main()
