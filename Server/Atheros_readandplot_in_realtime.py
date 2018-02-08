# -*- coding: utf-8 -*-
"""@package Atheros_readandplot_in_realtime
Created on Tue May 16 13:25:36 2017

@author: ren
"""

import Atheros
import udp
import Atheros_plotandsave


ret = [] #an empty dictionary which could be save the CSI_matrix

#ret = Atheros.read_from_file('./withantenna.dat')  # 

s = udp.udp_init(5563) # create a udp handle. the port number could be changed
filehandle = Atheros_plotandsave.save_to_file_init('withrouter10072017.dat')  # create a filehandle in which could save the CSI_matrix

for i in range(10240):  # a loop to receive the data
    
    data, addr = udp.recv(s)  # create a udp socket
    CSI_matrix = Atheros.read_from_stream(data) # decode the CSI_matrix from udp stream
    Atheros_plotandsave.save_to_file(data, filehandle) # log the data to a file
    ret.append(CSI_matrix) # save the CSI_matrix to a dictionary
    
    
#    Atheros_plotandsave.amplitude(CSI_matrix) # plot the amplitude

#    Atheros_plotandsave.phase(CSI_matrix) #plot the phase
    Atheros_plotandsave.plot_single(CSI_matrix)
    
udp.close(s) #close udp
Atheros_plotandsave.close(filehandle) #close file
