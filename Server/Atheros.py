# -*- coding: utf-8 -*-
"""@package Atheros

Created on Wed Jun 07 10:15:54 2017

function: 
    read_csi: decode the CSI from binary to complex number
    read_from_file: read the saved data witch generated from client 
    read_from_stream: read the received data from udp

@author: ren
"""

import numpy as np
import sys 

global streamNr
streamNr = 1


def bit_convert(data, maxbit):
    if (data & (1 << (maxbit -1))):
        data -= (1 << maxbit)
    return data  
##
#@brief decode the CSI from row binary to complex number
#@param csi_buf received CSI row data
#@return retrun a matrix which contain all data related to the CSI
#
    
def read_csi(csi_buf, nr, nc, num_tones):
        
    csi_matrix = np.zeros((3,3,114),dtype  = complex)   #create a complex array which store the CSI matrix
    
    idx = 0   
    bits_left = 16 #init bits_left. we process 16 bits at a time
    bitmask = np.uint32(( 1 << 10 ) - 1) #according to the h/w, we have 10 bit resolution 
                              #for each real and imag value of the csi matrix H
    h_data = csi_buf[idx] # get 16 bits for processing
    idx += 1
    h_data += (csi_buf[idx] << 8)
    idx += 1
    current_data = h_data & ((np.uint32(1) << 16) - 1)
    
    for k in range(num_tones): #loop for every subcarrier
        for nc_idx in range(nc): # loop for each tx antenna
            for nr_idx in range(nr): #loop for each rx antenna
                if (bits_left - 10 ) < 0:
                    h_data = csi_buf[idx]
                    idx += 1
                    h_data += (csi_buf[idx] << 8)
                    idx += 1
                    current_data += h_data << bits_left
                    bits_left += 16
                imag = current_data & bitmask
                imag = bit_convert(imag, 10)
                imag = np.complex(imag)
                imag = imag *(0+1j)
                csi_matrix[nr_idx][nc_idx][k] += imag
                
                bits_left -=10
                current_data = current_data >> 10
                
                if (bits_left - 10) < 0: # bits number less than 10, get next 16 bits
                    h_data = csi_buf[idx]
                    idx += 1
                    h_data += (csi_buf[idx] << 8)
                    idx += 1
                    current_data += h_data << bits_left
                    bits_left += 16
                
                real = current_data & bitmask
                real = bit_convert(real, 10)
                real = np.complex(real)
                csi_matrix[nr_idx][nc_idx][k] += real
                
                bits_left -= 10
                current_data = current_data >> 10
                
    return csi_matrix
##
#@brief read the logged data which could saved from the client or saved from the server
#@return return a dictionary in which contains the CSI_matrix
#
  
def read_from_file(file_path):
    try:
        file = open(file_path,'rb')
    except Exception:
        print 'couldn\'t open file %s' %file_path
        file.close()
        sys.exit(0) 
    
    status = file.seek(0,2)
    if status != 0:
        pass # error message
        print 'Error2'
        
    len = file.tell()
    print 'file length is:%d\n' %len
    
    status = file.seek(0,0)
    if status != 0:
        pass # error message
        print status
        print 'error3'
    
    cur = 0
    ret = []
    
    endian_format = 'ieee-le' # some embedded system use big endian. for 16/32/64 system this should be all fine
    
    while cur < (len - 4):
        
        csi_matrix = {}
        field_len = np.fromfile(file, np.uint16, 1)
        if endian_format != 'ieee-le':
            field_len.dtype = '>u2'
        cur = cur + 2
        print 'Block length is: %d\n' %field_len
        
        if (cur + field_len)> len:
            break
        
        timestamp = np.fromfile(file, np.uint64, 1)
        if endian_format != 'ieee-le':
            timestamp.dtype = '>u8'
        csi_matrix['timestamp'] = timestamp
        cur = cur + 8
        print 'timestamp is %d\n' %timestamp
        
        csi_len = np.fromfile(file, np.uint16, 1)
        if endian_format != 'ieee-le':
            csi_len.dtype = '>u2'
        csi_matrix['csi_len'] = csi_len
        cur = cur + 2
        print 'csi_len is %d\n' %csi_len
          
        tx_channel = np.fromfile(file, np.uint16, 1)
        if endian_format != 'ieee-le':
            tx_channel.dtype = '>u2'
        csi_matrix['channel'] = tx_channel
        cur = cur + 2
        print 'channel is %d\n' %tx_channel
        
        err_info = np.fromfile(file, np.int8, 1)
        if endian_format != 'ieee-le':
            err_info.dtype = '>u1'
        else:
            err_info.dtype = 'u1'
        csi_matrix['err_info'] = err_info
        cur = cur + 1
        print 'err_info is %d\n' %err_info
     
        
        noise_floor = np.fromfile(file, np.int8, 1)
        if endian_format != 'ieee-le':
            noise_floor.dtype = '>u1'
        else:
            noise_floor.dtype = 'u1'
        csi_matrix['noise_floor'] = noise_floor
        cur = cur + 1
        print 'noise_floor is %d\n' %noise_floor
        
        Rate = np.fromfile(file, np.int8, 1) 
        if endian_format != 'ieee-le':
            Rate.dtype = '>u1'
        else:
            Rate.dtype = 'u1'
        csi_matrix['Rate'] = Rate
        cur = cur + 1
        print 'rate is %x\n' %Rate
        
        bandWidth = np.fromfile(file, np.int8, 1)
        if endian_format != 'ieee-le':
            bandWidth.dtype = '>u1'
        else:
            bandWidth.dtype = 'u1'
        csi_matrix['bandWidth'] = bandWidth
        cur = cur + 1
        print 'bandWidth is %d\n' %bandWidth
        
        num_tones = np.fromfile(file, np.int8, 1)
        if endian_format != 'ieee-le':
            num_tones.dtype = ">u1"
        else:
            num_tones.dtype = "u1"
        csi_matrix['num_tones'] = num_tones
        cur = cur + 1
        print 'num_tones is %d\n' %num_tones
        
        nr = np.fromfile(file, np.int8, 1)
        if endian_format != 'ieee-le':
            nr.dtype = '>u1'
        else:
            nr.dtype = 'u1'
        csi_matrix['nr'] = nr
        cur = cur + 1
        print 'nr is %d\n' %nr
        
        nc = np.fromfile(file, np.int8, 1)
        if endian_format != 'ieee-le':
            nc.dtype = '>u1'
        else:
            nc.dtype = 'u1'
        csi_matrix['nc'] = nc
        cur = cur + 1
        print 'nc is %d\n' %nc
        
        rssi = np.fromfile(file, np.int8, 1)
        if endian_format != 'ieee-le':
            rssi.dtype = '>u1'
        else:
            rssi.dtype = 'u1'
        csi_matrix['rssi'] = rssi
        cur = cur + 1
        print 'rssi is %d\n' %rssi
        
        rssi1 = np.fromfile(file, np.int8, 1)
        if endian_format != 'ieee-le':
            rssi1.dtype = '>u1'
        else:
            rssi1.dtype = 'u1'
        csi_matrix['rssi1'] = rssi1
        cur = cur + 1
        print 'rssi1 is %d\n' %rssi1
        
        rssi2 = np.fromfile(file, np.int8, 1)
        if endian_format != 'ieee-le':
            rssi2.dtype = '>u1'
        else:
            rssi2.dtype = 'u1'
        csi_matrix['rssi2'] = rssi2
        cur = cur + 1
        print 'rssi2 is %d\n' %rssi2
        
        rssi3 = np.fromfile(file, np.int8, 1) #wrong
        if endian_format != 'ieee-le':
            rssi3.dtype = '>u1'
        else:
            rssi3.dtype = 'u1'
        csi_matrix['rssi3'] = rssi3
        cur = cur + 1
        print 'rssi3 is %d\n' %rssi3
        
        payload_len = np.fromfile(file, np.int16, 1)
        if endian_format != 'ieee-le':
            payload_len.dtype = '>u2'
        csi_matrix['payload_len'] = payload_len
        cur = cur + 2
        print 'payload length is %d\n' %payload_len
        
        if csi_len > 0:
            csi_buf = np.fromfile(file, np.uint8, csi_len)
            csi = read_csi(csi_buf, nr, nc, num_tones)
            cur = cur + csi_len
            csi_matrix['csi'] = csi
#        else:
#            csi_matrix['csi'] =''
        
        if payload_len > 0:
            data_buf = np.fromfile(file, np.uint8, payload_len)
            cur = cur + payload_len
            csi_matrix['payload'] = data_buf
        else:
            csi_matrix['payload'] = 0
            
        if (cur + 420) > len:
            break
        ret.append(csi_matrix)
    
    if ret.__len__() > 1:
        ret = ret[0:(ret.__len__() - 1)]
        
    file.close()
    return ret

##
#@brief read the stream which transmitted from udp
#@return return a CSI_matrix
#

def read_from_stream(stream):
    
    global streamNr
    
    cur = 0
    csi_matrix = {}
    
    length =len(stream)
    print '%d stream length is: %d\n' %(streamNr,length)
    streamNr += 1
    
    endian_format = 'ieee-le' # some embedded system use big endian. for 16/32/64 system this should be all fine  
    
    timestamp = np.frombuffer(stream, np.uint64, 1, cur)
    if endian_format != 'ieee-le':
        timestamp.dtype = '>u8'
    csi_matrix['timestamp'] = timestamp
    cur = cur + 8
#    print 'timestamp is %d\n' %timestamp
    
    csi_len = np.frombuffer(stream, np.uint16, 1, cur)
    if endian_format != 'ieee-le':
        csi_len.dtype = '>u2'
    csi_matrix['csi_len'] = csi_len
    cur = cur + 2
#    print 'csi_len is %d\n' %csi_len
      
    tx_channel = np.frombuffer(stream, np.uint16,1, cur)
    if endian_format != 'ieee-le':
        tx_channel.dtype = '>u2'
    csi_matrix['channel'] = tx_channel
    cur = cur + 2
#    print 'channel is %d\n' %tx_channel
    
    err_info = np.frombuffer(stream, np.int8, 1, cur)
    if endian_format != 'ieee-le':
        err_info.dtype = '>u1'
    else:
        err_info.dtype = 'u1'
    csi_matrix['err_info'] = err_info
    cur = cur + 1
#    print 'err_info is %d\n' %err_info
     
    noise_floor = np.frombuffer(stream, np.int8, 1, cur)
    if endian_format != 'ieee-le':
        noise_floor.dtype = '>u1'
    else:
        noise_floor.dtype = 'u1'
    csi_matrix['noise_floor'] = noise_floor
    cur = cur + 1
#    print 'noise_floor is %d\n' %noise_floor
    
    Rate = np.frombuffer(stream, np.int8, 1, cur) 
    if endian_format != 'ieee-le':
        Rate.dtype = '>u1'
    else:
        Rate.dtype = 'u1'
    csi_matrix['Rate'] = Rate
    cur = cur + 1
#    print 'rate is %x\n' %Rate
    
    bandWidth = np.frombuffer(stream, np.int8, 1, cur)
    if endian_format != 'ieee-le':
        bandWidth.dtype = '>u1'
    else:
        bandWidth.dtype = 'u1'
    csi_matrix['bandWidth'] = bandWidth
    cur = cur + 1
#    print 'bandWidth is %d\n' %bandWidth
    
    num_tones = np.frombuffer(stream, np.int8, 1, cur)
    if endian_format != 'ieee-le':
        num_tones.dtype = ">u1"
    else:
        num_tones.dtype = "u1"
    csi_matrix['num_tones'] = num_tones
    cur = cur + 1
#    print 'num_tones is %d\n' %num_tones
    
    nr = np.frombuffer(stream, np.int8, 1, cur)
    if endian_format != 'ieee-le':
        nr.dtype = '>u1'
    else:
        nr.dtype = 'u1'
    csi_matrix['nr'] = nr
    cur = cur + 1
#    print 'nr is %d\n' %nr
    print '↑↑↑↑↑ (nr) receiving antenna is %d ↑↑↑↑↑↑↑↑' %nr
    
    nc = np.frombuffer(stream, np.int8, 1, cur)
    if endian_format != 'ieee-le':
        nc.dtype = '>u1'
    else:
        nc.dtype = 'u1'
    csi_matrix['nc'] = nc
    cur = cur + 1
#    print 'nc is %d\n' %nc
    print '↑↑↑↑↑ (nc) transmitting antenna is %d ↑↑↑↑↑\n\n' %nc
    
    rssi = np.frombuffer(stream, np.int8, 1, cur)
    if endian_format != 'ieee-le':
        rssi.dtype = '>u1'
    else:
        rssi.dtype = 'u1'
    csi_matrix['rssi'] = rssi
    cur = cur + 1
    print 'rssi is %d\n' %rssi
    
    rssi1 = np.frombuffer(stream, np.int8, 1, cur)
    if endian_format != 'ieee-le':
        rssi1.dtype = '>u1'
    else:
        rssi1.dtype = 'u1'
    csi_matrix['rssi1'] = rssi1
    cur = cur + 1
    print 'rssi1 is %d\n' %rssi1
    
    rssi2 = np.frombuffer(stream, np.int8, 1, cur)
    if endian_format != 'ieee-le':
        rssi2.dtype = '>u1'
    else:
        rssi2.dtype = 'u1'
    csi_matrix['rssi2'] = rssi2
    cur = cur + 1
    print 'rssi2 is %d\n' %rssi2
    
    rssi3 = np.frombuffer(stream, np.int8, 1, cur) #wrong
    if endian_format != 'ieee-le':
        rssi3.dtype = '>u1'
    else:
        rssi3.dtype = 'u1'
    csi_matrix['rssi3'] = rssi3
    cur = cur + 1
    print 'rssi3 is %d\n' %rssi3
    
    payload_len = np.frombuffer(stream, np.int16, 1, cur)
    if endian_format != 'ieee-le':
        payload_len.dtype = '>u2'
    csi_matrix['payload_len'] = payload_len
    cur = cur + 2
#    print 'payload length is %d\n' %payload_len
    
    if csi_len > 0:
        csi_buf = np.frombuffer(stream, np.uint8, csi_len, cur)
        csi = read_csi(csi_buf, nr, nc, num_tones)
        cur = cur + csi_len
        csi_matrix['csi'] = csi
#    else:
#        csi_matrix['csi'] = ''
    
    if payload_len > 0:
        data_buf = np.frombuffer(stream, np.uint8, payload_len, cur)
        cur = cur + payload_len
        csi_matrix['payload'] = data_buf
    else:
        csi_matrix['payload'] = 0
    
    return csi_matrix

    
        
        
        
        
        
