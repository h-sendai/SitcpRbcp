#!/usr/bin/python3

import os
import sys
import time

import socket
import struct
import wx
import SitcpRbcp

register_info = [
    # name                  addr length init_value
    ('user_area_0', 0xffffff3c, 1, '0'),
    ('user_area_1', 0xffffff3d, 1, '1'),
    ('user_area_2', 0xffffff3e, 1, '2'),
    ('user_area_3', 0xffffff3f, 1, '3'),
]

ip_address = '192.168.10.16'
format = dict()
format[1] = '>B'
format[2] = '>H'
format[4] = '>I'

class Sample(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title = "NUETRON DAQ", size = (400, 420))
        panel = wx.Panel(self, -1)

        y = 10
        for (s, a, l, v) in register_info:
            wx.StaticText(panel, -1, s, (10,  y))
            setattr(self, s, wx.TextCtrl(panel, -1, v, (180, y), (120, -1), style = wx.ALIGN_RIGHT))
            y += 30

        putSend  = wx.Button(panel, -1,        'Send',  (180, 350), (80, 30))
        exit     = wx.Button(panel, wx.ID_EXIT, '',     (270, 350), (80, 30))
        #putStart = wx.Button(panel, -1,        'Start', (180, 380), (80, 30))
        #putStop  = wx.Button(panel, -1,        'Stop',  (270, 380), (80, 30))
        self.Bind(wx.EVT_BUTTON, self.OnSend,  id = putSend.GetId() )
        self.Bind(wx.EVT_BUTTON, self.OnExit,  id = wx.ID_EXIT      )
        #self.Bind(wx.EVT_BUTTON, self.OnStart, id = putStart.GetId())
        #self.Bind(wx.EVT_BUTTON, self.OnStop,  id = putStop.GetId() )

        #self.Bind(wx.EVT_BUTTON, self.OnEnd,   id = putEnd.GetId())

        self.Show(True)
    
    def OnExit(self, event):
        self.Close()

    def OnSend(self, event):
        rbcp = SitcpRbcp.SitcpRbcp()
        print('name address length value')
        for (s, a, l, v) in register_info:
            data = int(getattr(self, s).GetValue(), 0)
            print('%s %x %d %d' % (s, a, l, data))
            rbcp.write_register_f(ip_address, a, format[l], data)

        # replace text 
        # Replace(from, to, value)
        # to replace whole string, from = 0, to = -1
        #for (s, a, l, v) in register_info:
        #    getattr(self, s).Replace(0, -1, '1000')

#    def OnStart(self, event):
#       request_id = 0x81234567 # Need MSB bit 1
#                               # (valid request id 0x80000000 - 0xFFFFFFFF)
#       sub_address = 0x0
#       cmd_field1 = 0xaaaaffff # write list (cmd = 0xaa, cmd_type = 0xaa)
#       cmd_field2 = 0x00000000 # don't care for write list
#       request_packet = struct.pack('>IIII',
#                           request_id,
#                           sub_address,
#                           cmd_field1,
#                           cmd_field2
#                        )
#       request_packet += struct.pack('>I', 0xf)
#       request_packet += struct.pack('>I', 0x1)
#
#       u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#       # need bind() to send from PC port 6007
#       u.bind((my_ip_address, my_port))
#       u.sendto(request_packet, (remote_ip_address, remote_port))
#
#       reply_packet = u.recvfrom(9000) # try to read 9000 bytes
#       reply_data = reply_packet[0]   # recvfrom returns tuple (payload, (host, address))
#
#       u.close()

#    def OnStop(self, event):
#        request_id = 0x81234567 # Need MSB bit 1
#                                # (valid request id 0x80000000 - 0xFFFFFFFF)
#        sub_address = 0x0
#        cmd_field1 = 0xaaaaffff # write list (cmd = 0xaa, cmd_type = 0xaa)
#        cmd_field2 = 0x00000000 # don't care for write list
#        request_packet = struct.pack('>IIII',
#                            request_id,
#                            sub_address,
#                            cmd_field1,
#                            cmd_field2
#                         )
#        request_packet += struct.pack('>I', 0xf)
#        request_packet += struct.pack('>I', 0x0)
#
#        u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#        # need bind() to send from PC port 6007
#        u.bind((my_ip_address, my_port))
#        u.sendto(request_packet, (remote_ip_address, remote_port))
#
#        reply_packet = u.recvfrom(9000) # try to read 9000 bytes
#        reply_data = reply_packet[0]   # recvfrom returns tuple (payload, (host, address))
#
#        u.close()

#    def OnEnd(self, event):
#        print 'end'
#        pass

def main():
    app = wx.App()
    Sample()
    app.MainLoop()

if __name__ == '__main__':
    main()
