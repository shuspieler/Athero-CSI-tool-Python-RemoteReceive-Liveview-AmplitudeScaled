# -*- coding: utf-8 -*-
"""@package Atheros_plotandsave
Created on Thu Jun 22 13:50:13 2017

@author: ren
"""

import math
import numpy as np
import matplotlib.pyplot as plt

global total_fig
global init
init = 0

##
#@brief plot the figure
#@param csi_matrix the input CSI_matrix which need to be plot
#@mode plot amplitude or phase
#

def ploting(csi_matrix, mode):

    global total_fig
    global init

    csi_total = csi_matrix['csi']

    if 0 == init:
        total_fig = plt.figure('CSI liveview',figsize=(17,10))
        plt.ion()
       
    for i in range(csi_matrix['nr']):

        fig_column = max(csi_matrix['nc'], csi_matrix['nr'])              
        csi_single_nc = csi_total[i,:,:]
        csi_transeposed_nc = np.transpose(csi_single_nc)
        transsub = total_fig.add_subplot(2,fig_column,i+1)
        
        if mode == amplitude:
            transsub.plot(20*np.log10(np.abs(csi_transeposed_nc)))
            transsub.grid(True)  
            transsub.set_ylabel('SNR [dB]')
            transsub.hold(False)             
            
            transsub.set_ylim((0,55))
        
        if mode == phase:
            transsub.plot(np.angle(csi_transeposed_nc))
            transsub.grid(True)  
            transsub.set_ylabel('phase(radian)')
            transsub.hold(False)        
            
            transsub.set_ylim((-4,4))
        
        transsub.set_xlabel('Subcarrier index with receiving antenna %d' %i)
        
#        if (1 == csi_matrix['nc']):
#            transsub.legend(('TX Antenna A'), loc = 'lower right')
        if (2 == csi_matrix['nc']):
            transsub.legend(('TX Antenna A', 'TX Antenna B'), loc = 'lower right')
        if (3 == csi_matrix['nc']):
            transsub.legend(('TX Antenna A', 'TX Antenna B', 'TX Antenna C'), loc = 'lower right')
        plt.pause(0.01)   
     
    for i in range(csi_matrix['nc']):

        fig_column = max(csi_matrix['nc'], csi_matrix['nr'])              
        csi_single_nr = csi_total[:,i,:]
        csi_transeposed_nr = np.transpose(csi_single_nr)
        recvsub = total_fig.add_subplot(2,fig_column,i+fig_column+1)  
        
        if mode == amplitude:                    
    
            recvsub.plot(20*np.log10(np.abs(csi_transeposed_nr)))    
            recvsub.grid(True)  
            recvsub.set_ylabel('SNR [dB]')
            recvsub.hold(False)              

            recvsub.set_ylim((0,55))
        
        if mode == phase:
            
            recvsub.plot(np.angle(csi_transeposed_nr)) 
            recvsub.grid(True)  
            recvsub.set_ylabel('phase(radian)')
            recvsub.hold(False)         

            recvsub.set_ylim((-4,4))
        
        recvsub.set_xlabel('Subcarrier index with transmitting antenna %d' %i)
        
#        if (1 == csi_matrix['nr']):
#            recvsub.legend(('RX Antenna A'), loc = 'lower right' )
        if (2 == csi_matrix['nr']):
            recvsub.legend(('RX Antenna A', 'RX Antenna B'), loc = 'lower right' )
        if (3 == csi_matrix['nr']):
            recvsub.legend(('RX Antenna A', 'RX Antenna B', 'RX Antenna C'), loc = 'lower right')
        plt.pause(0.01)   
    
    if 0 == init:
       init = 1
       
     
def plot_single(csi_matrix):
    
    global total_fig    
    global init

    csi_total = csi_matrix['csi']
    csi_total_scaled_amplitude = get_scaled_csi(csi_matrix)

    if 0 == init:
        total_fig = plt.figure('CSI liveview',figsize=(17,10))
        plt.ion()
  
    csi_single_nc = csi_total[0,:,:]
    csi_transeposed_nc = np.transpose(csi_single_nc)
    subfig = total_fig.add_subplot(2,2,1)
    subfig.plot(20*np.log10(np.abs(csi_transeposed_nc)))
#    subfig.plot((np.abs(csi_transeposed_nc)))
    subfig.grid(True)  
    subfig.set_ylabel('CSI Amplitude [dB]')
    subfig.hold(False)             
    subfig.set_ylim((30,50))
#    subfig.set_ylim((0,300))
    subfig.set_xlabel('Subcarrier index with receiving antenna 0')
        
    subfig = total_fig.add_subplot(2,2,2)
    subfig.plot(np.unwrap(np.angle(csi_transeposed_nc)))
    subfig.grid(True)  
    subfig.set_ylabel('unwapped phase(radian)')
    subfig.hold(False)        
    subfig.set_ylim((-4,4))
    subfig.set_xlabel('Subcarrier index with receiving antenna 0')    

    plt.pause(0.01)   
  

  
    csi_single_nr = csi_total[:,0,:]
    csi_transeposed_nr = np.transpose(csi_single_nr)
    
    csi_single_nr_scaled_amplitude = csi_total_scaled_amplitude[:,0,:]
    csi_transeposed_nr_scaled_amplitude = np.transpose(csi_single_nr_scaled_amplitude)
    
    subfig = total_fig.add_subplot(2,2,3)  
#    subfig.plot(20*np.log10(np.abs(csi_transeposed_nr_scaled_amplitude)))  
    subfig.plot(csi_transeposed_nr_scaled_amplitude)   
    subfig.grid(True)  
    subfig.set_ylabel('scaled RSS [dBm]')
    subfig.hold(False)              
#    subfig.set_ylim((-55,-65))
#    subfig.set_ylim((0,300))
    subfig.set_xlabel('Subcarrier index with transmitting antenna *')
    
    
    signal_level_total = int (csi_matrix["rssi"]) - 95
    signal_level_1 = int (csi_matrix["rssi1"]) - 95
    signal_level_2 = int (csi_matrix["rssi2"]) - 95    
    print 'signal level total %d dBm\n' %signal_level_total
    print 'signal level 1 %d dBm\n' %signal_level_1
    print 'signal level 2 %d dBm\n' %signal_level_2
    
    
    
    
    
    
    
        
    subfig = total_fig.add_subplot(2,2,4)            
    subfig.plot(np.unwrap(np.angle(csi_transeposed_nr[:,0:2])))
    subfig.grid(True)  
    subfig.set_ylabel(' unwrapped phase(radian)')
    subfig.hold(False)         
    subfig.set_ylim((-6,6))
    subfig.set_xlabel('Subcarrier index with transmitting antenna *')
    
    
    
    


    if 0 == init:
       init = 1


def amplitude(csi_matrix):
    
    ploting(csi_matrix, amplitude)

    
def phase(csi_matrix):
    
    ploting(csi_matrix, phase)
 
   
def save_to_file_init(filename):
    savetofile = open(filename, 'wb')
    return savetofile
 
   
def save_to_file(csi_matrix, filehandle):
    length = len(csi_matrix)
    filehandle.write(np.uint16(length))
    filehandle.write(csi_matrix)
 
    
def close(filehandle):
    filehandle.close()
    
def db(x):

    return (np.log10(x)*10+30)

def dbinv(x):

    ret = math.pow(10,(x/10.0))

    return ret
    
    
def get_scaled_csi(csi_matrix):

    num_tones = csi_matrix['num_tones']
    nr = csi_matrix['nr']
    nc = csi_matrix['nc']
    csi = csi_matrix['csi'][0:nr,0:nc,0:num_tones,]
    
    csi_squared = np.zeros((nr,nc,num_tones),dtype  = complex)
    csi_scaled = np.zeros((nr,nc,num_tones),dtype  = complex)
    for m in range(num_tones):
        for j in range (0, nc):
            for k in range (0, nr):
                csi_squared[k,j,m] = csi[k,j,m] * np.conjugate(csi[k,j,m])
       
    rssi_mag = 0
    if csi_matrix['rssi1'] != 128:
        signal_level = int (csi_matrix['rssi1']) - 95
        rssi_mag = dbinv(signal_level)
        csi_pwr = np.sum(csi_squared[0,:,:])
        csi_scaled[0,:,:] = 10*np.log10(csi_squared[0,:,:]/csi_pwr*rssi_mag)
    rssi_mag = 0
    if csi_matrix['rssi2'] != 128:
        signal_level = int (csi_matrix['rssi2']) - 95
        rssi_mag = dbinv(signal_level)
        csi_pwr = np.sum(csi_squared[1,:,:])
        csi_scaled[1,:,:] = 10*np.log10(csi_squared[1,:,:]/csi_pwr*rssi_mag) 
    rssi_mag = 0
    if csi_matrix['rssi3'] != 128:
        signal_level = int (csi_matrix['rssi3']) - 95
        rssi_mag = dbinv(signal_level)
        csi_pwr = np.sum(csi_squared[2,:,:])
        csi_scaled[2,:,:] = 10*np.log10(csi_squared[2,:,:]/csi_pwr*rssi_mag) 
        
#    if nc == 2:
#        csi_scaled = csi_scaled * np.sqrt(2)
#    elif nc == 3:
#        csi_scaled = csi_scaled + np.sqrt(3)
    return csi_scaled    

    