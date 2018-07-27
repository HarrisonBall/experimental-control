# -*- coding: utf-8 -*-
"""
2018-03-02, v2 RW
    - proble with ramps im shutteling mode: list voltage not always reached, just randomly
    - origin: calculation of ramp speeds = (V(t)-V(t-1))/timestep leaves no room to compensate for 
        voltages not reached, therefore errors add up
    - function to be changed: "def calculate_ramp_speeds(self, tau, V_ramp_list):"
        include factor of 0.9 before tau(=timestep), therefore ramp is always 10% faster than necessary
        giving some headroom to reach voltage before not timestep starts
    
2018-03-02, v2 RW
    - loads Penning_trap_cxn_dictionaries_v2 which includes all trap electrodes and no egaun stuff
    - LTCE1 and STEC2 voltage readbacks have to be calibrated

Created on Mon Feb 27 18:03:24 2017

@author: Harrison Ball
"""

#=================================================================================================

#           DEFINE CLASS FOR COMMANDING ALL TRAP SURFACES VIA ISEG HV POWER SUPPLIES 

#=================================================================================================


import numpy as np
import pyqtgraph as pg
import time
import datetime
#from PyQt4 import QtCore, QtGui
from copy import deepcopy
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.Qt import QMutex

from Penning_trap_cxn_dictionaries_v2 import trap_surf_dict, iseg_controlled_trap_surfaces
from voltage_configuration_dictionary_v2 import volt_config_dict

from instrument_command import ISEG_Command

class trap_control(QtCore.QObject):
    """ Set up the connections for the instruments for controlling trap plate surfaces """
    shuttling_finished = QtCore.pyqtSignal()  
       
    def __init__(self):
        QtCore.QObject.__init__(self)
        
        #Read from Penning_trap_cxn_dictionaries relevant information mapping ISEG units to trap 
        #surfaces in order to start the relevant sessions. 
        self.trap_surfaces = iseg_controlled_trap_surfaces.keys()
        self.num_trap_surfs = len(self.trap_surfaces) 
        self.INST_IDs_4_TRAP_SURFs = [trap_surf_dict[self.trap_surfaces[i]]['INST_ID'] for i in range(len(self.trap_surfaces))]
        self.VISA_IDs_4_TRAP_SURFs = [trap_surf_dict[self.trap_surfaces[i]]['VISA_ID'] for i in range(len(self.trap_surfaces))]
                                                                       
        # Setup connections to individual iseg units assigned to trap surface control
        self.iseg_modules = ISEG_Command(self.VISA_IDs_4_TRAP_SURFs)
                   
        self.running = True
                           
        self.temp_volt_dict = deepcopy(volt_config_dict)
        self.create_thread_shuttling()
        self.mutex  = QMutex()
        self.colours = [trap_surf_dict[c]['COLOUR'] for c in self.trap_surfaces]

        self.num_completed_shuttling_cycles = 0
        self.reinitialize_shuttling_sequence = True
          
    def read_command_parameters_from_VCD(self):   
        '''Read all command parameters relevant to controlling trap surfaces via ISEG modules from
        the default voltage configuration dictionary (VCD)'''
        self.num_time_segs = volt_config_dict['global ramping parameters']['num_time_segs']
        self.tau = volt_config_dict['global ramping parameters']['tau']
        self.num_shuttling_cycles = volt_config_dict['global ramping parameters']['num_shuttling_cycles']
        self.repetition_time_delay = volt_config_dict['global ramping parameters']['repetition_time_delay']
        self.V_initial_list = [volt_config_dict[c]['V_initial'] for c in self.trap_surfaces]
        self.V_final_list = [volt_config_dict[c]['V_final'] for c in self.trap_surfaces]
        self.V_ramp_list_array = self.stack_voltage_lists() 
        self.ramp_speed_list_array = self.stack_ramp_speed_lists()
    
    def read_command_parameters_from_TVD(self):   
        '''Read all command parameters relevant to controlling trap surfaces via ISEG modules from
        the temporary voltage dictionary (TVD) to allow user updates from GUI'''
        self.num_time_segs = self.temp_volt_dict['global ramping parameters']['num_time_segs']
        self.tau = self.temp_volt_dict['global ramping parameters']['tau']
        self.num_shuttling_cycles = self.temp_volt_dict['global ramping parameters']['num_shuttling_cycles']
        self.repetition_time_delay = self.temp_volt_dict['global ramping parameters']['repetition_time_delay']
        self.V_initial_list = [self.temp_volt_dict[c]['V_initial'] for c in self.trap_surfaces]
        self.V_final_list = [self.temp_volt_dict[c]['V_final'] for c in self.trap_surfaces]
        self.V_ramp_list_array = self.stack_voltage_lists() 
        self.ramp_speed_list_array = self.stack_ramp_speed_lists()
      
    def stack_voltage_lists(self):
        V_ramp_list_array = np.empty((0,self.num_time_segs+1), int)
        for c in self.trap_surfaces:
            V_ramp_list_array = np.vstack((V_ramp_list_array, self.temp_volt_dict[c]['V_ramp_list']))
        return V_ramp_list_array

    def stack_ramp_speed_lists(self):
        ramp_speed_list_array = np.empty((0,self.num_time_segs), int)
        for c in self.trap_surfaces:
            ramp_speed_list_array = np.vstack((ramp_speed_list_array, self.calculate_ramp_speeds(self.temp_volt_dict['global ramping parameters']['tau'], self.temp_volt_dict[c]['V_ramp_list'])))
        return ramp_speed_list_array 
        
    def calculate_ramp_speeds(self, tau, V_ramp_list):
        return [abs((abs(V_ramp_list[k+1])-abs(V_ramp_list[k]))/(0.9*tau)) for k in range(len(V_ramp_list)-1)] 
        #return [abs((abs(V_ramp_list[k+1])-abs(V_ramp_list[k]))/tau) for k in range(len(V_ramp_list)-1)] 
        #return [200 for k in range(len(V_ramp_list)-1)] 
    
    def send_command_parameters_to_iseg_modules(self):    
        
        self.read_command_parameters_from_TVD()
        self.iseg_modules.num_time_segs = self.num_time_segs
        self.iseg_modules.tau = self.tau  
        self.iseg_modules.repetition_time_delay = self.repetition_time_delay
        self.iseg_modules.V_initial_list = self.V_initial_list
        self.iseg_modules.V_final_list = self.V_final_list
        self.iseg_modules.V_ramp_list_array =  self.V_ramp_list_array
        self.iseg_modules.ramp_speed_list_array = self.ramp_speed_list_array 

#_________________________________________________________________________________________________

#                                 *  SET INITIAL VOLTAGES 
#                                 *  SET FINAL VOLTAGES 
#_________________________________________________________________________________________________
        
    def set_Vinitial_voltages(self):
        self.iseg_modules.set_initial_voltages(self.V_initial_list)   
        
    def set_Vfinal_voltages(self):
        self.iseg_modules.set_final_voltages(self.V_final_list)  

#_________________________________________________________________________________________________

#                               CONTROL COMMANDS FOR SHUTTLING SEQUENCE  
#_________________________________________________________________________________________________

    def create_thread_shuttling(self):
        self.running = True
        self.thread_shuttling = QtCore.QThread()
        self.iseg_modules.moveToThread(self.thread_shuttling)
        self.thread_shuttling.started.connect(self.iseg_modules.ramp_sequence) 
        self.iseg_modules.ramp_finished.connect(self.repeat_shuttling_sequence)
        
    def close_thread_shuttling(self):
        ''' Use ramp_finished signal from iseg_modules to close threads at conclusion of shuttling sequence '''
        self.running = False
        self.iseg_modules.running = self.running
        self.thread_shuttling.quit()
        self.num_completed_shuttling_cycles = 0
        self.shuttling_finished.emit()
        print 'trap_sufrace_module: threads closed'
        
        
    def start_shuttling_sequence(self):
        
        print 'trap_sufrace_module: start shuttling sequence'
        self.running = True
        self.iseg_modules.running = self.running
        self.num_completed_shuttling_cycles = 0
        self.reinitialize_shuttling_sequence = True      
        
        self.send_command_parameters_to_iseg_modules()
        
        #Start the thread associated with initiating shuttling sequence 
        self.thread_shuttling.start() 

    def repeat_shuttling_sequence(self):
       
        if self.running:
            self.num_shuttling_cycles = self.temp_volt_dict['global ramping parameters']['num_shuttling_cycles']
            self.num_completed_shuttling_cycles +=1
            self.reinitialize_shuttling_sequence = self.num_completed_shuttling_cycles<self.num_shuttling_cycles
        
            print 'trap_sufrace_module: repeat cycles completed: {}/{}'.format(str(self.num_completed_shuttling_cycles), self.num_shuttling_cycles)
           
            if self.num_completed_shuttling_cycles == self.num_shuttling_cycles:
                print 'trap_sufrace_module: do not reset initial voltages, final shuttling cycle completed.'
                self.close_thread_shuttling() 
            else:
                if self.reinitialize_shuttling_sequence == True: 
                    print 'trap_sufrace_module: reset initial voltages for next shuttling cycle.'
                    self.send_command_parameters_to_iseg_modules() 
                    self.set_Vinitial_voltages()                        
                    self.thread_shuttling.quit()
                    time.sleep(0.1)
                    self.thread_shuttling.start() # Start the next ramp
  
    def close_sessions_iseg_trap_surfs(self, event):
        '''close communication channels to iseg units for trap surfaces '''
        if self.iseg_modules is not None:
            self.iseg_modules.close()
        print 'trap_sufrace_module: VISA connections closed for trap surfaces.'

#_________________________________________________________________________________________________

#                               SAVE SHUTTLING VOLTAGES TO TXT FILE   
#_________________________________________________________________________________________________
        
    def save_to_txt(self,FullData__shuttling):
        print 'trap_sufrace_module: shuttling sequence: txt file created'
        FileName__shuttling = "[log_trap_voltages_shuttling] {}".format(str(datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")) )
        DatafilePath__shuttling = "Y:/Beryllium Lab/Projects/Project_experimental_control/Penning_system_control_program/data_log/log_trap_voltages_shuttling/"+FileName__shuttling+".txt"
        DataFile_ID_shuttling = open(DatafilePath__shuttling, 'w+')
        
        #here you open the ascii file
                
        fmt_str = ['%-14.14s']*(1+self.num_trap_surfs)
        
        header_str='\n'.join(["Log of trap voltages for shuttling procedure. Data measured from NI DAQ on iseg EHQ 102M modules.", 
                              str(datetime.datetime.now().strftime("%y.%m.%d\t%H:%M:%S")) + "\t" + str(time.time()),
                              ""])
                         
        INST_IDs_4_TRAP_SURFs_str = ['{}'.format(self.INST_IDs_4_TRAP_SURFs[i]) for i in range(self.num_trap_surfs)]
        INST_IDs_4_TRAP_SURFs_str.insert(0,"")
        
        TRAP_SURF_NAME_str = [trap_surf_dict[self.trap_surfaces[i]]['TRAP_SURF_NAME_SHORT'] for i in range(self.num_trap_surfs)]
        TRAP_SURF_NAME_str.insert(0,"") 

        data_labels_str = ['volts [V]']*(self.num_trap_surfs)
        data_labels_str.insert(0,"time [s]")
        
        break_str = [""]*(self.num_trap_surfs+1)
        
        str_data = np.vstack((TRAP_SURF_NAME_str, INST_IDs_4_TRAP_SURFs_str, data_labels_str, break_str, FullData__shuttling.astype(str)))
        
        #np.savetxt('test_array.txt', str_data, header=header_str, fmt=fmt_str)
        np.savetxt(DataFile_ID_shuttling, str_data, fmt=fmt_str, header=header_str)
        #here the ascii file is populated.