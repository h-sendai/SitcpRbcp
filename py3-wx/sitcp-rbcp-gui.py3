#!/usr/bin/python3

# based on
# https://gist.github.com/driscollis/a42aecb379742d3cd150/

import os
import sys
import time

import socket
import struct
import SitcpRbcp
import datetime

import wx
import wx.lib.scrolledpanel as scrolled

register_info = [
    # name                  addr length init_value
    ('user_area_0', 0xffffff3c, 1, '0'),
    ('user_area_1', 0xffffff3d, 1, '1'),
    ('user_area_2', 0xffffff3e, 1, '2'),
    ('user_area_3', 0xffffff3f, 1, '3'),
    #('user_area_4', 0xffffff40, 1, '4'),
    #('user_area_5', 0xffffff41, 1, '4'),
    #('user_area_6', 0xffffff42, 1, '4'),
    #('user_area_7', 0xffffff43, 1, '4'),
    #('user_area_8', 0xffffff43, 1, '4'),
    #('user_area_9', 0xffffff43, 1, '4'),
    #('user_area_10', 0xffffff43, 1, '4'),
]

ip_address = '192.168.10.16'
format = dict()
format[1] = '>B'
format[2] = '>H'
format[4] = '>I'

class Sample(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title = "SiTCP RBCP GUI", size = (200, 300))
        self.panel = wx.Panel(self, wx.ID_ANY)

        # layout
        self.scrolled_panel = scrolled.ScrolledPanel(self.panel, -1,
                              style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER, name="panel1")

        self.scrolled_panel.SetAutoLayout(1)
        self.scrolled_panel.SetupScrolling()
        self.spSizer = wx.BoxSizer(wx.VERTICAL)

        # Create Data structure
        # self.labels:    dict of StaticText objects. indexes are register name
        # self.textctrls: dict of TextCtrl objects. indexes are register name
        self.labels    = dict()
        self.textctrls = dict()
        for (n, a, l, v) in register_info:
            # create labels and textctrls
            self.labels[n]    = wx.StaticText(self.scrolled_panel, id = wx.ID_ANY, label = n, size = (90, 30))
            self.textctrls[n] = wx.TextCtrl(self.scrolled_panel, id = wx.ID_ANY, size = (90, 30), value = v, style = wx.ALIGN_RIGHT)

        for (n, a, l, v) in register_info:
            v = wx.BoxSizer(wx.HORIZONTAL)
            v.Add(self.labels[n],    0, wx.ALL|wx.EXPAND, 5)
            v.Add(self.textctrls[n], 1, wx.ALL|wx.EXPAND, 5)
            self.spSizer.Add(v)

        self.scrolled_panel.SetSizer(self.spSizer)

        # Create button and layout them
        putSend  = wx.Button(self.panel, -1, 'Send')
        # exit     = wx.Button(self.panel, wx.ID_EXIT, '')

        # Assign methods to each buttons
        self.Bind(wx.EVT_BUTTON, self.OnSend,  id = putSend.GetId() )
        #self.Bind(wx.EVT_BUTTON, self.OnExit,  id = wx.ID_EXIT      )

        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.scrolled_panel, 1, wx.EXPAND)
        panelSizer.Add(putSend)
        self.panel.SetSizer(panelSizer)

        # Create Status bar
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Good Luck')

        self.panel.SetSizer(panelSizer)
        #self.Show(True)
    
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
    app = wx.App(False)
    frame = Sample().Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
