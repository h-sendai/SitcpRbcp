#!/usr/bin/env python
# coding: utf-8

import sys
import os
import struct
import sitcprbcp

DEFAULT_IP = '192.168.10.10'
DEFAULT_PORT = '4660'

def rbcp_help():
    print 'Command list\n'
    print 'wrb [address] [byte_data]          : Write byte'
    print 'wrs [address] [short_data]         : Write short(16bit)'
    print 'wrw [address] [word_data]          : Write word(32bit)'
    print 'rd [address] [length]              : Read data'
    print 'rdd [address] [length] [file name] : Read data with a dump file'
    print 'load [file name]                   : Execute a script'
    print 'quit                               : quit from this program\n'
    return

def get_addr_data(cmdLine):
    cmdLine = cmdLine.strip()
    tempList = cmdLine.split(' ')
    cmdLine = []
    for s in tempList:
        if s != '':
            cmdLine.append(s)
    return cmdLine

def hex_int(str):
    str = str.strip()
    str = str.lower()

    if str[:2] == '0x' or str[0] == 'x':
        return int(str,16)
    else:
        return int(str)

def dispatch_command(cmdLine,rbcpId):
    cmdLine = cmdLine.strip()
    cmdLine = cmdLine.lower()
    if cmdLine == 'help':
        rbcp_help()
    elif cmdLine == 'quit':
        run=0
        print '\nBye'
        exit()
    elif cmdLine[:2] == 'cd':
        cmdLine = get_addr_data(cmdLine[2:])
        if len(cmdLine) == 1:
            os.chdir(cmdLine[0])
            print ' Current: %s' % os.getcwd()
        else:
            print 'RBCP>  Error! Unknown command or style!'
    elif cmdLine == 'pwd':
            print ' ' + os.getcwd()
    elif cmdLine[:2] == 'ls':
        cmdLine = get_addr_data(cmdLine[2:])
        if len(cmdLine) == 0:
            cmdLine = os.listdir('.')
        elif len(cmdLine) == 1:
            cmdLine = os.listdir(cmdLine[0])
        else:
            cmdLine = ['RBCP>  Error! Unknown command or style!']
        for str in cmdLine:
            print ' ' + str
    elif cmdLine[:2] == 'rd':
        cmdLine = get_addr_data(cmdLine[2:])
        if len(cmdLine) == 2:
            rbcpAddr = hex_int(cmdLine[0])
            rbcpLen = hex_int(cmdLine[1])
            data = sitcprbcp.read_registers(ipAddress, rbcpAddr,rbcpLen, rbcpId)
            adrOfst = rbcpAddr % 16
            adrStart = rbcpAddr - adrOfst
            idx=0
            if len(data) == hex_int(cmdLine[1]):
                print 'RBCP>  Succeed in read. (ID=%d)' % rbcpId
            else:
                print 'RBCP>  Timeout occuered! (ID=%d)' % rbcpId
            for c in data:
                if idx % 16 ==0:
                    if idx==0:
                        print 'RBCP>  %08x:' % adrStart,
                        for s in range(adrOfst):
                            print '  ',
                        idx = adrOfst
                    else:
                        print 
                        print 'RBCP>  %08x:' % (adrStart + idx),
                elif idx % 8 == 0:
                    print '-',
                print '%02x' % (ord(c)),
                idx +=1
            print
            rbcpId += 1
        else:
            print 'RBCP>  Error! Unknown style of rd!'
    elif cmdLine[:2] == 'wr':
        cmdLine = get_addr_data(cmdLine[2:])
        if len(cmdLine) == 3:
            rbcpAddr = hex_int(cmdLine[1])
            rbcpWd = hex_int(cmdLine[2])
            if cmdLine[0] == 'b':
                rbcpLen = 1
                rbcpPack = '>B'
            elif cmdLine[0] == 's':
                rbcpLen = 2
                rbcpPack = '>H'
            elif cmdLine[0] == 'w':
                rbcpLen = 4
                rbcpPack = '>I'
            else:
                rbcpLen = 0
                rbcpPack = '>B'
            print 'RBCP>  Write %s to 0x%x (ID=%d)' % (cmdLine[2],rbcpAddr,rbcpId)
            data = struct.pack(rbcpPack, rbcpWd)
            sitcprbcp.write_registers(ipAddress, rbcpAddr, rbcpLen, data, rbcpId)
            rbcpId += 1
        else:
            print 'RBCP>  Error! Unknown style of wr!'
    return rbcpId

if __name__ == "__main__":

    argv = sys.argv  # コマンドライン引数を格納したリストの取得
    argc = len(argv) # 引数の個数

    if argc == 1:
        ipAddress = DEFAULT_IP
        rbcpPort = DEFAULT_PORT
    elif argc == 3:
        ipAddress = argv[1]
        rbcpPort = argv[2]
    else:
        print 'Usage: %s <IP address> <Port#>\n\n' % argv[0]
        quit()

    run =1
    cmdline = ''
    rbcpId = 0

    while run==1:
        cmdLine = raw_input('RBCP>')
        cmdLine = cmdLine.strip()
        cmdLine = cmdLine.lower()
        
        if cmdLine[0:5] == 'load ':
            cmdLine = get_addr_data(cmdLine[5:])
            fname = cmdLine[0]
            if len(cmdLine)==1:
                f_in = open(fname, 'r')
                for cmdLine in f_in:
                    rbcpId = dispatch_command(cmdLine,rbcpId)
        else:
            rbcpId = dispatch_command(cmdLine,rbcpId)

