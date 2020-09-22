# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 17:12:15 2020

@author: victor
"""

import numpy as np
from scipy.io import wavfile
from scipy import signal


_JUST='just intonation'
_TEMP='well tempered'


_C_FREQ=261.6256
_Db_FREQ=277.1826
_D_FREQ=293.6648
_Eb_FREQ=311.1270
_E_FREQ=329.6276
_F_FREQ=349.2282
_Gb_FREQ=369.9944
_G_FREQ=391.9954
_Ab_FREQ=415.3047
_A_FREQ=440
_Bb_FREQ=466.1638
_B_FREQ=493.8833


def build_frequency_matrix(frequency_list,fundamental=440.,system='equal temperament',broadness=1):
    frequency_list=frequency_list[1:]
    matrix=np.zeros(len(frequency_list))
    
    allowed_frequency_list=[]
    lowest_fundamental=fundamental
    while lowest_fundamental>frequency_list[0]:
        lowest_fundamental/=2.
    number_of_octaves=0
    highest_fundamental = lowest_fundamental
    while highest_fundamental<frequency_list[-1]:
        highest_fundamental*=2
        number_of_octaves+=1
    
    for i in range(number_of_octaves-1):
        if system=='equal temperament':
            allowed_frequency_list.append(lowest_fundamental*2**i)
            allowed_frequency_list.append(lowest_fundamental*2**(i+1./6.))
            allowed_frequency_list.append(lowest_fundamental*2**(i+1./3.))
            allowed_frequency_list.append(lowest_fundamental*2**(i+5./12.))
            allowed_frequency_list.append(lowest_fundamental*2**(i+7./12.))
            allowed_frequency_list.append(lowest_fundamental*2**(i+9./12.))
            allowed_frequency_list.append(lowest_fundamental*2**(i+11./12.))
        if system=='just intonation':
            allowed_frequency_list.append(lowest_fundamental*2**i)
            allowed_frequency_list.append(lowest_fundamental*2**i*9./8.)
            allowed_frequency_list.append(lowest_fundamental*2**i*5./4.)
            allowed_frequency_list.append(lowest_fundamental*2**i*4./3.)
            allowed_frequency_list.append(lowest_fundamental*2**i*3./2.)
            allowed_frequency_list.append(lowest_fundamental*2**i*5./3.)
            allowed_frequency_list.append(lowest_fundamental*2**i*15./8.)
    j=0
    while allowed_frequency_list[j]<frequency_list[0]:
        j+=1
    allowed_frequency_list=allowed_frequency_list[j:]
    j=0
    while allowed_frequency_list[-j]>frequency_list[-1]:
        j+=1
    allowed_frequency_list=allowed_frequency_list[:-1]
    i=0
    maxlen=len(frequency_list)-1
    for freq in allowed_frequency_list:
        while ((freq > frequency_list[i]) and (i<maxlen)):
            i+=1
        if i>broadness and i<maxlen-broadness:
            for j in range(i-broadness,i+broadness):
                matrix[j]=1.
        else:
            matrix[i]=1.
    return np.hstack((np.array([0]),matrix))

def harmonicise(input_path,output_path,fundamental=440.,system='equal temperament',broadness=1,nperseg=1024,inverse=False):
    rate,wav=wavfile.read(input_path)
    stereo=True
    if len(wav.shape)==2:
        stereo=True
    else:
        stereo=False
    
    if stereo:
        f,t,Zxx_l=signal.stft(wav[:,0],rate,nperseg=nperseg)
        f,t,Zxx_r=signal.stft(wav[:,1],rate,nperseg=nperseg)
    else:
        f,t,Zxx_l=signal.stft(wav,rate,nperseg=nperseg)
    fm=build_frequency_matrix(f,fundamental,'equal temperament',broadness)
    if inverse:
        fm=(fm-1)*(-1)
    print(f[5],t[1]-t[0])
    for i in range(len(t)):
        Zxx_l[:,i]*=fm
        
        if stereo:
            Zxx_r[:,i]*=fm
    out=signal.istft(Zxx_l,rate)[1]
    #return out,rate
    if stereo:
        out=np.vstack((out,signal.istft(Zxx_r,rate)[1]))
    out=out.T/out.max()
    wavfile.write(output_path,rate,out)
    return out,rate
        
