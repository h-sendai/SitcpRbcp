#!/usr/bin/env python3
import SitcpRbcp

def main():
    rbcp = SitcpRbcp.SitcpRbcp()
    #rbcp.set_veriy_mode()
    rbcp.set_timeout(1.0)
    data = rbcp.read_register_f('192.168.10.10', 0xffffff40, '>H')[0]
    print(data)

if __name__ == '__main__':
    main()
