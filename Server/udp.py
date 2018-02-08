# -*- coding: utf-8 -*-
"""@package udp
Created on Fri Jun 16 17:13:04 2017

@author: ren
"""

import socket

def udp_init(port):
    ## initalize the socket with udp protocol
    #
    #@param port the port number which used for the udp at the server
    #
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # SOCKET_DGRAM：UDP
    #s.bind(("", 0x1031))
    s.bind(("",port))
    
    return s

def recv(s):
    data, addr = s.recvfrom(4096) # BUFSIZE
    return data,addr
    
def close(s):
    s.close()