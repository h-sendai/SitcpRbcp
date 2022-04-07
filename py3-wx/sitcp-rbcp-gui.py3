#!/usr/bin/python3

import os
import sys
import time

import socket
import struct
import wx
import SitcpRbcp
import datetime

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
        wx.Frame.__init__(self, None, title = "NUETRON DAQ")
        panel = wx.Panel(self, -1)

        # layout
        sizer = wx.GridSizer(cols = 2, vgap = 0, hgap = 0)

        # Create Data structure
        # self.labels:    dict of StaticText objects. indexes are register name
        # self.textctrls: dict of TextCtrl objects. indexes are register name
        self.labels    = dict()
        self.textctrls = dict()
        for (n, a, l, v) in register_info:
            # create labels and textctrls
            self.labels[n]    = wx.StaticText(panel, id = wx.ID_ANY, label = n)
            self.textctrls[n] = wx.TextCtrl(panel, id = wx.ID_ANY, size = (100, 20), value = v, style = wx.ALIGN_RIGHT)

        for (n, a, l, v) in register_info:
            sizer.Add(self.labels[n])
            sizer.Add(self.textctrls[n])

        # Create button and layout them
        putSend  = wx.Button(panel, -1, 'Send')
        exit     = wx.Button(panel, wx.ID_EXIT, '')
        sizer.Add(putSend)
        sizer.Add(exit)

        # Assign methods to each buttons
        self.Bind(wx.EVT_BUTTON, self.OnSend,  id = putSend.GetId() )
        self.Bind(wx.EVT_BUTTON, self.OnExit,  id = wx.ID_EXIT      )

        # Create Status bar
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Start')

        panel.SetSizer(sizer)
        self.Show(True)
    
    def write_status(self, line):
        now = datetime.datetime.now().strftime("%F %T")
        self.statusbar.SetStatusText(now + ' ' + line)

    def OnExit(self, event):
        self.Close()

    def OnSend(self, event):
        self.write_status('OnSend')
        rbcp = SitcpRbcp.SitcpRbcp()
        print('name address length value')
        for (n, a, l, v) in register_info:
            data = int(self.textctrls[n].GetValue(), 0)
            print('%s %x %d %d' % (n, a, l, data))
            rbcp.write_register_f(ip_address, a, format[l], data)

        # replace text 
        # Replace(from, to, value)
        # to replace whole string, from = 0, to = -1
        #for (s, a, l, v) in register_info:
        #    getattr(self, s).Replace(0, -1, '1000')

        self.write_status('Send register data done')

def main():
    app = wx.App()
    Sample()
    app.MainLoop()

if __name__ == '__main__':
    main()
