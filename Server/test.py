# -*- coding: utf-8 -*-
"""@package test
Created on Tue Jun 20 14:54:47 2017

@author: ren
"""

import numpy as np
import matplotlib.pyplot as plt

import Atheros
import Atheros_plotandsave

#orig = open('compare_orig.dat','rb')
#maked = open('compare_maked.dat', 'rb')
#fixed = open('compare_fixed.dat', 'rb')
#savetofile = open('apusaveandupd.dat', 'rb')
#udp_stream = open('pythonsave.dat', 'rb')


test = Atheros.read_from_file('Atheros_test.dat')



#orig = np.fromfile(orig, np.uint8)
#maked = np.fromfile(maked, np.uint8)
#fixed = np.fromfile(fixed, np.uint8)
#udp_stream = np.fromfile(udp_stream, np.uint8)
#savetofile = np.fromfile(savetofile, np.uint8)


ret = Atheros.read_from_file('./withrouter10072017.dat')

csi_matrix = ret[12]

#csi_total = csi_matrix['csi']
#csi_single = csi_total[:,0,:]

#csi_transeposed = np.transpose(csi_single)

#plt.plot(20*np.log10(np.abs(csi_transeposed)))
#plt.plot(np.angle(csi_transeposed)) #plt.plot(np.angle(csi_transeposed, deg =1)) :Return angle in degrees

#Atheros_plot.amplitude(csi_matrix)
#Atheros_plot.phase(csi_matrix)
