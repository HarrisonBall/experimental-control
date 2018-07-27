# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 11:35:44 2017

@author: QCL
"""

import visa
import numpy as np           

rm = visa.ResourceManager()
VISA_IDs= rm.list_resources()    
print VISA_IDs
DEVICES = [rm.open_resource(VISA_IDs[i]) for i in range(len(VISA_IDs))]          
print '0'  
def DEVICES_ID(device):
        ID=device.query('*IDN?')
        return ID
print '1'        
DEVICE_ID_INFO = np.zeros((1, 2))                     
for i in range(len(VISA_IDs)):    
    DEVICE_ID_INFO = np.concatenate((DEVICE_ID_INFO, np.array([[VISA_IDs[i], DEVICES_ID(DEVICES[i])]])))           
print '2'  
#print DEVICE_ID_INFO

for i in range(len(DEVICE_ID_INFO)):
    print DEVICE_ID_INFO[i]