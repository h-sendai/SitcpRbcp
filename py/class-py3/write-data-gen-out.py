#!/usr/bin/env python3
#!/usr/local/python3/bin/python3

# 10GbE TCP_TEST mode
# write 0x80 to address 0x5 

import os
import sys
import time
import argparse
import SitcpRbcp

def print_postion_args():
    global args
    print(args)

def main():
    rbcp = SitcpRbcp.SitcpRbcp()
    rbcp.set_verify_mode()
    rbcp.set_timeout(1.0)
    rbcp.write_register_f('192.168.10.10', 0x80, '>B', 0x80)

if __name__ == '__main__':
    main()
