# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 09:26:21 2017

@author: Harrison Ball

2017-09-18, RW
    - ISEG EHQ102M serial number 480996 back from repair, implement again, seems to work
"""
from collections import OrderedDict

#=================================================================================================

#       ------------------------  DICTIONARY OF ISEG IDENTIFIERS  ------------------------
#            maps USB IDs assigned by computer to serial numbers of iseg modules. 
#    user to ensure dictionary is current, with each re-installation any hardware interface

#=================================================================================================

# ------------------------# ------------------------# ------------------------
# This self-contained code queries all ISEG modules an lists the USB IDs of all
# modules currently connected, then gener*ates a list of corresponding serial
# numbers
# ------------------------# ------------------------# ------------------------              
''' 
import visa
import numpy as np           

rm = visa.ResourceManager()
VISA_IDs= rm.list_resources()    
print VISA_IDs
DEVICES = [rm.open_resource(VISA_IDs[i]) for i in range(len(VISA_IDs))]          

def DEVICES_ID(device):
        ID=device.query('*IDN?')
        return ID
        
DEVICE_ID_INFO = np.zeros((1, 2))                     
for i in range(len(VISA_IDs)):    
    DEVICE_ID_INFO = np.concatenate((DEVICE_ID_INFO, np.array([[VISA_IDs[i], 
                                                            DEVICES_ID(DEVICES[i])]])))           
#print DEVICE_ID_INFO

for i in range(len(DEVICE_ID_INFO)):
    print DEVICE_ID_INFO[i]

 
CURRENT CONEXTIONS

[u'ASRL4::INSTR' u'iseg Spezialelektronik GmbH,EHQ 102,480996,3.14\r\n']
[u'ASRL5::INSTR' u'iseg Spezialelektronik GmbH,EHQ 102,480997,3.14\r\n']
[u'ASRL17::INSTR' u'iseg Spezialelektronik GmbH,EHQ 102,480936,3.14\r\n']
[u'ASRL18::INSTR' u'iseg Spezialelektronik GmbH,EHQ 102,480935,3.14\r\n']
[u'ASRL19::INSTR' u'THURLBY THANDAR, MX100TP, 436129, 1.03-1.00-1.02\r\n']
[u'ASRL20::INSTR' u'iseg Spezialelektronik GmbH,EHQ 102,480931,3.14\r\n']
[u'ASRL21::INSTR' u'iseg Spezialelektronik GmbH,EHQ 102,480934,3.14\r\n']
[u'ASRL22::INSTR' u'iseg Spezialelektronik GmbH,EHQ 102,480932,3.14\r\n']
[u'ASRL23::INSTR' u'iseg Spezialelektronik GmbH,EHQ 102,480933,3.14\r\n']
 
''' 
      
#____________ BIJECTIVE DICTIONARY: return ID/USB given USB/ID  ______________

InstID_2_VisaID={}

InstID_2_VisaID[u'ASRL4::INSTR'] = 'iseg:480996'
InstID_2_VisaID[u'ASRL5::INSTR'] = 'iseg:480997'
#InstID_2_VisaID[u'ASRL6::INSTR'] = 'TEMP:iseg:480499'#TEMPORARY UNIT ON LOAN WHILE UNIT 480996 IS BEING REPAIRED
InstID_2_VisaID[u'ASRL17::INSTR'] = 'iseg:480936'
InstID_2_VisaID[u'ASRL18::INSTR'] = 'iseg:480935'
InstID_2_VisaID[u'ASRL19::INSTR'] = 'MX100TP:436129'
InstID_2_VisaID[u'ASRL20::INSTR'] = 'iseg:480931'
InstID_2_VisaID[u'ASRL21::INSTR'] = 'iseg:480934'
InstID_2_VisaID[u'ASRL22::INSTR'] = 'iseg:480932'
InstID_2_VisaID[u'ASRL23::INSTR'] = 'iseg:480933'  

InstID_2_VisaID['iseg:480996'] = u'ASRL4::INSTR' 
InstID_2_VisaID['iseg:480997'] = u'ASRL5::INSTR'
#InstID_2_VisaID['TEMP:iseg:480499'] = u'ASRL6::INSTR' 
InstID_2_VisaID['iseg:480936'] = u'ASRL17::INSTR'
InstID_2_VisaID['iseg:480935'] = u'ASRL18::INSTR'
InstID_2_VisaID['MX100TP:436129'] = u'ASRL19::INSTR' 
InstID_2_VisaID['iseg:480931'] = u'ASRL20::INSTR' 
InstID_2_VisaID['iseg:480934'] = u'ASRL21::INSTR' 
InstID_2_VisaID['iseg:480932'] = u'ASRL22::INSTR' 
InstID_2_VisaID['iseg:480933'] = u'ASRL23::INSTR'   #TEMPORARY UNIT ON LOAN WHILE UNIT 480996 IS BEING REPAIRED

InstID_2_VisaID['ISEG GND'] = 'N/A: ISEG GND'

#=================================================================================================

#    --------    CREATE LIST OF COLOURS FOR ASSOCIATING PERMENANTLY TO TRAP SURFACES  -------

#=================================================================================================


colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']



#=================================================================================================

#    --------  DEFINE DICTIONARIES FOR CNX ATTRIBUTES FOR ALL UHV SYSTEM COMPONENTS     --------

#=================================================================================================
#
#
#
# ________________________________________________________________________________________________

# ----------------------#                  FT#1 (D-SUB)                 # ------------------------
# ________________________________________________________________________________________________


# ----------------------# ----------------------# ----------------------# ------------------------
# ----------------------#                  ELECTRON GUN #1               # ------------------------
# ----------------------# ----------------------# ----------------------# ------------------------
#
#____________________ 'Electron Gun #1: emission-bias' _____________________

egun1_emission_bias = {}
egun1_emission_bias['TRAP_SURF_NAME_LONG'] = 'Electron Gun #1: emission-bias'
egun1_emission_bias['TRAP_SURF_NAME_SHORT'] = 'egun1:emission-bias'
egun1_emission_bias['ID_TAG'] = '1.1 & 1.2'
egun1_emission_bias['FT_PIN'] = '1.1 & 1.2'
egun1_emission_bias['INST_ID'] = 'iseg:480935' #previously UNIT 480996, but exchanged with STring (now controlled by TEMP:480449 during repair of faulty 480996 unit)
egun1_emission_bias['INST_CHANNEL'] = 'N/A'
egun1_emission_bias['VISA_ID'] = InstID_2_VisaID[egun1_emission_bias['INST_ID']]
egun1_emission_bias['NIDAQ_AI'] = 'to be filled'
egun1_emission_bias['NIDAQ_2_HV_CONVERSION'] = 'N/A'

#____________________ 'Electron Gun #1: emission-source' _____________________

egun1_emission_source = {}
egun1_emission_source['TRAP_SURF_NAME_LONG'] = 'Electron Gun #1: emission-source'
egun1_emission_source['TRAP_SURF_NAME_SHORT'] = 'egun1:emission-source'
egun1_emission_source['ID_TAG'] = '1.1/1.2'
egun1_emission_source['FT_PIN'] = '1.1/1.2'
egun1_emission_source['INST_ID'] = 'MX100TP:436129'
egun1_emission_source['INST_CHANNEL'] = 1
egun1_emission_source['VISA_ID'] = InstID_2_VisaID[egun1_emission_bias['INST_ID']]
egun1_emission_source['NIDAQ_AI'] = 'to be filled'
egun1_emission_source['COLOUR'] = colours[0]

#____________________ 'Electron Gun #1: cathode plate' _____________________

egun1_cathode = {}
egun1_cathode['TRAP_SURF_NAME_LONG'] = 'Electron Gun #1: cathode plate'
egun1_cathode['TRAP_SURF_NAME_SHORT'] = 'egun1:cathode'
egun1_cathode['ID_TAG'] = '1.5'
egun1_cathode['FT_PIN'] = '1.5'
egun1_cathode['INST_ID'] = 'MX100TP:436129'
egun1_cathode['INST_CHANNEL'] = 3
egun1_cathode['VISA_ID'] = InstID_2_VisaID[egun1_cathode['INST_ID']]
egun1_cathode['NIDAQ_AI'] = 'to be filled'
egun1_cathode['COLOUR'] = colours[0]

#____________________ 'Electron Gun #1: annode plate' _____________________

egun1_anode = {}
egun1_anode['TRAP_SURF_NAME_LONG'] = 'Electron Gun #1: anode plate'
egun1_anode['TRAP_SURF_NAME_SHORT'] = 'egun1:anode'
egun1_anode['ID_TAG'] = '1.6'
egun1_anode['FT_PIN'] = '1.6'
egun1_anode['INST_ID'] = 'MX100TP:436129'
egun1_anode['INST_CHANNEL'] = 2
egun1_anode['VISA_ID'] = InstID_2_VisaID[egun1_anode['INST_ID']]
egun1_anode['NIDAQ_AI'] = 'to be filled'
egun1_anode['COLOUR'] = colours[0]


# ----------------------# ----------------------# ----------------------# ------------------------
# ----------------------#                  ELECTRON GUN #2               # ------------------------
# ----------------------# ----------------------# ----------------------# ------------------------


#____________________ 'Electron Gun #2: emission-bias' _____________________

egun2_emission_bias = {}
egun2_emission_bias['TRAP_SURF_NAME_LONG'] = 'Electron Gun #2: emission-bias'
egun2_emission_bias['TRAP_SURF_NAME_SHORT'] = 'egun2:emission-bias'
egun2_emission_bias['ID_TAG'] = '1.7/1.8 OR 1.9/1.10'
egun2_emission_bias['FT_PIN'] = '1.7/1.8 OR 1.9/1.10'
egun2_emission_bias['INST_ID'] = 'MX100TP:436129'
egun2_emission_bias['INST_CHANNEL'] = 1
egun2_emission_bias['VISA_ID'] = InstID_2_VisaID[egun2_emission_bias['INST_ID']]
egun2_emission_bias['NIDAQ_AI'] = 'to be filled'
egun2_emission_bias['COLOUR'] = colours[0]

#____________________ 'Electron Gun #2: cathode plate' _____________________

egun2_cathode = {}
egun2_cathode['TRAP_SURF_NAME_LONG'] = 'Electron Gun #2: cathode plate'
egun2_cathode['TRAP_SURF_NAME_SHORT'] = 'egun2:cathode'
egun2_cathode['ID_TAG'] = '1.11'
egun2_cathode['FT_PIN'] = '1.11'
egun2_cathode['INST_ID'] = 'MX100TP:436129'
egun2_cathode['INST_CHANNEL'] = 2
egun2_cathode['VISA_ID'] = InstID_2_VisaID[egun2_cathode['INST_ID']]
egun2_cathode['NIDAQ_AI'] = 'to be filled'
egun2_cathode['COLOUR'] = colours[0]

#____________________ 'Electron Gun #2: annode plate' _____________________

egun2_anode = {}
egun2_anode['TRAP_SURF_NAME_LONG'] = 'Electron Gun #2: anode plate'
egun2_anode['TRAP_SURF_NAME_SHORT'] = 'egun2:anode'
egun2_anode['ID_TAG'] = '1.12'
egun2_anode['FT_PIN'] = '1.12'
egun2_anode['INST_ID'] = 'MX100TP:436129'
egun2_anode['INST_CHANNEL'] = 3
egun2_anode['VISA_ID'] = InstID_2_VisaID[egun2_anode['INST_ID']]
egun2_anode['NIDAQ_AI'] = 'to be filled'
egun2_anode['COLOUR'] = colours[0]


# ________________________________________________________________________________________________

# ----------------------#                     FT#2                      # ------------------------
# ________________________________________________________________________________________________
##
#
#____________________ 'Electron Gun #1: ExB plate (LHS)' _____________________

egun1ExB_LHS = {}
egun1ExB_LHS['TRAP_SURF_NAME_LONG'] = 'Electron Gun #1: ExB plate (LHS)'
egun1ExB_LHS['TRAP_SURF_NAME_SHORT'] = 'egun1:ExB:LHS'
egun1ExB_LHS['ID_TAG'] = '2.1'
egun1ExB_LHS['FT_PIN'] = '2.1'
egun1ExB_LHS['INST_ID'] = 'iseg:480936'#(previously: 'iseg:480996', exchanged with STE2)
egun1ExB_LHS['INST_CHANNEL'] = 'N/A'
egun1ExB_LHS['VISA_ID'] = InstID_2_VisaID[egun1ExB_LHS['INST_ID']]
egun1ExB_LHS['NIDAQ_AI'] = '6'
egun1ExB_LHS['NIDAQ_2_HV_CONVERSION'] = 'N/A'

#____________________ 'Electron Gun #1: ExB plate (RHS)' _____________________

egun1ExB_RHS = {}
egun1ExB_RHS['TRAP_SURF_NAME_LONG'] = 'Electron Gun #1: ExB plate (RHS)'
egun1ExB_RHS['TRAP_SURF_NAME_SHORT'] = 'egun1:ExB:RHS'
egun1ExB_RHS['ID_TAG'] = '2.2'
egun1ExB_RHS['FT_PIN'] = '2.2'
egun1ExB_RHS['INST_ID'] = 'iseg:480997'
egun1ExB_RHS['INST_CHANNEL'] = 'N/A'
egun1ExB_RHS['VISA_ID'] = InstID_2_VisaID[egun1ExB_RHS['INST_ID']]
egun1ExB_RHS['NIDAQ_AI'] = '7'
egun1ExB_RHS['NIDAQ_2_HV_CONVERSION'] = 'N/A'

#____________________ 'Electron Gun #2: ExB plate (LHS)' _____________________

egun2ExB_LHS = {}
egun2ExB_LHS['TRAP_SURF_NAME_LONG'] = 'Electron Gun #2: ExB plate (LHS)'
egun2ExB_LHS['TRAP_SURF_NAME_SHORT'] = 'egun2:ExB:LHS'
egun2ExB_LHS['ID_TAG'] = '2.3'
egun2ExB_LHS['FT_PIN'] = '2.3'
egun2ExB_LHS['INST_ID'] = 'iseg:480996'
egun2ExB_LHS['INST_CHANNEL'] = 'N/A'
#egun2ExB_LHS['VISA_ID'] = InstID_2_VisaID[egun2ExB_LHS['INST_ID']]
egun2ExB_LHS['NIDAQ_AI'] = '8'
egun2ExB_LHS['NIDAQ_2_HV_CONVERSION'] = 'N/A'

#____________________ 'Electron Gun #2: ExB plate (RHS)' _____________________

egun2ExB_RHS = {}
egun2ExB_RHS['TRAP_SURF_NAME_LONG'] = 'Electron Gun #2: ExB plate (RHS)'
egun2ExB_RHS['TRAP_SURF_NAME_SHORT'] = 'egun2:ExB:RHS'
egun2ExB_RHS['ID_TAG'] = '2.4'
egun2ExB_RHS['FT_PIN'] = '2.4'
egun2ExB_RHS['INST_ID'] = 'iseg:480997'
egun2ExB_RHS['INST_CHANNEL'] = 'N/A'
#egun2ExB_RHS['VISA_ID'] = InstID_2_VisaID[egun2ExB_RHS['INST_ID']]
egun2ExB_RHS['NIDAQ_AI'] = '9'
egun2ExB_RHS['NIDAQ_2_HV_CONVERSION'] = 'N/A'


#____________________ 'Loading Trap: end-cap #1' _____________________

Loading_EndCap1 = {}
Loading_EndCap1['TRAP_SURF_NAME_LONG'] = 'Loading Trap: end-cap #1'
Loading_EndCap1['TRAP_SURF_NAME_SHORT'] = 'LoadTrp:EC1'
Loading_EndCap1['ID_TAG'] = '2.5'
Loading_EndCap1['FT_PIN'] = '2.5'
Loading_EndCap1['INST_ID'] = 'ISEG GND'
Loading_EndCap1['VISA_ID'] = 'ISEG GND'
Loading_EndCap1['NIDAQ_AI'] = 'to be filled'

#____________________ 'Loading Trap: centre ring' _____________________

Loading_CentreRing = {}
Loading_CentreRing['TRAP_SURF_NAME_LONG'] = 'Loading Trap: centre ring'
Loading_CentreRing['TRAP_SURF_NAME_SHORT'] = 'LoadTrp:CR'
Loading_CentreRing['ID_TAG'] = '2.6'
Loading_CentreRing['FT_PIN'] = '2.6'
Loading_CentreRing['INST_ID'] = 'iseg:480931'
Loading_CentreRing['VISA_ID'] = InstID_2_VisaID[Loading_CentreRing['INST_ID']]
Loading_CentreRing['NIDAQ_AI'] = '0'
#Loading_CentreRing['NIDAQ_2_HV_CONVERSION'] = 1000/4.250
Loading_CentreRing['NIDAQ_2_HV_CONVERSION'] = 220.1218463
Loading_CentreRing['COLOUR'] = colours[0]

#____________________ 'Loading Trap: end-cap #2' _____________________

Loading_EndCap2 = {}
Loading_EndCap2['TRAP_SURF_NAME_LONG'] = 'Loading Trap: end-cap #2'
Loading_EndCap2['TRAP_SURF_NAME_SHORT'] = 'LoadTrp:EC2'
Loading_EndCap2['ID_TAG'] = '2.7'
Loading_EndCap2['FT_PIN'] = '2.7'
Loading_EndCap2['INST_ID'] = 'iseg:480932'
Loading_EndCap2['VISA_ID'] = InstID_2_VisaID[Loading_EndCap2['INST_ID']]
Loading_EndCap2['NIDAQ_AI'] = '1'
#Loading_EndCap2['NIDAQ_2_HV_CONVERSION'] = 1000/4.160
Loading_EndCap2['NIDAQ_2_HV_CONVERSION'] = 220.7230592
Loading_EndCap2['COLOUR'] = colours[1]

#
#
# ________________________________________________________________________________________________

# ----------------------#                     FT#3                      # ------------------------
# ________________________________________________________________________________________________

#____________________ 'Rotating Wall: Quadruplet #1' _____________________

RW1 = {}
RW1['TRAP_SURF_NAME_LONG'] = 'Rotating Wall: Quadruplet #1'
RW1['TRAP_SURF_NAME_SHORT'] = 'RW1'
RW1['ID_TAG'] = '3.4'
RW1['FT_PIN'] = '3.1'
RW1['INST_ID'] = 'iseg:480933'
RW1['VISA_ID'] = InstID_2_VisaID[RW1['INST_ID']]
RW1['NIDAQ_AI'] = '2'
#RW1['NIDAQ_2_HV_CONVERSION'] = 1000/4.260
RW1['NIDAQ_2_HV_CONVERSION'] = 220.6153391
RW1['COLOUR'] = colours[2]

#____________________ 'Rotating Wall: Quadruplet #2' _____________________

RW2 = {}
RW2['TRAP_SURF_NAME_LONG'] = 'Rotating Wall: Quadruplet #2'
RW2['TRAP_SURF_NAME_SHORT'] = 'RW2'
RW2['ID_TAG'] = '3.5'
RW2['FT_PIN'] = '3.2'
RW2['INST_ID'] = 'iseg:480933'
RW2['VISA_ID'] = InstID_2_VisaID[RW2['INST_ID']]
RW2['NIDAQ_AI'] = '2'
#RW2['NIDAQ_2_HV_CONVERSION'] = 1000/4.260
RW2['NIDAQ_2_HV_CONVERSION'] = RW1['NIDAQ_2_HV_CONVERSION']
RW2['COLOUR'] = colours[2]

#____________________ 'Rotating Wall: Quadruplet #3' _____________________

RW3 = {}
RW3['TRAP_SURF_NAME_LONG'] = 'Rotating Wall: Quadruplet #3'
RW3['TRAP_SURF_NAME_SHORT'] = 'RW3'
RW3['ID_TAG'] = '3.6'
RW3['FT_PIN'] = '3.3'
RW3['INST_ID'] = 'iseg:480933'
RW3['VISA_ID'] = InstID_2_VisaID[RW3['INST_ID']]
RW3['NIDAQ_AI'] = '2'
#RW3['NIDAQ_2_HV_CONVERSION'] = 1000/4.260
RW3['NIDAQ_2_HV_CONVERSION'] = RW1['NIDAQ_2_HV_CONVERSION']
RW3['COLOUR'] = colours[2]

#____________________ 'Rotating Wall: Quadruplet #4' _____________________

RW4 = {}
RW4['TRAP_SURF_NAME_LONG'] = 'Rotating Wall: Quadruplet #4'
RW4['TRAP_SURF_NAME_SHORT'] = 'RW4'
RW4['ID_TAG'] = '3.7'
RW4['FT_PIN'] = '3.4'
RW4['INST_ID'] = 'iseg:480933'
RW4['VISA_ID'] = InstID_2_VisaID[RW4['INST_ID']]
RW4['NIDAQ_AI'] = '2'
#RW4['NIDAQ_2_HV_CONVERSION'] = 1000/4.260
RW4['NIDAQ_2_HV_CONVERSION'] = RW1['NIDAQ_2_HV_CONVERSION']
RW4['COLOUR'] = colours[2]
#
#
# ________________________________________________________________________________________________

# ----------------------#                     FT#4                      # ------------------------
# ________________________________________________________________________________________________

#
#____________________ 'Science Trap: end-cap #1' _____________________

Science_EndCap1 = {}
Science_EndCap1['TRAP_SURF_NAME_LONG'] = 'Science Trap: end-cap #1'
Science_EndCap1['TRAP_SURF_NAME_SHORT'] = 'SciTrp:EC1'
Science_EndCap1['ID_TAG'] = '3.1'
Science_EndCap1['FT_PIN'] = '4.1'
Science_EndCap1['INST_ID'] = 'iseg:480934'
Science_EndCap1['VISA_ID'] = InstID_2_VisaID[Science_EndCap1['INST_ID']]
Science_EndCap1['NIDAQ_AI'] = '3'
#Science_EndCap1['NIDAQ_2_HV_CONVERSION'] = 1000/4.260
Science_EndCap1['NIDAQ_2_HV_CONVERSION'] = 221.1746219
Science_EndCap1['COLOUR'] = colours[3]

#____________________ 'Science Trap: centre ring' _____________________

Science_CentreRing = {}
Science_CentreRing['TRAP_SURF_NAME_LONG'] = 'Science Trap: centre ring'
Science_CentreRing['TRAP_SURF_NAME_SHORT'] = 'SciTrp:CR'
Science_CentreRing['ID_TAG'] = '3.2'
Science_CentreRing['FT_PIN'] = '4.2'
Science_CentreRing['INST_ID'] = 'iseg:480996'# previously 'iseg:480935', before switching this unit to egun bias
Science_CentreRing['VISA_ID'] = InstID_2_VisaID[Science_CentreRing['INST_ID']]
Science_CentreRing['NIDAQ_AI'] = '4'
#Science_CentreRing['NIDAQ_2_HV_CONVERSION'] = 1000/4.185
Science_CentreRing['NIDAQ_2_HV_CONVERSION'] = 221.1201484
Science_CentreRing['COLOUR'] = colours[4]

#____________________ 'Science Trap: end-cap #2' _____________________

Science_EndCap2 = {}
Science_EndCap2['TRAP_SURF_NAME_LONG'] = 'Science Trap: end-cap #2'
Science_EndCap2['TRAP_SURF_NAME_SHORT'] = 'SciTrp:EC2'
Science_EndCap2['ID_TAG'] = '3.3'
Science_EndCap2['FT_PIN'] = '4.3'
Science_EndCap2['INST_ID'] = 'ISEG GND' #previously: iseg:480996' #previously: 'iseg:480936', exchanged with egun1 ExB LHS
Science_EndCap2['VISA_ID'] = InstID_2_VisaID[Science_EndCap2['INST_ID']]
Science_EndCap2['NIDAQ_AI'] = '5'
#Science_EndCap2['NIDAQ_2_HV_CONVERSION'] = 1000/4.195
Science_EndCap2['NIDAQ_2_HV_CONVERSION'] = 219.4036463
Science_EndCap2['COLOUR'] = colours[5]

#____________________ 'Wire Mesh' _____________________

WireMesh = {}
WireMesh['TRAP_SURF_NAME_LONG'] = 'Wire Mesh'
WireMesh['TRAP_SURF_NAME_SHORT'] = 'Wire Mesh'
WireMesh['ID_TAG'] = '3.4'
WireMesh['FT_PIN'] = '4.4'
WireMesh['INST_ID'] = 'ISEG GND'
WireMesh['VISA_ID'] = 'ISEG GND'
WireMesh['NIDAQ_AI'] = 'to be filled'

#=================================================================================================

#                          TOP-LEVEL DICTIONARY CALLING E-GUN SURFACES

#=================================================================================================

egun1_surf_dict = OrderedDict()


egun1_surf_dict['Electron Gun #1: emission-bias']= egun1_emission_bias           
egun1_surf_dict['Electron Gun #1: emission-source']= egun1_emission_source    

egun1_surf_dict['Electron Gun #1: cathode plate']= egun1_cathode           
egun1_surf_dict['Electron Gun #1: anode plate']= egun1_anode    
       
egun1_surf_dict['Electron Gun #1: ExB plate (LHS)']= egun1ExB_LHS            
egun1_surf_dict['Electron Gun #1: ExB plate (RHS)']= egun1ExB_RHS

                
egun2_surf_dict = OrderedDict()               
               
egun2_surf_dict['Electron Gun #2: emission-bias']= egun2_emission_bias           
egun2_surf_dict['Electron Gun #2: cathode plate']= egun2_cathode           
egun2_surf_dict['Electron Gun #2: anode plate']= egun2_anode       
    
egun2_surf_dict['Electron Gun #2: ExB plate (LHS)']= egun2ExB_LHS            
egun2_surf_dict['Electron Gun #2: ExB plate (RHS)']= egun2ExB_RHS

               
#=================================================================================================

#                          TOP-LEVEL DICTIONARY CALLING TRAP-SUFRACES   

#=================================================================================================


trap_surf_dict = OrderedDict()

trap_surf_dict['Loading Trap: end-cap #1']= Loading_EndCap1
trap_surf_dict['Loading Trap: centre ring']= Loading_CentreRing
trap_surf_dict['Loading Trap: end-cap #2']= Loading_EndCap2

trap_surf_dict['Rotating Wall: Quadruplet #1']= RW1
trap_surf_dict['Rotating Wall: Quadruplet #2']= RW2
trap_surf_dict['Rotating Wall: Quadruplet #3']= RW3
trap_surf_dict['Rotating Wall: Quadruplet #4']= RW4

trap_surf_dict['Science Trap: end-cap #1']= Science_EndCap1
trap_surf_dict['Science Trap: centre ring']= Science_CentreRing
trap_surf_dict['Science Trap: end-cap #2']= Science_EndCap2

trap_surf_dict['Wire Mesh']= WireMesh

#=================================================================================================

#      TOP-LEVEL DICTIONARY CALLING TRAP-SUFRACES TO BE CONTROLLED BY ISEG HV POWER SUPPLY 

#=================================================================================================


iseg_controlled_trap_surfaces = OrderedDict()

    #iseg_controlled_trap_surfaces['Loading Trap: end-cap #1']= Loading_EndCap1

iseg_controlled_trap_surfaces['Loading Trap: centre ring']= Loading_CentreRing
iseg_controlled_trap_surfaces['Loading Trap: end-cap #2']= Loading_EndCap2

iseg_controlled_trap_surfaces['Rotating Wall: Quadruplet #1']= RW1

iseg_controlled_trap_surfaces['Science Trap: end-cap #1']= Science_EndCap1
iseg_controlled_trap_surfaces['Science Trap: centre ring']= Science_CentreRing
#iseg_controlled_trap_surfaces['Science Trap: end-cap #2']= Science_EndCap2

    #iseg_controlled_trap_surfaces['Wire Mesh']= WireMesh

#=================================================================================================

#      TOP-LEVEL DICTIONARY CALLING EGUN-SUFRACES TO BE CONTROLLED BY ISEG HV POWER SUPPLY 

#=================================================================================================

MX100TP_controlled_egun_surfaces = OrderedDict()                               
iseg_controlled_egun_surfaces = OrderedDict() 

MX100TP_controlled_egun_surfaces['Electron Gun #1: cathode plate']= egun1_cathode           
MX100TP_controlled_egun_surfaces['Electron Gun #1: anode plate']= egun1_anode 

MX100TP_controlled_egun_surfaces['Electron Gun #1: emission-source']= egun1_emission_source                  
iseg_controlled_egun_surfaces['Electron Gun #1: emission-bias']= egun1_emission_bias   

iseg_controlled_egun_surfaces['Electron Gun #1: ExB plate (LHS)']= egun1ExB_LHS            
iseg_controlled_egun_surfaces['Electron Gun #1: ExB plate (RHS)']= egun1ExB_RHS   
   
   
               
               


