# -*- coding: utf-8 -*-
"""
2018-05-16: RW
    - changed measure_AI method to use NiDAQ_AnalogInput class
    
    
2018-02-23: RW
    - changed the default ramp speed of the ISEGs from 200V/s down to 10V/s, is hard coded in the following objects:
        set_initial_voltages(self, V_initial_list):  
        set_final_voltages(self, V_final_list): 

            
            
            
Created on Mon Feb 27 18:03:24 2017

@author: Harrison Ball
"""

import visa
import numpy as np
import time
import ctypes
from pyqtgraph.Qt import QtCore
from PyQt4.Qt import QMutex
#from voltage_configuration_dictionary import volt_config_dict
from nidaqmx_caller import NiDAQ_AnalogInput


#=================================================================================================

#                   DEFINE CLASS FOR COMMANDING THE ISEG HV POWER SUPPLY

#=================================================================================================

class ISEG_Command(QtCore.QObject):
    """This is a class"""
    ramp_finished = QtCore.pyqtSignal()
    update_TVD = QtCore.pyqtSignal()
    measure_currents_finished = QtCore.pyqtSignal()
    
       
    def __init__(self, ISEG_VISA_IDs):
        QtCore.QObject.__init__(self)
        self.ISEG_VISA_IDs = ISEG_VISA_IDs
        self.num_channels = len(self.ISEG_VISA_IDs)
        print self.ISEG_VISA_IDs
        
        #iseg module parameters
        self.num_time_segs = None 
        self.V_ramp_list_array = None 
        self.ramp_speed_list_array = None 
        self.tau = None 
        self.repetition_time_delay = None 
        self.V_initial_list = None 
        self.V_final_list = None
        
        self.running = True
                         
        self.connect(self.ISEG_VISA_IDs)
        
        self.mutex  = QMutex()
        
        self.micro = 10**(-6)


    def connect(self, ISEG_VISA_IDs):
        """ this is a function """
        
        self.rm = visa.ResourceManager()
        self.inst_channels = []
        for i in range(self.num_channels):
            inst = self.rm.open_resource(ISEG_VISA_IDs[i])
            inst.write('*CLS')
            inst.write('*RST')

            inst.write(":CONF:ECHO OFF")
            inst.write(":CONF:ECHO OFF")
            
            attempts = 0
            while attempts < 3:
                try:
                    print 'started session: instrument ID: iseg:', self.get_SN(inst)
                    break
                except visa.VisaIOError:
                    print 'Visa IO Error: ' + str(self.rm.last_status) + ' Attempt {}/2'.format(attempts)
                    time.sleep(0.5)
                    attempts += 1
                    continue
            self.inst_channels.append(inst)
            
            
    def query(self, inst, querystr):
        return inst.query(querystr)
        
    def measure_volts(self):

        V_measured = []
        for i in range(self.num_channels):
            v = self.query(self.inst_channels[i], ':MEAS:VOLT?')
            V_measured.append(float(v[0:len(v)-3]))
            #V_measured.append(v)
        V_measured_rounded = [ '%.2f' % elem for elem in V_measured]        
        return V_measured_rounded
        
    def measure_currents(self):

        I_measured = []
        self.mutex.lock()  
        for i in range(self.num_channels):
            current = self.query(self.inst_channels[i], ':MEAS:CURR?')
            I_num_amps = float(current[0:len(current)-3])
            I_str_uamps = str(I_num_amps/self.micro)+' uA'
            #I_measured.append(float(current[0:len(current)-3]))
            I_measured.append(I_str_uamps)
        self.mutex.unlock()  
        return I_measured
        print 'ISEG command: curents measured'
        self.measure_currents_finished.emit()
        
    def set_initial_voltages(self, V_initial_list):  
        for i in range(self.num_channels):
            self.inst_channels[i].write(":CONF:RAMP:VOLT "+str(10))
            self.inst_channels[i].write(":VOLT "+str(abs(V_initial_list[i]))) 

    def set_final_voltages(self, V_final_list):  
        for i in range(self.num_channels):
            self.inst_channels[i].write(":CONF:RAMP:VOLT "+str(10))
            self.inst_channels[i].write(":VOLT "+str(abs(V_final_list[i])))  
            
    def ramp(self, inst, ramp_speed, V_end):
        inst.write(":CONF:RAMP:VOLT "+str(ramp_speed))
        inst.write(":VOLT "+str(abs(V_end)))
        
    def get_SN(self, inst):
        SN=self.query(inst, '*IDN?')
        return SN[36:42]

    def close(self):
        for inst in self.inst_channels:
            inst.close()

    def ramp_sequence(self): 
        time.sleep(self.repetition_time_delay/2)
        tic_RS = time.time()
        for k in range(self.num_time_segs):
            if self.running:
                tic_ramp = time.time()
                self.mutex.lock()
                for i in range(self.num_channels):
                    self.ramp(self.inst_channels[i], self.ramp_speed_list_array[i,k], self.V_ramp_list_array[i,k+1])
                self.mutex.unlock()  
                time.sleep(self.tau)
                toc_ramp = abs(tic_ramp-time.time())
                print 'ISEG command: ramp time: {} seconds'.format(toc_ramp)
                self.update_TVD.emit()
        toc_RS = time.time() - tic_RS
        print 'ISEG command: ramp sequence total time: {} seconds'.format(toc_RS)

        time.sleep(self.repetition_time_delay/2)
        self.ramp_finished.emit()
        
        
    def update_ramp_params(parameter_list):
        pass

#=================================================================================================

#                   DEFINE CLASS FOR COMMANDING THE MX100TP DC POWER SUPPLY 

#=================================================================================================

class MX100TP_Command(QtCore.QObject):
    """This class contains functions relevant for remotely controlling the self.MX100TP DC power supply"""
    MX100TP_ON = QtCore.pyqtSignal()
    MX100TP_OFF = QtCore.pyqtSignal()
    
       
    def __init__(self, MX100TP_VISA_ID):
        QtCore.QObject.__init__(self)
        self.MX100TP_VISA_ID = MX100TP_VISA_ID
        self.connect(self.MX100TP_VISA_ID)
        
        #self.mutex  = QMutex()

    def connect(self, MX100TP_VISA_ID):
        """ this is a function """
        self.rm = visa.ResourceManager()
        self.MX100TP = self.rm.open_resource(MX100TP_VISA_ID)  
        #print 'connectivity check: '+get_full_ID()
                    
        attempts = 0
        while attempts < 3:
            try:
                print 'started session: instrument ID:', self.get_full_ID()[17:32]
                break
            except visa.VisaIOError:
                print 'Visa IO Error: ' + str(self.rm.last_status) + ' Attempt {}/2'.format(attempts)
                time.sleep(0.5)
                attempts += 1
                continue
        
        
    def get_full_ID(self):
        ID = self.MX100TP.query('*IDN?')
        return ID
        
    def get_SN(self):
        SN = self.MX100TP.query('*IDN?')[26:32]
        return SN
    
    def set_V_OP(self,channel,V_OP):
        self.MX100TP.write('OVP%s %s' % (channel,V_OP))
        print 'MX100TP command: over voltage protection: ch%s: %s V' % (channel,V_OP)
        
    def read_V_OP(self,channel):
        return self.MX100TP.query('V_OP%s?' % (channel))
        
    def set_I_OP(self,channel,I_OP):
        self.MX100TP.write('OCP%s %s' % (channel,I_OP))
        print 'MX100TP command: over current protection: ch%s: %s A' % (channel,I_OP)
        
    def read_I_OP(self,channel):
        return self.MX100TP.query('OCP%s?' % (channel))    
    
    def set_voltage_setpoint(self,channel,V_set):
        if V_set == 'N/A':
            print 'MX100TP command: ch%s: no voltage setpoint nominated' % (channel)
        else:                 
            self.MX100TP.write('V%s %s' % (channel,V_set))
            print 'MX100TP command: voltage setpoint: ch%s: %s V' % (channel,V_set)
        
    def read_voltage_setpoint(self,channel):
        return self.MX100TP.query('V%s?' % (channel))
        
    def set_current_setpoint(self,channel,C_set):
        if C_set == 'N/A':
            print 'MX100TP command: ch%s: no current setpoint nominated' % (channel)
        else:
            self.MX100TP.write('I%s %s' % (channel,C_set))
            print 'MX100TP command: current setpoint: ch%s: %s A' % (channel,C_set)
        
    def read_current_setpoint(self,channel):
        return self.MX100TP.query('I%s?' % (channel))    
    
    def voltage_output_readback(self,channel):
        Vout = self.MX100TP.query('V%sO?' % (channel))
        return float(Vout[0:len(Vout)-3])
        print 'MX100TP command: voltage output readback: ch%s: %s V' % (channel,Vout)
        
    def current_output_readback(self,channel):
        Cout = self.MX100TP.query('I%sO?' % (channel))
        return float(Cout[0:len(Cout)-3])
        print 'MX100TP command: current output readback: ch%s: %s A' % (channel,Cout)
    
    def set_output(self,channel,output_state):
        self.MX100TP.write('OP%s %s' % (channel,output_state))
        print 'MX100TP command: set output state: ch%s: output=%s' % (channel,output_state)
        
    def set_all_outputs(self,output_state):
        self.MX100TP.write('OPALL %s' % (output_state))
        print 'MX100TP command: set all output states: output=%s' % (output_state)
        if output_state == 1:
            self.MX100TP_ON.emit()
        elif output_state == 0:
            self.MX100TP_OFF.emit()
        
    def set_output_voltage_range(self,channel,range_config):
        self.MX100TP.write('VRANGE%s %s' % (channel,range_config))
        #print 'MX100TP command: set output voltage range: ch%s: range config=%s' % (channel,range_config)
        
    def read_output_voltage_range(self,channel):
        Vrange_dict = {}
        #CH1
        Vrange_dict[(1,1)] = '16V/6A'
        Vrange_dict[(1,2)] = '35V/3A'
        #CH2
        Vrange_dict[(2,1)] = '35V/3A'
        Vrange_dict[(2,2)] = '16V/6A'
        Vrange_dict[(2,3)] = '35V/6A'
        #CH3
        Vrange_dict[(3,1)] = '35V/3A'
        Vrange_dict[(3,2)] = '70V/1.5A'
        Vrange_dict[(3,3)] = '70V/3A'
        #<NR1>                    
        NR1=self.MX100TP.query('VRANGE%s?' % (channel))
        return Vrange_dict[(int(channel),int(NR1))]
                           
    def reset(self):
        self.MX100TP.write('*RST')
        print 'MX100TP command: reset/initialize device' 
#=================================================================================================

#                   DEFINE CLASS FOR COMMANDING THE NI USB-65259 DAQ BOARD

#=================================================================================================
    
class NI_USB_6259_Command():
    """This is a class"""   
    # This is a translation of the example program
    # C:\Program Files\National Instruments\NI-DAQ\Examples\DAQmx ANSI C\Analog In\Measure Voltage\Acq-Int Clk\Acq-IntClk.c
    
    def __init__(self):
        self.nidaq = ctypes.windll.nicaiu # load the DLL
        print 'started session: instrument ID: NI USB-6259'
    ##############################
    # Setup some typedefs and constants
    # to correspond with values in
    # C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h
    # the typedefs
#    def measure_AI(self, AI):
#      
#        int32 = ctypes.c_long
#        uInt32 = ctypes.c_ulong
#        uInt64 = ctypes.c_ulonglong
#        float64 = ctypes.c_double
#        TaskHandle = uInt32
#        # the constants
#        DAQmx_Val_Cfg_Default = int32(-1)
#        DAQmx_Val_Volts = 10348
#        DAQmx_Val_Rising = 10280
#        DAQmx_Val_FiniteSamps = 10178
#        DAQmx_Val_GroupByChannel = 0
#        ##############################
#        def CHK(self, err):
#            """a simple error checking routine"""
#            if err < 0:
#                buf_size = 100
#                buf = ctypes.create_string_buffer('\000' * buf_size)
#                self.nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
#                raise RuntimeError('nidaq call failed with error %d: %s'%(err,repr(buf.value)))
#        # set_initial_voltages variables
#        taskHandle = TaskHandle(0)
#        max_num_samples = 2
#        data = np.zeros((max_num_samples,),dtype=np.float64)
#        # now, on with the program
#    
#        CHK(self, self.nidaq.DAQmxCreateTask("",ctypes.byref(taskHandle)))
#        CHK(self, self.nidaq.DAQmxCreateAIVoltageChan(taskHandle,"Dev1/ai{}".format(AI),"",
#                                           DAQmx_Val_Cfg_Default,
#                                           float64(-10.0),float64(10.0),
#                                           DAQmx_Val_Volts,None))
#        CHK(self, self.nidaq.DAQmxCfgSampClkTiming(taskHandle,"",float64(10000.0),
#                                        DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,
#                                        uInt64(max_num_samples)));
#        CHK(self, self.nidaq.DAQmxStartTask(taskHandle))
#        read = int32()
#        CHK(self, self.nidaq.DAQmxReadAnalogF64(taskHandle,max_num_samples,float64(10.0),
#                                     DAQmx_Val_GroupByChannel,data.ctypes.data,
#                                     max_num_samples,ctypes.byref(read),None))
#        
#        if taskHandle.value != 0:
#            self.nidaq.DAQmxStopTask(taskHandle)
#            self.nidaq.DAQmxClearTask(taskHandle)
#    
#        return data[-1] # element -1 refers to the last element in the list, -2 would be the second last
   
    
    def measure_AI(self, AI):
        ''' new method for measure_AI which uses NiDAQ_AnalogInput class from Virginia'''
        self.Ainput = NiDAQ_AnalogInput(["Dev1/ai{}".format(AI)])
        self.Ainput.configure()
        self.AIread = self.Ainput.read(val=1,name="Dev1/ai{}".format(AI))
        #print(self.AIread)
        return self.AIread  