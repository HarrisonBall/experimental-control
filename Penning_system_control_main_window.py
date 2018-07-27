# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 13:12:45 2017

@author: Harrison Ball
"""
#=================================================================================================
#=================================================================================================

#  -----------    MAIN WINDOW FOR EXECUTING SHUTTLING SEQUENCE ON ISEG HV SUPPLY    --------------

#=================================================================================================
#=================================================================================================


import time, sys
import datetime
import os.path
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from copy import deepcopy
import numpy as np

from Penning_trap_cxn_dictionaries import trap_surf_dict, iseg_controlled_trap_surfaces, egun1_surf_dict
from voltage_configuration_dictionary import volt_config_dict

from instrument_command import NI_USB_6259_Command

import egun1_module
import trap_surfaces_module

class MainWin(QtGui.QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        
        self.setDockOptions(QtGui.QMainWindow.AnimatedDocks | QtGui.QMainWindow.AllowNestedDocks)                            

        self.running = True

        self.setup_control_system()

        self.create_ctrl_panel()
        
#=================================================================================================

#                     SETUP ALL INSTRUMENT CONTROL AND MONITORING OBJECTS

#=================================================================================================

    def setup_control_system(self):    

        self.temp_volt_dict = deepcopy(volt_config_dict)
        
        #setup parameters for controlling trap surfaces
        self.trap_surfaces = iseg_controlled_trap_surfaces.keys()                
        self.num_trap_surfs = len(self.trap_surfaces)  
        self.colours = [trap_surf_dict[c]['COLOUR'] for c in self.trap_surfaces]

        #setup control object for trap surfaces
        self.trap_control = trap_surfaces_module.trap_control()
        self.trap_control.iseg_modules.update_TVD.connect(self.update_shuttling_control_parameters_continuously)
     
        #setup parameters for shuttling 
        self.num_time_segs = self.temp_volt_dict['global ramping parameters']['num_time_segs']
        self.tau = self.temp_volt_dict['global ramping parameters']['tau']
        self.num_shuttling_cycles = self.temp_volt_dict['global ramping parameters']['num_shuttling_cycles']
        self.repetition_time_delay = self.temp_volt_dict['global ramping parameters']['repetition_time_delay']
       
        #setup plot environment for monitoring voltages on trap surfaces
        self.pg_curves = []
        self.setup_plots_shuttling()
                        
        #start session for NI USB-6259 for data acquisition
        self.nidaq = NI_USB_6259_Command() 
        
        #setup control object for egun#1 
        self.egun1_control = egun1_module.egun1_control()
        self.egun1_surfs_all = self.egun1_control.egun1_surfs_all  
        
        #scales
        self.micro = 10**(-6)
        
#=================================================================================================

#                                  CREATE GUI CONTROL PANEL   

#=================================================================================================
   
    def create_TabWidget(self, widget_list, widget_title_list): 
        '''Create a QtGui.QTabWidget object to which all individual tabs are added, by specification
        of listed widget objects and corresponding titles.'''
        self.tabWidget = QtGui.QTabWidget(self) 
        
        for i in range(len(widget_list)):
            self.tabWidget.addTab(widget_list[i], widget_title_list[i])

        
  
    def create_ctrl_panel(self):
                
        self.create_tab_egun1()
        
        self.create_tab_Vinitial()
        
        self.create_tab_shuttling()
        
        self.create_tab_Vfinal()
        
        self.create_tab_monitor_trap_voltages()
                
        self.create_TabWidget([self.tab_egun1, self.tab_Vinitial, self.tab_shuttling, self.tab_Vfinal, self.tab_monitor_trap_voltages], ['e-gun #1', 'Initial/Loading Voltages','Ion Shuttling','Final Trap Voltages', 'Monitor Trap Voltages'])
        
        self.ctrl_dock = QtGui.QDockWidget('Control panel')
        
        self.ctrl_dock.setWidget(self.tabWidget)
        
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.ctrl_dock)
        
        self.connect_GUI_buttons_to_actions()

#=================================================================================================

#                                    CREATE/POPULATE GUI TAB
#                                        BERYLLIUM OVENS 

#=================================================================================================
    '''    
    def create_tab_Be_ovens(self):       
       
       self.tab_Be_ovens = QtGui.QWidget()

       self.table_Widget_Be_ovens = QtGui.QTableWidget()
       self.populate_table_Be_ovens()
       
       tab_layout_Be_ovens = QtGui.QVBoxLayout()
       
       button_HLayout_Be_ovens = QtGui.QHBoxLayout()
       self.button_set_setpoints_voltage_and_current_Be_ovens = QtGui.QPushButton("Set Setpoints")      
       self.button_set_setpoints_and_deploy_outputs_voltage_and_current_Be_ovens = QtGui.QPushButton("Output ON")       
       self.button_kill_output_Be_ovens = QtGui.QPushButton("Output OFF")       
       self.button_update_instrument_readback_values_Be_ovens_writeGUI = QtGui.QPushButton("Update Instrument Readback")      
       self.button_restore_default_settings_Be_ovens = QtGui.QPushButton("Default Settings")
                   
       button_HLayout_Be_ovens.addWidget(self.button_restore_default_settings_Be_ovens)
       button_HLayout_Be_ovens.addWidget(self.button_update_instrument_readback_values_Be_ovens_writeGUI)
       button_HLayout_Be_ovens.addStretch(1)
       button_HLayout_Be_ovens.addWidget(self.button_set_setpoints_voltage_and_current_Be_ovens)
       button_HLayout_Be_ovens.addWidget(self.button_kill_output_Be_ovens)
       button_HLayout_Be_ovens.addWidget(self.button_set_setpoints_and_deploy_outputs_voltage_and_current_Be_ovens)
             
       tab_layout_Be_ovens.addWidget(self.table_Widget_Be_ovens)       
       tab_layout_Be_ovens.addLayout(button_HLayout_Be_ovens)
           
       self.tab_Be_ovens.setLayout(tab_layout_Be_ovens) 
    '''   
#=================================================================================================

#                                    CREATE/POPULATE GUI TAB
#                                    EGUN POTENTIAL SURFACES

#=================================================================================================
        
    def create_tab_egun1(self):       
       
       self.tab_egun1 = QtGui.QWidget()

       self.table_Widget_egun1 = QtGui.QTableWidget()
       self.populate_table_egun1()
       
       tab_layout_egun1 = QtGui.QVBoxLayout()
       
       button_HLayout_egun1 = QtGui.QHBoxLayout()
       self.button_set_setpoints_voltage_and_current_egun1 = QtGui.QPushButton("Set Setpoints")      
       self.button_set_setpoints_and_deploy_outputs_voltage_and_current_egun1 = QtGui.QPushButton("Output ON")       
       
       self.button_kill_output_egun1 = QtGui.QPushButton("Output OFF")
       self.toggle_state_OFF_egun1()  
       
       self.button_update_instrument_readback_values_egun1_writeGUI = QtGui.QPushButton("Update Instrument Readback")      
       self.button_restore_default_settings_egun1 = QtGui.QPushButton("Default Settings")
                   
       button_HLayout_egun1.addWidget(self.button_restore_default_settings_egun1)
       button_HLayout_egun1.addWidget(self.button_update_instrument_readback_values_egun1_writeGUI)
       button_HLayout_egun1.addStretch(1)
       button_HLayout_egun1.addWidget(self.button_set_setpoints_voltage_and_current_egun1)
       button_HLayout_egun1.addWidget(self.button_kill_output_egun1)
       button_HLayout_egun1.addWidget(self.button_set_setpoints_and_deploy_outputs_voltage_and_current_egun1)
           
       tab_layout_egun1.addWidget(self.table_Widget_egun1)       
       tab_layout_egun1.addLayout(button_HLayout_egun1)
           
       self.tab_egun1.setLayout(tab_layout_egun1) 
                  
        
    def populate_table_egun1(self):  
        
        ncols = 11
        nrows = len(self.egun1_surfs_all)
        self.table_Widget_egun1.setColumnCount(ncols)
        self.table_Widget_egun1.setRowCount(nrows)
                
        for i in range(ncols):
            clabels = ['Surface', 'FT PIN', 'Instrument','Channel', 'V/I range','V_OP [V]','I_OP [A]', 'Vset [V]', 'Iset [A]', 'Vreadback [V]', 'Ireadback [A]']
            colours = ['Indian Red', 'Indian Red','Indian Red','Indian Red','Light Blue','Light Blue','Light Blue','Light Blue','Light Blue','Light Blue','Light Blue']
            h_item = QtGui.QTableWidgetItem(clabels[i])
            h_item.setBackground(QtGui.QColor(colours[i]))
            self.table_Widget_egun1.setHorizontalHeaderItem(i, h_item)

        FT_PINs_egun1 = [egun1_surf_dict[self.egun1_surfs_all[i]]['FT_PIN'] for i in range(len(self.egun1_surfs_all))]
        INST_IDs_egun1 = [egun1_surf_dict[self.egun1_surfs_all[i]]['INST_ID'] for i in range(len(self.egun1_surfs_all))]
        INST_CHANNELs_egun1 = [str(egun1_surf_dict[self.egun1_surfs_all[i]]['INST_CHANNEL']) for i in range(len(self.egun1_surfs_all))]
        V_OP_egun1 = [str(self.temp_volt_dict[self.egun1_surfs_all[i]]['V_OP']) for i in range(len(self.egun1_surfs_all))]
        I_OP_egun1 = [str(self.temp_volt_dict[self.egun1_surfs_all[i]]['I_OP']) for i in range(len(self.egun1_surfs_all))]
        V_set_egun1 = [str(self.temp_volt_dict[self.egun1_surfs_all[i]]['V_set']) for i in range(len(self.egun1_surfs_all))]    
        I_set_egun1 = [str(self.temp_volt_dict[self.egun1_surfs_all[i]]['I_set']) for i in range(len(self.egun1_surfs_all))]
        V_readback_egun1 = self.egun1_control.voltage_readback_all()  
        I_readback_egun1 = self.egun1_control.current_readback_all()  

        for j in range(nrows):
            #COLUMN 1: SURFACE NAME
            newItem = QtGui.QTableWidgetItem(self.egun1_surfs_all[j])
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_Widget_egun1.setItem(j, 0, newItem)
        
        for j in range(nrows):
            #COLUMN 2: FT PIN
            newItem = QtGui.QTableWidgetItem(FT_PINs_egun1[j])
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_Widget_egun1.setItem(j, 1, newItem)

        for j in range(nrows):
            #COLUMN 3: INSTRUMENT ID 
            newItem = QtGui.QTableWidgetItem(INST_IDs_egun1[j])
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_Widget_egun1.setItem(j, 2, newItem)
            
        for j in range(nrows):
            #COLUMN 4: INSTRUMENT CHANNEL
            newItem = QtGui.QTableWidgetItem(INST_CHANNELs_egun1[j])
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_Widget_egun1.setItem(j, 3, newItem)
            
        for j in range(nrows):
            #COLUMN 5: INSTRUMENT VOLTAGE RANGE 
            if INST_IDs_egun1[j]=='MX100TP:436129':   
                newItem = QtGui.QTableWidgetItem(self.egun1_control.read_voltage_range_MX100TP(INST_CHANNELs_egun1[j]))
                newItem.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table_Widget_egun1.setItem(j, 4, newItem)
            else:
                newItem = QtGui.QTableWidgetItem('N/A')
                newItem.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table_Widget_egun1.setItem(j, 4, newItem)
            
        for j in range(nrows):
            #COLUMN 6: VOLTAGE OVER PROTECTION
            newItem = QtGui.QTableWidgetItem(V_OP_egun1[j])
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_Widget_egun1.setItem(j, 5, newItem)   
            
        for j in range(nrows):
            #COLUMN 7: CURRENT OVER PROTECTION 
            newItem = QtGui.QTableWidgetItem(I_OP_egun1[j])
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_Widget_egun1.setItem(j, 6, newItem)
            
        for j in range(nrows):
            #COLUMN 8: VOLTAGE SET VALUE
            newItem = QtGui.QTableWidgetItem(V_set_egun1[j])
            newItem.setBackground(QtGui.QColor('Medium Sea Green'))
            self.table_Widget_egun1.setItem(j, 7, newItem)  
            
        for j in range(nrows):
            #COLUMN 9: CURRNET SET VALUE
            newItem = QtGui.QTableWidgetItem(I_set_egun1[j])
            if self.egun1_surfs_all[j] == 'Electron Gun #1: emission-source': 
                newItem.setBackground(QtGui.QColor('Medium Sea Green'))
                self.table_Widget_egun1.setItem(j, 8, newItem)      
            else:
                newItem.setFlags(QtCore.Qt.ItemIsEnabled)
                newItem.setBackground(QtGui.QColor('Light Slate Gray'))
                self.table_Widget_egun1.setItem(j, 8, newItem) 
                
   
        for j in range(nrows):
            #COLUMN 10: VOLTAGE READBACK
            newItem = QtGui.QTableWidgetItem(str(V_readback_egun1[j]))
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_Widget_egun1.setItem(j, 9, newItem) 

        for j in range(nrows):
            #COLUMN 11: CURRENT READBACK
            newItem = QtGui.QTableWidgetItem(str(I_readback_egun1[j]))
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_Widget_egun1.setItem(j, 10, newItem) 

        self.table_Widget_egun1.resizeColumnsToContents()
       
#=================================================================================================

#                                   CREATE/POPULATE GUI TAB
#                                    TRAP INITIAL VOLTAGES  

#=================================================================================================
        
    def create_tab_Vinitial(self):       
       self.tab_Vinitial = QtGui.QWidget()
      
       self.table_Widget_Vinitial = QtGui.QTableWidget()
       self.populate_table_Vinitial()

       self.button_set_Vinitial = QtGui.QPushButton("Set Voltages")              
       self.button_restore_default_settings_Vinitial = QtGui.QPushButton("Default Settings")
      
       button_HLayout_Vinitial = QtGui.QHBoxLayout()
       button_HLayout_Vinitial.addWidget(self.button_restore_default_settings_Vinitial)
       button_HLayout_Vinitial.addStretch(1)
       button_HLayout_Vinitial.addWidget(self.button_set_Vinitial)
       
       tab_layout_Vinitial = QtGui.QVBoxLayout()
       tab_layout_Vinitial.addWidget(self.table_Widget_Vinitial)
       
       tab_layout_Vinitial.addLayout(button_HLayout_Vinitial)
       
       self.tab_Vinitial.setLayout(tab_layout_Vinitial)
        
    def populate_table_Vinitial(self):        
        self.table_Widget_Vinitial.setColumnCount(self.num_trap_surfs)
        self.table_Widget_Vinitial.setRowCount(1)
            
        for i in range(self.num_trap_surfs):
            h_item = QtGui.QTableWidgetItem(self.trap_surfaces[i])
            h_item.setBackground(QtGui.QColor(self.colours[i]))
            self.table_Widget_Vinitial.setHorizontalHeaderItem(i, h_item)
            
        columnData_Vinitial = [self.temp_volt_dict[self.trap_surfaces[i]]['V_initial'] for i in range(self.num_trap_surfs)]  
                      

        for i in range(self.num_trap_surfs):

            newItem = QtGui.QTableWidgetItem(str(columnData_Vinitial[i]))
            self.table_Widget_Vinitial.setItem(0, i, newItem)
         
        self.table_Widget_Vinitial.resizeColumnsToContents()
        self.table_Widget_Vinitial.resizeRowsToContents()

#=================================================================================================

#                                    CREATE/POPULATE GUI TAB
#                                    TRAP SHUTTLING VOLTAGES  

#=================================================================================================
      
    def create_tab_shuttling(self):       
       self.tab_shuttling = QtGui.QWidget()
      
       self.table_Widget_shuttling = QtGui.QTableWidget()
       
       self.populate_table_shuttling()
     
       self.button_start_shuttling = QtGui.QPushButton("Start Shuttling")                    
       self.button_restore_default_settings_shuttling = QtGui.QPushButton("Default Settings")       
       self.button_abort_shuttling_sequence = QtGui.QPushButton("Abort Ramp")
  
       button_HLayout_shuttling = QtGui.QHBoxLayout()
       button_HLayout_shuttling.addWidget(self.button_restore_default_settings_shuttling)
       button_HLayout_shuttling.addStretch(1)
       button_HLayout_shuttling.addWidget(self.button_abort_shuttling_sequence)
       button_HLayout_shuttling.addWidget(self.button_start_shuttling)
       
       spinbox_HLayout_shuttling = QtGui.QHBoxLayout()
       
       self.spinbox_tau = QtGui.QDoubleSpinBox()
       self.spinbox_tau.setValue(self.tau)
       spinbox_label_tau = QtGui.QLabel('Segment Duration (s)')
       self.spinbox_tau.valueChanged.connect(self.update_tau_readSpinBox_write_TVD)
       self.spinbox_tau.setKeyboardTracking(False)
       self.spinbox_tau.setDecimals(1)
       
       self.spinbox_repetition_time_delay = QtGui.QDoubleSpinBox()
       self.spinbox_repetition_time_delay.setValue(self.repetition_time_delay)
       spinbox_label_repetition_time_delay = QtGui.QLabel('Repetition Time Delay (s)')
       self.spinbox_repetition_time_delay.valueChanged.connect(self.update_repetition_time_delay_readSpinBox_write_TVD)
       self.spinbox_repetition_time_delay.setKeyboardTracking(False)
       self.spinbox_repetition_time_delay.setDecimals(1)
       
       self.spinbox_num_shuttling_cycles = QtGui.QSpinBox()
       self.spinbox_num_shuttling_cycles.setValue(self.num_shuttling_cycles)
       spinbox_label_num_shuttling_cycles = QtGui.QLabel('Num Shuttling Cycles')
       self.spinbox_num_shuttling_cycles.valueChanged.connect(self.update_num_shuttling_cycles_readSpinBox_write_TVD)
       self.spinbox_num_shuttling_cycles.setKeyboardTracking(False)
       #self.spinbox_num_shuttling_cycles.setDecimals(1)
       
       spinbox_HLayout_shuttling.addWidget(self.spinbox_tau)
       spinbox_HLayout_shuttling.addWidget(spinbox_label_tau)
       
       spinbox_HLayout_shuttling.addWidget(self.spinbox_repetition_time_delay)
       spinbox_HLayout_shuttling.addWidget(spinbox_label_repetition_time_delay)
       
       spinbox_HLayout_shuttling.addStretch(1)
       spinbox_HLayout_shuttling.addWidget(self.spinbox_num_shuttling_cycles)
       spinbox_HLayout_shuttling.addWidget(spinbox_label_num_shuttling_cycles)
       
       tab_layout_shuttling = QtGui.QVBoxLayout()
       tab_layout_shuttling.addWidget(self.table_Widget_shuttling)
       tab_layout_shuttling.addLayout(spinbox_HLayout_shuttling)
       tab_layout_shuttling.addLayout(button_HLayout_shuttling)
       
       self.tab_shuttling.setLayout(tab_layout_shuttling)
       
       
    def populate_table_shuttling(self):        
        self.table_Widget_shuttling.setColumnCount(self.num_trap_surfs)
        self.table_Widget_shuttling.setRowCount(self.num_time_segs + 1)
                
        for i in range(self.num_trap_surfs):
            h_item = QtGui.QTableWidgetItem(self.trap_surfaces[i])
            h_item.setBackground(QtGui.QColor(self.colours[i]))
            self.table_Widget_shuttling.setHorizontalHeaderItem(i, h_item)
                        
        columnData_shuttling = [self.temp_volt_dict[self.trap_surfaces[i]]['V_ramp_list'] for i in range(self.num_trap_surfs)]  
                      
        for i in range(self.num_trap_surfs):
            for j in range(self.num_time_segs + 1):
                newItem = QtGui.QTableWidgetItem(str(columnData_shuttling[i][j]))
                self.table_Widget_shuttling.setItem(j, i, newItem)
         
        self.table_Widget_shuttling.resizeColumnsToContents()

#=================================================================================================

#                                    CREATE/POPULATE GUI TAB
#                                      FINAL TRAP VOLTAGES  

#=================================================================================================
  
    def create_tab_Vfinal(self):       
       
       self.tab_Vfinal = QtGui.QWidget()
      
       self.table_Widget_Vfinal = QtGui.QTableWidget()
       
       self.populate_table_Vfinal()
     
       self.button_set_Vfinal = QtGui.QPushButton("Set Voltages")           
       self.button_restore_default_settings_Vfinal = QtGui.QPushButton("Default Final Voltages")
      
       button_HLayout_Vfinal = QtGui.QHBoxLayout()
       button_HLayout_Vfinal.addWidget(self.button_restore_default_settings_Vfinal)
       button_HLayout_Vfinal.addStretch(1)
       button_HLayout_Vfinal.addWidget(self.button_set_Vfinal)
       
       tab_layout_Vfinal = QtGui.QVBoxLayout()
       tab_layout_Vfinal.addWidget(self.table_Widget_Vfinal)
       
       tab_layout_Vfinal.addLayout(button_HLayout_Vfinal)
       
       self.tab_Vfinal.setLayout(tab_layout_Vfinal)
      

    def populate_table_Vfinal(self):        
        self.table_Widget_Vfinal.setColumnCount(self.num_trap_surfs)
        self.table_Widget_Vfinal.setRowCount(1)
        
        for i in range(self.num_trap_surfs):
            h_item = QtGui.QTableWidgetItem(self.trap_surfaces[i])
            h_item.setBackground(QtGui.QColor(self.colours[i]))
            self.table_Widget_Vfinal.setHorizontalHeaderItem(i, h_item)
        
        columnData_Vfinal = [self.temp_volt_dict[self.trap_surfaces[i]]['V_final'] for i in range(self.num_trap_surfs)]      

        for i in range(self.num_trap_surfs):  
            newItem = QtGui.QTableWidgetItem(str(columnData_Vfinal[i]))
            self.table_Widget_Vfinal.setItem(0, i, newItem)
         
        self.table_Widget_Vfinal.resizeColumnsToContents()
        self.table_Widget_Vfinal.resizeRowsToContents()
       
#=================================================================================================

#                                    CREATE/POPULATE GUI TAB
#                              LIVE DATA ACQUISITION TRAP VOLTAGES  

#=================================================================================================

    def create_tab_monitor_trap_voltages(self):       
       
       self.tab_monitor_trap_voltages = QtGui.QWidget()

       self.table_Widget_monitor_trap_voltages = QtGui.QTableWidget()
       self.table_Widget_monitor_trap_currents = QtGui.QTableWidget()
       
       tab_layout_monitor_trap_voltages = QtGui.QVBoxLayout()
       
       button_HLayout_monitor_trap_voltages = QtGui.QHBoxLayout()       
       spinbox_HLayout_monitor_trap_voltages = QtGui.QHBoxLayout()
     
       self.button_start_monitor_trap_voltages = QtGui.QPushButton("Start Acquisition")
       
       self.button_stop_monitor_trap_voltages = QtGui.QPushButton("Stop Acquisition")
       
       button_HLayout_monitor_trap_voltages.addStretch(1)
       button_HLayout_monitor_trap_voltages.addWidget(self.button_stop_monitor_trap_voltages)
       button_HLayout_monitor_trap_voltages.addWidget(self.button_start_monitor_trap_voltages)
                                
       self.spinbox_SampleTime_monitor_trap_voltages = QtGui.QDoubleSpinBox()
       self.spinbox_SampleTime_monitor_trap_voltages.setValue(0)
       self.SampleTime_monitor_trap_voltages_label = QtGui.QLabel('Sample Time (s)')
       self.spinbox_SampleTime_monitor_trap_voltages.valueChanged.connect(self.update_SampleTime_monitor_trap_voltages_readSpinBox)
       self.spinbox_SampleTime_monitor_trap_voltages.setKeyboardTracking(False)
       self.spinbox_SampleTime_monitor_trap_voltages.setDecimals(1)
          
       spinbox_HLayout_monitor_trap_voltages.addWidget(self.spinbox_SampleTime_monitor_trap_voltages)
       spinbox_HLayout_monitor_trap_voltages.addWidget(self.SampleTime_monitor_trap_voltages_label)      
       spinbox_HLayout_monitor_trap_voltages.addStretch(1)
      
       tab_layout_monitor_trap_voltages.addWidget(self.table_Widget_monitor_trap_voltages)
       tab_layout_monitor_trap_voltages.addWidget(self.table_Widget_monitor_trap_currents)       
       
       tab_layout_monitor_trap_voltages.addLayout(spinbox_HLayout_monitor_trap_voltages)
       tab_layout_monitor_trap_voltages.addLayout(button_HLayout_monitor_trap_voltages)
           
       self.tab_monitor_trap_voltages.setLayout(tab_layout_monitor_trap_voltages)    
       

    def populate_table_monitor_trap_voltages(self, measured_voltage_list, CurrentReadback__list):        
        self.table_Widget_monitor_trap_voltages.setColumnCount(self.num_trap_surfs)
        self.table_Widget_monitor_trap_voltages.setRowCount(1)
        
        self.table_Widget_monitor_trap_currents.setColumnCount(self.num_trap_surfs)
        self.table_Widget_monitor_trap_currents.setRowCount(1)     
                                       
        ### POPULATE VOLTAGE TABLE         
        for i in range(self.num_trap_surfs):
            h_item = QtGui.QTableWidgetItem(self.trap_surfaces[i]+"   [V]")
            h_item.setBackground(QtGui.QColor(self.colours[i]))
            self.table_Widget_monitor_trap_voltages.setHorizontalHeaderItem(i, h_item)
        
        columnData_monitor_trap_voltages = measured_voltage_list
        
        for i in range(self.num_trap_surfs):  
            newItem = QtGui.QTableWidgetItem(str(columnData_monitor_trap_voltages[i]))
            self.table_Widget_monitor_trap_voltages.setItem(0, i, newItem)
            
        ### POPULATE VOLTAGE TABLE 
        for i in range(self.num_trap_surfs):
            h_item = QtGui.QTableWidgetItem(self.trap_surfaces[i]+"   [uA]")
            h_item.setBackground(QtGui.QColor(self.colours[i]))
            self.table_Widget_monitor_trap_currents.setHorizontalHeaderItem(i, h_item)   

        for i in range(self.num_trap_surfs):  
            newItem = QtGui.QTableWidgetItem(str(CurrentReadback__list[i]))
            self.table_Widget_monitor_trap_currents.setItem(0, i, newItem)

        self.table_Widget_monitor_trap_voltages.resizeColumnsToContents()
        self.table_Widget_monitor_trap_currents.resizeColumnsToContents()

     
#=================================================================================================

#                                 CONNECT GUI BUTTONS TO ACTIONS 

#=================================================================================================
        
    def connect_GUI_buttons_to_actions(self):     
        '''Connect GUI buttons to relevant action/control functions'''
        #buttons for egun1 control
        self.connect(self.button_set_setpoints_voltage_and_current_egun1, QtCore.SIGNAL("clicked()"), self.set_setpoints_voltage_and_current_egun1)
        
        self.egun1_control.MX100TP_module_egun1.MX100TP_ON.connect(self.toggle_state_ON_egun1)
        #self.thread_shuttling.started.connect(self.egun1_control.MX100TP_module_egun1.MX100TP_ON) 
        #self.connect(self.button_set_setpoints_and_deploy_outputs_voltage_and_current_egun1, QtCore.SIGNAL("clicked()"), self.toggle_state_ON_egun1)
        self.connect(self.button_set_setpoints_and_deploy_outputs_voltage_and_current_egun1, QtCore.SIGNAL("clicked()"), self.set_setpoints_and_deploy_outputs_voltage_and_current_egun1)

        self.egun1_control.MX100TP_module_egun1.MX100TP_OFF.connect(self.toggle_state_OFF_egun1)
        #self.connect(self.button_kill_output_egun1, QtCore.SIGNAL("clicked()"), self.toggle_state_OFF_egun1)
        self.connect(self.button_kill_output_egun1, QtCore.SIGNAL("clicked()"), self.kill_output_egun1)
        
              
        self.connect(self.button_update_instrument_readback_values_egun1_writeGUI, QtCore.SIGNAL("clicked()"), self.update_instrument_readback_values_egun1_writeGUI)
        self.connect(self.button_restore_default_settings_egun1, QtCore.SIGNAL("clicked()"), self.restore_default_settings_egun1)
       
        #buttons for Vinitial tab for trap surface control
        self.connect(self.button_set_Vinitial, QtCore.SIGNAL("clicked()"), self.set_Vinitial_voltages)
        self.connect(self.button_restore_default_settings_Vinitial, QtCore.SIGNAL("clicked()"), self.restore_default_settings_Vinitial)
        
        #buttons for Vfinal tab for trap surface control     
        self.connect(self.button_set_Vfinal, QtCore.SIGNAL("clicked()"), self.set_Vfinal_voltages)             
        self.connect(self.button_restore_default_settings_Vfinal, QtCore.SIGNAL("clicked()"), self.restore_default_settings_Vfinal)
        
        #buttons for shuttling tab for trap surface control
        self.connect(self.button_start_shuttling, QtCore.SIGNAL("clicked()"), self.start_shuttling_sequence)
        self.connect(self.button_restore_default_settings_shuttling, QtCore.SIGNAL("clicked()"), self.restore_default_settings_shuttling)      
        self.connect(self.button_abort_shuttling_sequence, QtCore.SIGNAL("clicked()"), self.abort_shuttling_sequence)
        
        #buttons for monitor trap voltages tab for trap surfaces 
        self.connect(self.button_start_monitor_trap_voltages, QtCore.SIGNAL("clicked()"), self.start_monitor_trap_voltages)
        self.connect(self.button_stop_monitor_trap_voltages, QtCore.SIGNAL("clicked()"), self.stop_monitor_trap_voltages)

#=================================================================================================

#                       UPDATE TEMPORARY VOLTAGE DICTIONARY (TVD) FROM GUI 

#=================================================================================================

    def update_TVD_from_GUI(self):         
        self.update_initial_voltages_readGUI_writeTVD()
        self.update_ramp_voltages_readGUI_writeTVD()
        self.update_final_voltages_readGUI_writeTVD()
        
        self.update_tau_readSpinBox_write_TVD()
        self.update_num_shuttling_cycles_readSpinBox_write_TVD()
        self.update_repetition_time_delay_readSpinBox_write_TVD()
                
    def update_initial_voltages_readGUI_writeTVD(self):  
        ''' Update the voltages in the V_ramp_list entry of the ramp voltage dictionary. Reads out the tableWidget
            and populates the temp_volt_dict'''                     
        for i in range(self.num_trap_surfs):
            self.temp_volt_dict[self.trap_surfaces[i]]['V_initial'] = float(self.table_Widget_Vinitial.item(0, i).text())          
                            
    def update_ramp_voltages_readGUI_writeTVD(self):  
        ''' Update the voltages in the V_ramp_list entry of the ramp voltage dictionary. Reads out the tableWidget
            and populates the temp_volt_dict'''                     
        for i in range(self.num_trap_surfs):
            for j in range(self.num_time_segs + 1):
                self.temp_volt_dict[self.trap_surfaces[i]]['V_ramp_list'][j] = float(self.table_Widget_shuttling.item(j, i).text())     
  
    def update_final_voltages_readGUI_writeTVD(self):  
        ''' Update the voltages in the V_final_list entry of the temp_volt_dict. Reads out the tableWidget
            and populates the temp_volt_dict'''                     
        for i in range(self.num_trap_surfs):
            self.temp_volt_dict[self.trap_surfaces[i]]['V_final'] = float(self.table_Widget_Vfinal.item(0, i).text())       
        
    def update_tau_readSpinBox_write_TVD(self):
        self.tau = self.spinbox_tau.value()
        self.temp_volt_dict['global ramping parameters']['tau'] = self.tau  

    def update_num_shuttling_cycles_readSpinBox_write_TVD(self):
        self.num_shuttling_cycles = self.spinbox_num_shuttling_cycles.value()        
        self.temp_volt_dict['global ramping parameters']['num_shuttling_cycles'] = self.num_shuttling_cycles
        
    def update_repetition_time_delay_readSpinBox_write_TVD(self):
        self.repetition_time_delay = self.spinbox_repetition_time_delay.value()
        self.temp_volt_dict['global ramping parameters']['repetition_time_delay'] = self.repetition_time_delay
                            
            
#=================================================================================================

#                                       UPDATE TVD FROM GUI 
#                       OTHER PARAMETERS FOR INSTRUMENT CONTROL/MEASUREMENT

#=================================================================================================
        
    def update_continuity_conditions(self):       
         #update default first row of ramp table to match manually updated initial voltages
        for i in range(self.num_trap_surfs):
            new_V_initial = QtGui.QTableWidgetItem(str(self.temp_volt_dict[self.trap_surfaces[i]]['V_initial']))
            self.table_Widget_shuttling.setItem(0, i, new_V_initial)            
        #update default final voltages to match final row of manually updated ramp table
        for i in range(self.num_trap_surfs):
            new_V_final = QtGui.QTableWidgetItem(str(self.temp_volt_dict[self.trap_surfaces[i]]['V_ramp_list'][-1]))
            self.table_Widget_Vfinal.setItem(0, i, new_V_final)   
            
    def update_shuttling_control_parameters_continuously(self):
        self.update_TVD_from_GUI()
        self.trap_control.temp_volt_dict = self.temp_volt_dict  
        self.trap_control.send_command_parameters_to_iseg_modules()
          
    def update_SampleTime_monitor_trap_voltages_readSpinBox(self):
        self.SampleTime_monitor_trap_voltages = self.spinbox_SampleTime_monitor_trap_voltages.value() 
        
#=================================================================================================

#                           RESTORE GUI VALUES FROM DEFAULT DICTIONARIES 

#=================================================================================================
                
    def restore_default_settings_Vinitial(self):
        print 'main window: default initial voltages restored'
        self.temp_volt_dict = deepcopy(volt_config_dict)
        self.populate_table_Vinitial()

    def restore_default_settings_shuttling(self):
        print 'main window: default shuttling voltages restored'
        self.temp_volt_dict = deepcopy(volt_config_dict)
        self.populate_table_shuttling()
        
        self.tau = self.temp_volt_dict['global ramping parameters']['tau']
        self.spinbox_tau.setValue(self.tau)

        self.num_shuttling_cycles = self.temp_volt_dict['global ramping parameters']['num_shuttling_cycles']
        self.spinbox_num_shuttling_cycles.setValue(self.num_shuttling_cycles)
        
        self.repetition_time_delay = self.temp_volt_dict['global ramping parameters']['repetition_time_delay']
        self.spinbox_repetition_time_delay.setValue(self.repetition_time_delay)        

    def restore_default_settings_Vfinal(self):
        print 'main window: default final voltages restored'
        self.temp_volt_dict = deepcopy(volt_config_dict)
        self.populate_table_Vfinal()
                   

#=================================================================================================

#                       INITIAL/FINAL VOLTAGE COMMANDS FOR TRAP SURFACES 

#=================================================================================================
        
    def set_Vinitial_voltages(self):
        print 'main window: initial voltages set'
        self.update_TVD_from_GUI()        
        self.update_continuity_conditions()
          
        self.trap_control.temp_volt_dict = self.temp_volt_dict  
        self.trap_control.read_command_parameters_from_TVD()  
        self.trap_control.set_Vinitial_voltages()  
        
    def set_Vfinal_voltages(self):
        print 'main window: final voltages set'
        self.update_TVD_from_GUI()
        self.update_continuity_conditions() 
        
        self.trap_control.temp_volt_dict = self.temp_volt_dict  
        self.trap_control.read_command_parameters_from_TVD()  
        self.trap_control.set_Vfinal_voltages()  
        
#=================================================================================================

#                                    SHUTTLING SEQUENCE COMMANDS 

#=================================================================================================

    def start_shuttling_sequence(self):
        
        self.running = True
        self.trap_control.running = self.running
        
        self.update_TVD_from_GUI()
        self.trap_control.temp_volt_dict = self.temp_volt_dict 
        
        self.update_continuity_conditions()
                                            
        self.Time__start_shuttling_sequence = time.time()
        self.trap_control.start_shuttling_sequence()  
                
        #start monitor and record using NI-DAQ unit
        self.NIDAQ_MON_and_REC__shuttling_sequence()
 
        
    def abort_shuttling_sequence(self):
        print 'main window: shuttling sequence aborted'
        self.trap_control.close_thread_shuttling()
        self.running = False  #this stops the plotting
        
#=================================================================================================

#                   INITIALIZE PLOTTING ENVIRONMENT FOR SHUTTLING SEQUENCE

#=================================================================================================
        

    def setup_plots_shuttling(self):
        
        self.trap_control.shuttling_finished.connect(self.stop_plotting)
    
        win = pg.GraphicsWindow()       
        pg_plot = win.addPlot()
        
        pg_plot.showGrid(x=True, y=True)
            
        pg_plot.setLabels(left=('voltage', 'V'))
        pg_plot.setLabels(bottom=('time', 's'))
        
        curve_names = [trap_surf_dict[self.trap_surfaces[i]]['TRAP_SURF_NAME_LONG'] \
                                    +'<br> FT PIN: {}'.format(trap_surf_dict[self.trap_surfaces[i]]['FT_PIN']) \
                                    +'<br> Inst ID: {}'.format(self.trap_control.INST_IDs_4_TRAP_SURFs[i]) \
                                    +"<br> NIDAQ: AI" + trap_surf_dict[self.trap_surfaces[i]]['NIDAQ_AI']  \
                                    for i in range(self.num_trap_surfs)] 
 
        for i in range(self.num_trap_surfs):
            pg_curve = pg_plot.plot(pen=self.colours[i], name=curve_names[i])
            
            self.pg_curves.append(pg_curve)
                
        vb = win.addViewBox()
        legend = pg.LegendItem()
        legend.setParentItem(vb)

        # Anchor the upper-left corner of the legend to the upper-left corner of its parent
        legend.anchor((0,0), (0,0))
        
        for i in range(self.num_trap_surfs):
            curve = self.pg_curves[i]
            legend.addItem(curve, curve.opts['name'])
        vb.setMaximumWidth(legend.boundingRect().width() + 10)
                
        plot_dock = QtGui.QDockWidget('Plots')
        
        plot_dock.setWidget(win)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), plot_dock)
        
        
#=================================================================================================

#                    SETUP NIDAQ MONTITOR AND RECORD FOR SHUTTLING SEQUENCE

#=================================================================================================
  
    def NIDAQ_MON_and_REC__shuttling_sequence(self):  
                                                    
        self.TimeArray__shuttling = []
        self.MeasuredSignal__arrays__shuttling = []
        self.RecordedData__shuttling = [0  for i in range(self.num_trap_surfs)]                                   
        for i in range(self.num_trap_surfs):
            self.MeasuredSignal__arrays__shuttling.append([])     
   
        while self.running:
            
            MeasuredSignal__shuttling_all_dec = [self.nidaq.measure_AI(AI=trap_surf_dict[self.trap_surfaces[i]]['NIDAQ_AI']) * \
                               trap_surf_dict[self.trap_surfaces[i]]['NIDAQ_2_HV_CONVERSION'] for i in range(self.num_trap_surfs)]

            MeasuredSignal__shuttling = [ '%.2f' % elem for elem in MeasuredSignal__shuttling_all_dec]
                               
            self.RecordedData__shuttling = np.vstack((self.RecordedData__shuttling, MeasuredSignal__shuttling))

            self.TimeArray__shuttling.append(time.time()-self.Time__start_shuttling_sequence)                
            
            for i in range(self.num_trap_surfs):
            
                pg_curve = self.pg_curves[i]

                MeasuredSignal__shuttling_array = self.MeasuredSignal__arrays__shuttling[i]                  
                MeasuredSignal__shuttling_array.append(float(MeasuredSignal__shuttling[i]))
                                    
                pg_curve.setData(self.TimeArray__shuttling, MeasuredSignal__shuttling_array)
                QtGui.QApplication.processEvents()
                

        self.RecordedData__shuttling = np.delete(self.RecordedData__shuttling,(0),axis=0)
        self.FullData__shuttling = np.hstack((np.array(self.TimeArray__shuttling).reshape(-1, 1), self.RecordedData__shuttling))        
        self.trap_control.save_to_txt(self.FullData__shuttling)         
        
    def stop_plotting(self):
        self.running = False         

    def continue_plotting(self):
        self.running = True  
                 
        
#=================================================================================================

#                                       DEFINE FUNCTIONS: 

#              *  
#              *  START LIVE DATA ACQUISITION 
#              *  SAVE CONTINUOUSLY TO TXT FILE

#=================================================================================================


    def start_monitor_trap_voltages(self):
                
        print 'main window: start monitor trap voltages'
        self.running = True
        
        self.TimeArray__monitor_trap_voltages = []
        self.MeasuredSignal__arrays__monitor_trap_voltages = []
        self.RecordedData__monitor_trap_voltages = [0  for i in range(self.num_trap_surfs)]                                          
        for i in range(self.num_trap_surfs):
            self.MeasuredSignal__arrays__monitor_trap_voltages.append([])   
        
        self.Time__start_monitor_trap_voltages = time.time()
        
        self.NIDAQ_MON_and_REC__monitor_trap_voltages()
        
    def stop_monitor_trap_voltages(self):
        self.running = False 
        print 'main window: stop monitor trap voltages'
        
    def NIDAQ_MON_and_REC__monitor_trap_voltages(self):

        self.create_txt_file_monitor_trap_voltages()
        file = open(self.DataFile_ID_monitor_trap_voltages, "a")
        file.write(self.header_str_monitor_trap_voltages)
        file.write(self.linelist_to_tab_dlt_string(self.break_str_monitor_trap_voltages)+"\n")
        file.write(self.linelist_to_tab_dlt_string(self.TRAP_SURF_NAME_str)+"\n")
        file.write(self.linelist_to_tab_dlt_string(self.INST_IDs_4_TRAP_SURFs_str)+"\n")
        file.write(self.linelist_to_tab_dlt_string(self.data_labels_str_monitor_trap_voltages)+"\n")
        file.write(self.linelist_to_tab_dlt_string(self.break_str_monitor_trap_voltages)+"\n")
        file.flush()
        
        while self.running:
                     
            self.update_SampleTime_monitor_trap_voltages_readSpinBox()
            time.sleep(self.SampleTime_monitor_trap_voltages)

            if True:
                MeasuredSignal__monitor_trap_voltages_all_dec = [self.nidaq.measure_AI(AI=trap_surf_dict[self.trap_surfaces[i]]['NIDAQ_AI']) * \
                                   trap_surf_dict[self.trap_surfaces[i]]['NIDAQ_2_HV_CONVERSION'] for i in range(self.num_trap_surfs)]
                                
                MeasuredSignal__monitor_trap_voltages = [ '%.2f' % elem for elem in MeasuredSignal__monitor_trap_voltages_all_dec]

                self.RecordedData__monitor_trap_voltages = np.vstack((self.RecordedData__monitor_trap_voltages, MeasuredSignal__monitor_trap_voltages))
                self.TimeArray__monitor_trap_voltages.append(time.time()-self.Time__start_monitor_trap_voltages) 
                
                CurrentReadback__list = self.trap_control.iseg_modules.measure_currents()
                self.populate_table_monitor_trap_voltages(MeasuredSignal__monitor_trap_voltages, CurrentReadback__list)
                
                for i in range(self.num_trap_surfs):
                
                    pg_curve = self.pg_curves[i]

                    MeasuredSignal__monitor_trap_voltages_array = self.MeasuredSignal__arrays__monitor_trap_voltages[i]                  
                    MeasuredSignal__monitor_trap_voltages_array.append(float(MeasuredSignal__monitor_trap_voltages[i]))
                    
                    
                    pg_curve.setData(self.TimeArray__monitor_trap_voltages, MeasuredSignal__monitor_trap_voltages_array)
                    QtGui.QApplication.processEvents()
                                   
                
            file.write(self.linelist_to_tab_dlt_string([self.TimeArray__monitor_trap_voltages[-1]]+MeasuredSignal__monitor_trap_voltages)+"\n")
            file.flush()
            
        self.RecordedData__monitor_trap_voltages = np.delete(self.RecordedData__monitor_trap_voltages,(0),axis=0)
        self.FullData__monitor_trap_voltages = np.hstack((np.array(self.TimeArray__monitor_trap_voltages).reshape(-1, 1), self.RecordedData__monitor_trap_voltages))
        
       
            
    def linelist_to_tab_dlt_string(self, line, spacing = 20 ):
        widths = [spacing for i in range(len(line))]
                
        proc_seqf = open('processed_seq.txt','a')
        
        pretty = ''.join('%-*s' % item for item in zip(widths, line))
        proc_seqf.write(pretty + '\n')
        return pretty
    
    
    def create_txt_file_monitor_trap_voltages(self):
        print 'main window: monitor trap voltages: txt file created'
        self.header_str_monitor_trap_voltages='\n'.join(["Log trap voltages (monitoring): iseg EHQ 102M modules", 
                              str(datetime.datetime.now().strftime("%y.%m.%d\t%H:%M:%S")) + "\t" + str(time.time()),
                              ""])
        
        self.INST_IDs_4_TRAP_SURFs = [trap_surf_dict[self.trap_surfaces[i]]['INST_ID'] for i in range(len(self.trap_surfaces))]                         
        self.INST_IDs_4_TRAP_SURFs_str = ['{}'.format(self.INST_IDs_4_TRAP_SURFs[i]) for i in range(self.num_trap_surfs)]
        self.INST_IDs_4_TRAP_SURFs_str.insert(0,"")
        
        self.TRAP_SURF_NAME_str = [trap_surf_dict[self.trap_surfaces[i]]['TRAP_SURF_NAME_SHORT'] for i in range(self.num_trap_surfs)]
        self.TRAP_SURF_NAME_str.insert(0,"") 

        self.data_labels_str_monitor_trap_voltages = ['volts [V]']*(self.num_trap_surfs)
        self.data_labels_str_monitor_trap_voltages.insert(0,"time [s]")
        
        self.break_str_monitor_trap_voltages = [""]*(self.num_trap_surfs+1)
            
        SavePath__monitor_trap_voltages = "Y:/Beryllium Lab/Projects/Project_experimental_control/Penning_system_control_program/data_log/log_trap_voltages_monitor/"
        FileName__monitor_trap_voltages = "[log_trap_voltages_monitor] {}".format(str(datetime.datetime.now().strftime("%y.%m.%d_%H.%M.%S")) )
        self.DataFile_ID_monitor_trap_voltages = os.path.join(SavePath__monitor_trap_voltages, FileName__monitor_trap_voltages+".txt")   
        


#=================================================================================================

#                                         EGUN#1 FUNCTIONS  

#=================================================================================================
       
    def update_egun1_voltage_set_values_readGUI_writeTVD(self):  
        ''' Update the value of Vset in the TVD for all surfaces of egun1'''                     
        for i in range(len(self.egun1_surfs_all)):
            if self.table_Widget_egun1.item(i, 7).text() == 'N/A':
                self.temp_volt_dict[self.egun1_surfs_all[i]]['V_set'] = 'N/A'
            else:
                self.temp_volt_dict[self.egun1_surfs_all[i]]['V_set'] = float(self.table_Widget_egun1.item(i, 7).text()) 
                print 'main window: update egun1 V_set vals'
                
    def update_egun1_current_set_values_readGUI_writeTVD(self):  
        ''' Update the value of Iset in the TVD for all egun1 emission source'''                     
        for i in range(len(self.egun1_surfs_all)):
            if self.table_Widget_egun1.item(i, 8).text() == 'N/A':
                self.temp_volt_dict[self.egun1_surfs_all[i]]['I_set'] = 'N/A'
            else:
                self.temp_volt_dict[self.egun1_surfs_all[i]]['I_set'] = float(self.table_Widget_egun1.item(i, 8).text()) 
                print 'main window: update egun1 I_set vals'

    def set_setpoints_voltage_and_current_egun1(self):  
        ''' Send (and set) voltage and current setpoint values to instrument control.'''                     
        self.update_egun1_voltage_set_values_readGUI_writeTVD()
        self.update_egun1_current_set_values_readGUI_writeTVD()
        self.egun1_control.temp_volt_dict = self.temp_volt_dict
        self.egun1_control.set_voltage_and_current_setpoints()

    def set_setpoints_and_deploy_outputs_voltage_and_current_egun1(self):  
        ''' Send voltage and current setpoints to instrument control, then deploy all outputs for egun1.'''                     
        self.set_setpoints_voltage_and_current_egun1()
        self.egun1_control.deploy_voltage_and_current_outputs()
        ###time.sleep(1)
        ###self.update_instrument_readback_values_egun1_writeGUI()                

    def kill_output_egun1(self):
        self.egun1_control.kill_output()
        ##time.sleep(1)
        ##self.update_instrument_readback_values_egun1_writeGUI()
        
    def restore_default_settings_egun1(self):   
        self.temp_volt_dict = deepcopy(volt_config_dict)
        self.egun1_control.temp_volt_dict = self.temp_volt_dict            
        self.egun1_control.execute_default_settings()
        self.populate_table_egun1()
        
    def toggle_state_ON_egun1(self):
        self.button_kill_output_egun1.setStyleSheet("background-color: None") 
        self.button_set_setpoints_and_deploy_outputs_voltage_and_current_egun1.setStyleSheet("background-color: red")
        
    def toggle_state_OFF_egun1(self):
        self.button_kill_output_egun1.setStyleSheet("background-color: red") 
        self.button_set_setpoints_and_deploy_outputs_voltage_and_current_egun1.setStyleSheet("background-color: None") 

    def update_instrument_readback_values_egun1_writeGUI(self):  
        '''Updates columns Vout and Iout on egun1 tab, by calling instrument readback, updating TVD, and re-populating GUI table'''
        nrows = len(self.egun1_surfs_all)       
        V_readback_egun1 = self.egun1_control.voltage_readback_all()  
        I_readback_egun1 = self.egun1_control.current_readback_all()  
        
        for j in range(nrows):
            newItem = QtGui.QTableWidgetItem(str(V_readback_egun1[j]))
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_Widget_egun1.setItem(j, 9, newItem) 

        for j in range(nrows):
            newItem = QtGui.QTableWidgetItem(str(I_readback_egun1[j]))
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_Widget_egun1.setItem(j, 10, newItem) 
            
if __name__ == '__main__':
    #app = 0
    app = QtGui.QApplication(sys.argv)
    app.setStyle(QtGui.QStyleFactory.create('cleanlooks')) # 'Plastique'  # won't work on windows style
    main = MainWin()
    main.setWindowTitle("Penning Trap System Control")
    main.setGeometry(400,50,1100,1000)
    main.show()
    sys.exit(app.exec_())

    
    