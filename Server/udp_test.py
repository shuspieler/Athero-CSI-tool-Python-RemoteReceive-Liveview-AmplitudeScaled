# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 13:24:48 2017

@author: ren
"""
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = "~~~~~~~~~~~~~python test~~~~~~~~~~~~~"
    # 发送数据:
s.sendto(data, ('131.188.213.33', 1025))
s.close()