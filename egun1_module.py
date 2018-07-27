# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 18:03:24 2017

@author: Harrison Ball
"""

from pyqtgraph.Qt import QtCore
from PyQt4.Qt import QMutex

from Penning_trap_cxn_dictionaries import egun1_surf_dict, iseg_controlled_egun_surfaces, MX100TP_controlled_egun_surfaces
from voltage_configuration_dictionary import volt_config_dict

from instrument_command import ISEG_Command
from instrument_command import MX100TP_Command


#=================================================================================================

#                   DEFINE CLASS FOR COMMANDING THE ISEG HV POWER SUPPLY

#=================================================================================================

class egun1_control(QtCore.QObject):
    """ Set up the connections for the instruments for controlling egun plate surfaces """
    #ramp_finished = QtCore.pyqtSignal()    
       
    def __init__(self):
        QtCore.QObject.__init__(self)
        
        self.egun1_surfs_iseg = iseg_controlled_egun_surfaces.keys()
        self.egun1_surfs_MX100TP = MX100TP_controlled_egun_surfaces.keys()
        self.egun1_surfs_all = self.egun1_surfs_MX100TP+self.egun1_surfs_iseg        
        self.INST_IDs_iseg_egun1 = [egun1_surf_dict[self.egun1_surfs_iseg[i]]['INST_ID'] for i in range(len(self.egun1_surfs_iseg))]
        self.VISA_IDs_iseg_egun1 = [egun1_surf_dict[self.egun1_surfs_iseg[i]]['VISA_ID'] for i in range(len(self.egun1_surfs_iseg))]
                                    
        self.INST_IDs_MX100TP_egun1 = [egun1_surf_dict[self.egun1_surfs_MX100TP[i]]['INST_ID'] for i in range(len(self.egun1_surfs_MX100TP))]
        self.VISA_IDs_MX100TP_egun1 = [egun1_surf_dict[self.egun1_surfs_MX100TP[i]]['VISA_ID'] for i in range(len(self.egun1_surfs_MX100TP))]                                       
        self.VISA_ID_MX100TP_egun1 = self.VISA_IDs_MX100TP_egun1[0]
                                   
        # create iseg modele objects for egun control
        self.iseg_modules_egun1 = ISEG_Command(self.VISA_IDs_iseg_egun1)
        # create MX100TP modele object for egun control
        self.MX100TP_module_egun1 = MX100TP_Command(self.VISA_ID_MX100TP_egun1)
                   
        self.execute_default_settings()

        self.running = True
        
        self.update_MX100TP_voltages = None     
        
        self.temp_volt_dict = None            
        
        self.mutex  = QMutex()
            

    def execute_default_settings(self):   
        self.kill_output()
        
        self.MX100TP_module_egun1.reset()
        #SET DEFAULT VOLTAGE RANGES ON MX100TP CHANNELS                    
        self.MX100TP_module_egun1.set_output_voltage_range(1,1)
        self.MX100TP_module_egun1.set_output_voltage_range(2,1)
        self.MX100TP_module_egun1.set_output_voltage_range(3,2)


        #DEFAULT VOLTAGE OVERPROTECTION AND SET VOLTAGE VALUES FOR MX100TP    
        for i in range(len(self.egun1_surfs_MX100TP)): 
            channel = egun1_surf_dict[self.egun1_surfs_MX100TP[i]]['INST_CHANNEL'] 
            V_OP = volt_config_dict[self.egun1_surfs_MX100TP[i]]['V_OP'] 
            I_OP = volt_config_dict[self.egun1_surfs_MX100TP[i]]['I_OP'] 
            V_set = volt_config_dict[self.egun1_surfs_MX100TP[i]]['V_set'] 
            I_set = volt_config_dict[self.egun1_surfs_MX100TP[i]]['I_set'] 
            self.MX100TP_module_egun1.set_V_OP(channel,V_OP)
            self.MX100TP_module_egun1.set_I_OP(channel,I_OP)
            self.MX100TP_module_egun1.set_voltage_setpoint(channel,V_set)
            self.MX100TP_module_egun1.set_current_setpoint(channel,I_set)
        #self.MX100TP_module_egun1.set_all_outputs(1)
        
        #DEFAULT SET VOLTAGE VALUES FOR  EXB PLATES  (ISEG HV)  
        V_set_iseg_startup = [0.01 for i in range(len(self.egun1_surfs_iseg))]  
        self.iseg_modules_egun1.set_initial_voltages(V_set_iseg_startup)

    def set_voltage_and_current_setpoints(self):
        #UPDATE VOLTAGE AND CURRENT SETPOINT VALUES ON MX100TP FROM TVD (PASSED FROM MAIN WINDOW), WITHOUT OUTPUT DEPLOYMENT
        for i in range(len(self.egun1_surfs_MX100TP)): 
            channel = egun1_surf_dict[self.egun1_surfs_MX100TP[i]]['INST_CHANNEL'] 
            V_set = self.temp_volt_dict[self.egun1_surfs_MX100TP[i]]['V_set']
            I_set = self.temp_volt_dict[self.egun1_surfs_MX100TP[i]]['I_set']
            self.MX100TP_module_egun1.set_voltage_setpoint(channel,V_set)
            self.MX100TP_module_egun1.set_current_setpoint(channel,I_set)
            
        
    def deploy_voltage_and_current_outputs(self):   
        
        #SET UPDATED SETPOINTS AND DEPLOY OUTPUTS ON MX100TP                 
        #self.set_voltage_and_current_setpoints(self)    
        self.MX100TP_module_egun1.set_all_outputs(1)    
        
        #UPDATE SET VOLTAGES (AND DEPLOY OUTPUT) ON ISEG MODULES FOR egun1, FROM TVD (PASSED FROM MAIN WINDOW) 
        V_list_iseg = [self.temp_volt_dict[self.egun1_surfs_iseg[i]]['V_set'] for i in range(len(self.egun1_surfs_iseg))]  
        self.iseg_modules_egun1.set_initial_voltages(V_list_iseg)
                
        
    def voltage_readback_all(self):  
        
        Vreadback_MX100TP = [self.MX100TP_module_egun1.voltage_output_readback(egun1_surf_dict[self.egun1_surfs_MX100TP[i]]['INST_CHANNEL']) for i in range(len(self.egun1_surfs_MX100TP))]       
        #print 'MX:'+ str(Vreadback_MX100TP)
        Vreadback_iseg =self.iseg_modules_egun1.measure_volts()     
        #print 'iseg:' +str(Vreadback_iseg)
        return Vreadback_MX100TP+Vreadback_iseg
        
        
    def current_readback_all(self):  
        
        Ireadback_MX100TP = [self.MX100TP_module_egun1.current_output_readback(egun1_surf_dict[self.egun1_surfs_MX100TP[i]]['INST_CHANNEL']) for i in range(len(self.egun1_surfs_MX100TP))]       
        #print 'MX:'+ str(Vreadback_MX100TP)
        Ireadback_iseg =self.iseg_modules_egun1.measure_currents()     
        #print 'iseg:' +str(Vreadback_iseg)
        return Ireadback_MX100TP+Ireadback_iseg
 
        
    #def turn_ON(self):     
    #    self.MX100TP_module_egun1.set_all_outputs(1)    
    
    def kill_output(self):
        print 'egun1_module: kill all outputs'
        self.MX100TP_module_egun1.set_all_outputs(0)  
        
        V_set_iseg_zero = [0.01 for i in range(len(self.egun1_surfs_iseg))]  
        self.iseg_modules_egun1.set_initial_voltages(V_set_iseg_zero)
        
    def read_voltage_range_MX100TP(self,channel):
        return self.MX100TP_module_egun1.read_output_voltage_range(channel)
        

    def read_V_OP_MX100TP(self,channel):
        return self.MX100TP_module_egun1.read_V_OP(channel)  
        
    def read_I_OP_MX100TP(self,channel):
        return self.MX100TP_module_egun1.read_I_OP(channel)  