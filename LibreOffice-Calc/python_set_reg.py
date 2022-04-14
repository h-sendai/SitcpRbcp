# coding: utf-8
# from __future__ import unicode_literals
from __future__ import print_function

import uno
import sys
import os
import time
import datetime
#import SitcpRbcp

def detect_last_used_row():
    # https://ask.libreoffice.org/t/looking-for-last-row-used-programmatically/26223
    oDoc = XSCRIPTCONTEXT.getDocument()
    oSheet = oDoc.CurrentController.ActiveSheet
    oCursor = oSheet.createCursor()
    oCursor.gotoEndOfUsedArea(False)
    end_row = oCursor.getRangeAddress().EndRow +1
    # sys.stderr.write('%d\n' % (end_row))
    return oCursor.getRangeAddress().EndRow +1

def print_now():
    now = datetime.datetime.now().strftime('%F %H:%M:%S.%f')
    print('%s' % (now), end = ' ')

def set_registers(*args):
    print_now()
    print('start')
    
    format = dict()
    format[1] = '>B'
    format[2] = '>H'
    format[4] = '>I'

    #print('try import SitcpRbcp')
    doc = XSCRIPTCONTEXT.getDocument()
    try:
        import SitcpRbcp
    except ImportError:
        p = os.environ['HOME'] + '/.config/libreoffice/4/user/Scripts/python'
        sys.path.append(p)

        # for embedded python macro
        p = uno.fileUrlToSystemPath(doc.URL + '/Scripts/python')
        sys.path.append(p)

        import SitcpRbcp

    #for i in sys.path:
    #    print(i)

    #print('import done')
    rbcp = SitcpRbcp.SitcpRbcp()
    rbcp.set_verify_mode()

    ip_address = '192.168.10.16'
    max_row = detect_last_used_row()
    # print('max_row:', max_row)
    sheet = doc.getSheets().getByIndex(0)
    for i in range(0, max_row):
        col_a = sheet.getCellByPosition(0, i).String 
        if col_a == '':
            print('empty line')
            continue
        if col_a.startswith('#'):
            # skip this row as comment line
            print('comment line')
            continue
        if col_a == 'ip_address':
            ip_address = sheet.getCellByPosition(1, i).String 
            continue
        name    = col_a
        address = int(sheet.getCellByPosition(1, i).String, 0)
        len     = int(sheet.getCellByPosition(2, i).String, 0)
        value   = int(sheet.getCellByPosition(3, i).String, 0) 
        print('%s %d %s 0x%x %d %d' % (ip_address, i + 1, name, address, len, value))
        rbcp.write_register_f(ip_address, address, format[len], value)

    print_now()
    print('done')

    return

