# coding= latin-1
"""
Created on Wed Jan  10 16:16:04 2018
@author: qcl
DAQmxCreateCICountEdgesChan    (TaskHandle taskHandle, const char counter[], 
                                const char nameToAssignToChannel[], int32 edge, 
                                uInt32 initialCount, int32 countDirection);
    Creates a channel to count the number of rising or falling edges of a digital 
    signal and adds the channel to the task you specify with taskHandle. With the 
    exception of devices that support multi-counter tasks, you can create only one
    counter input channel at a time with this function because a task can contain 
    only one counter input channel. To read from multiple counters simultaneously, 
    use a separate task for each counter. Connect the input signal to the default 
    input terminal of the counter unless you select a different input terminal.
    Parameters
    ---------------
    Input (Name  -	Type  -  Description)
        
        taskHandle 	TaskHandle 	                The task to which to add the channels that 
                                                this function creates.
        counter 	const char [] 	            The name of the counter to use to create 
                                                virtual channels.
        nameToAssignToChannel 	const char [] 	The name(s) to assign to the created virtual  
                                                channel(s). If you do not specify a name, 
                                                NI-DAQmx uses the physical channel name as the 
                                                virtual channel name. If you specify your own 
                                                names for nameToAssignToChannel, you must use the 
                                                names when you refer to these channels in other 
                                                NI-DAQmx functions.
    If you create multiple virtual channels with one call to this function, you can specify a list 
    of names separated by commas. If you provide fewer names than the number of virtual channels you 
    create, NI-DAQmx automatically assigns names to the virtual channels.
        edge 	int32 	                        Specifies on which edges of the input signal to 
                                                increment or decrement the count.
                    Value: 		            Description
                        DAQmx_Val_Rising 		Rising edge(s).
                        DAQmx_Val_Falling 		Falling edge(s).
        initialCount 	uInt32 	                The value from which to start counting.
        countDirection 	int32 	                Specifies whether to increment or decrement the counter on each edge.
                    Value: 		            Description
                        DAQmx_Val_CountUp 		Increment the count register on each edge.
                        DAQmx_Val_CountDown 	Decrement the count register on each edge.
                        DAQmx_Val_ExtControlled The state of a digital line controls the count direction. 
                                                Each counter has a default count direction terminal.
    Return Value
        Name 	Type 	Description
        status 	int32 	The error code returned by the function in the event of an error or warning. A value 
                        of 0 indicates success. A positive value indicates a warning. A negative value 
                        indicates an error.
DAQmxCfgDigEdgeStartTrig (TaskHandle taskHandle, const char triggerSource[], int32 triggerEdge);
    Configures the task to start acquiring or generating samples on a rising or falling edge of a digital 
    signal.
    Parameters
    --------------
    Input (Name  -	Type  -  Description)
    
        taskHandle 	TaskHandle 	        The task used in this function.
        triggerSource 	const char [] 	The name of a terminal where there is a digital signal to use as the 
                                        source of the trigger.
        triggerEdge 	int32 	        Specifies on which edge of a digital signal to start acquiring or 
                                        generating samples.
                    Value:      		Description
                    DAQmx_Val_Rising 		Rising edge(s).
                    DAQmx_Val_Falling 		Falling edge(s).
    Return Value
        Name 	Type 	Description
        status 	int32 	The error code returned by the function in the event of an error or warning. A value 
                    of 0 indicates success. A positive value indicates a warning. A negative value indicates
                    an error.
DAQmxReadCounterU32 (TaskHandle taskHandle, int32 numSampsPerChan, float64 timeout, uInt32 readArray[], 
                    uInt32 arraySizeInSamps, int32 *sampsPerChanRead, bool32 *reserved);
    Reads multiple 32-bit integer samples from a counter task. Use this function when counter samples are 
    interleaved, and are returned unscaled, such as for edge counting.
    Parameters
    --------------
    Input (Name  -	Type  -  Description)
        taskHandle 	TaskHandle  The task to read samples from.
        numSampsPerChan int32 	The number of samples, per channel, to read. The default value of -1 
                                (DAQmx_Val_Auto) reads all available samples. If readArray does not contain 
                                enough space, this function returns as many samples as fit in readArray.
        NI-DAQmx determines how many samples to read based on whether the task acquires samples continuously or 
        acquires a finite number of samples.
        If the task acquires samples continuously and you set this parameter to -1, this function reads all the 
        samples currently available in the buffer.
        If the task acquires a finite number of samples and you set this parameter to -1, the function waits for 
        the task to acquire all requested samples, then reads those samples. If you set the Read All Available 
        Samples property to TRUE, the function reads the samples currently available in the buffer and does not 
        wait for the task to acquire all requested samples.
        timeout 	float64 	The amount of time, in seconds, to wait for the function to read the sample(s). 
                                To specify an infinite wait, pass -1 (DAQmx_Val_WaitInfinitely). This function 
                                returns an error if the timeout elapses.
        A value of 0 indicates to try once to read the requested samples. If all the requested samples are read, 
        the function is successful. Otherwise, the function returns a timeout error and returns the samples that 
        were actually read.
        arraySizeInSamps    uInt32 	The size of the array, in samples, into which samples are read.
        reserved 	bool32 *    	Reserved for future use. Pass NULL to this parameter.
    Output
        
        readArray 	uInt32 [] 	        The array to read samples into.
        sampsPerChanRead 	int32 * 	The actual number of samples read from each channel.
        Return Value
        Name 	Type 	Description
        status 	int32 	The error code returned by the function in the event of an error or warning. A value of 0 
                        indicates success. A positive value indicates a warning. A negative value indicates an 
                        error.
TODO: test counting with single and multiple triggers
        - can we recycle task handles?
        - work out whether we need to configure the trigger everytime we restart the task
        - when do we need to stop the task? after reading?
        - do we need to clear the counter after each set of reps? (Igor is resetting)
        - which trigger function do we need:
            could be this one:
                DAQmxCfgDigEdgeStartTrig
            or this one:
                DAQmxCfgDigEdgeAdvTrig
            or:
                DAQmxCfgSampClkTiming
"""

import numpy as np

from PyDAQmx.DAQmxFunctions import DAQmxCreateTask, DAQmxCreateAOVoltageChan, \
                DAQmxResetDevice, DAQmxStartTask, DAQmxWriteAnalogF64, DAQmxStopTask, \
                DAQmxCreateCICountEdgesChan, DAQmxReadCounterU32, DAQmxCfgDigEdgeStartTrig, \
                DAQmxSetCICountEdgesTerm, DAQmxCfgAnlgEdgeStartTrig, DAQmxCfgDigEdgeAdvTrig, \
                DAQmxCfgSampClkTiming, DAQmxClearTask, DAQmxCreateAIVoltageChan, DAQmxReadAnalogF64
from PyDAQmx.DAQmxConstants import DAQmx_Val_Volts, DAQmx_Val_GroupByChannel, \
                DAQmx_Val_Rising, DAQmx_Val_Falling, DAQmx_Val_CountUp, DAQmx_Val_RisingSlope, \
                DAQmx_Val_ContSamps, DAQmx_Val_FiniteSamps,  DAQmx_Val_HWTimedSinglePoint, DAQmx_Val_RSE
from PyDAQmx import TaskHandle, int32
from ctypes import byref
import traceback
import sys

class NiDAQ_Controller(object):
    '''
        Base class for handling communication with the NiDAQmx board. This class creates
        task handles for given physical channels and stores a dictionary of those handles
        for each channel. It also implements two simple methods to stop a single or all 
        tasks from that dictionary. Functions for starting tasks are defined in respective
        child classes, as they strongly depend on the type of task.
        This class serves as base class only and should not be used directly. To set
        up a certain type of task, write a sub-class which inherits from this one. See
        below for examples of classes for analog output and digital counting.
    '''
    def __init__(self, physical_channel, reset=False):
        
        if not isinstance(physical_channel, list):
            self.physical_channel = [physical_channel]
        else:
            self.physical_channel = physical_channel

        self.num_channels = len(self.physical_channel)
        
        if reset:
            DAQmxResetDevice(physical_channel[0].split('/')[1] )
            
    def create_tasks(self):
        ''' Create TaskHandles for each channel '''
        task_handles = dict([(name, TaskHandle(0)) for name in self.physical_channel])

        for name in self.physical_channel:
            DAQmxCreateTask('', byref(task_handles[name]))

        self.task_handles = task_handles  
      
    def stop_task(self, name):
        if name is None:
            name = self.physical_channel[0]
        task_handle = self.task_handles[name]                    
        return DAQmxStopTask(task_handle)
        
    def stop_all(self):
        for name in self.physical_channel:
            task_handle = self.task_handles[name]                    
            DAQmxStopTask(task_handle)
        return 0

    def clear_all(self):
        ''' Clear all task objects to let go of resources '''
        for name in self.physical_channel:
            task_handle = self.task_handles[name]                    
            DAQmxClearTask(task_handle)
            del self.task_handles[name]
        return 0



class NiDAQ_AnalogOutput(NiDAQ_Controller):
    '''Class to create a multi-channel analog output 
    Taken from the PyDAQmx MultiChannelAnalogInput example and modified to output.
    
    Usage: AO = NiDAQ_AnalogOutput(physicalChannel)
        physicalChannel: a string or a list of strings
    optional parameter: limit: tuple or list of tuples, the AO limit values
                        reset: Boolean
    Methods:
        write(val, name): write a voltage value to the specified channel
        TODO: implement limits (if you think it's important)
    '''
    def __init__(self, physical_channel, limit=None, reset=False):
        super(NiDAQ_AnalogOutput, self).__init__(physical_channel, reset)
        self.has_task_handles = False
            
    def configure(self):
        ''' Configure analog output voltage tasks and corresponding task handles.
            The super method create_tasks() creates the task handles and writes them
            into the task_handles dictionary.
         '''
        if not self.has_task_handles: # In case you want to call configure again but
            self.create_tasks()       # not create new task handles

        for name in self.physical_channel:
            DAQmxCreateAOVoltageChan(self.task_handles[name], name, '',
                                     -10.0, 10.0, # analog output voltage limits
                                     DAQmx_Val_Volts, None)
     
    def start_task(self, val=1, name=None):
      ''' Start the task (without writing)'''
      if name is None:
        name = self.physical_channel[0]
        task_handle = self.task_handles[name]                    
        DAQmxStartTask(task_handle)
      
        #data = np.zeros((1,), dtype=np.float64)
        #data[0] = val
        #DAQmxWriteAnalogF64(task_handle, 1, 1, 5, DAQmx_Val_GroupByChannel, data, None, None)
      
    def write(self, val, name=None):
        ''' Start an analog write task for a previously configured physical channel. '''
        if name is None:
            name = self.physical_channel[0]
        task_handle = self.task_handles[name]                    
        #DAQmxStartTask(task_handle)
        
        data = np.zeros((1,), dtype=np.float64)
        data[0] = val
        DAQmxWriteAnalogF64(task_handle, 1, 1, 5, DAQmx_Val_GroupByChannel, data, None, None)



class NiDAQ_AnalogInput(NiDAQ_Controller):
    '''Class to create a multi-channel analog input 
    Taken from the PyDAQmx MultiChannelAnalogInput example.
    
    Usage: AI = NiDAQ_AnalogOutput(physicalChannel)
        physicalChannel: a string or a list of strings
    optional parameter: limit: tuple or list of tuples, the AO limit values
                        reset: Boolean
    Methods:
        read(name): read a voltage value from the specified channel
        TODO: implement limits (if you think it's important)
    '''
    def __init__(self, physical_channel, limit=None, reset=False):
        super(NiDAQ_AnalogInput, self).__init__(physical_channel, reset)
        self.has_task_handles = False
            
    def configure(self):
        ''' Configure analog output voltage tasks and corresponding task handles.
            The super method create_tasks() creates the task handles and writes them
            into the task_handles dictionary.
         '''
        if not self.has_task_handles: # In case you want to call configure again but
            self.create_tasks()       # not create new task handles

        for name in self.physical_channel:
            DAQmxCreateAIVoltageChan(self.task_handles[name], name, '', DAQmx_Val_RSE,
                                     -10.0, 10.0, # analog output voltage limits
                                     DAQmx_Val_Volts, None)
     
    def start_task(self, val=1, name=None):
      ''' Start the task (without writing)'''
      if name is None:
        name = self.physical_channel[0]
        task_handle = self.task_handles[name]                    
        DAQmxStartTask(task_handle)
      
        #data = np.zeros((1,), dtype=np.float64)
        #data[0] = val
        #DAQmxWriteAnalogF64(task_handle, 1, 1, 5, DAQmx_Val_GroupByChannel, data, None, None)
      
    def read(self, val, name=None):
        ''' Start an analog read task for a previously configured physical channel. '''
        if name is None:
            name = self.physical_channel[0]
        task_handle = self.task_handles[name]                    
        #DAQmxStartTask(task_handle)
        
        data = np.zeros((1,), dtype=np.float64)
        read = int32()
        DAQmxReadAnalogF64(task_handle, 1, 10.0, DAQmx_Val_GroupByChannel, data, 1, byref(read), None)
        return data[0]


class NiDAQ_DigitalCounter(NiDAQ_Controller):
    '''
        Class for handling communication with the NiDAQmx board for
        digital counters with analog triggers
    '''
    def __init__(self, physical_channel=['/Dev2/pfi0', '/Dev2/pfi4'], reset=False):
        # physical_channel=['Dev2/pfi0', 'Dev2/pfi4']
        super(NiDAQ_DigitalCounter, self).__init__(physical_channel, reset)
        
            
    def configure(self, trigger_sources=['/Dev2/pfi1', '/Dev2/pfi5'], 
                  num_samples_1=10, num_samples_2=10):
        ''' Create TaskHandles for each channel using the super method create_tasks and
            set up digital count egdes tasks for each physical channel. Can add trigger sources
            to set up a triggered counter.
        '''
        # trigger_sources=['Dev2/pfi1', 'Dev2/pfi5']
        
        try:
            if len(self.task_handles) != 0:
                print('Clear existing tasks')
                self.clear_all()
        except AttributeError:
            print('No tasks found')
        
        self.create_tasks() 

        if trigger_sources is None:
            trigger_sources = [None for ch in self.physical_channel]
        else:
            assert len(self.task_handles) == len(trigger_sources)

        counter = iter(['Dev2/ctr0', 'Dev2/ctr1'])
        samples = iter([num_samples_1, num_samples_2])
        # Create Count Edges task
        for name, trig_source in zip(self.physical_channel, trigger_sources):
            ctr = next(counter)
            DAQmxCreateCICountEdgesChan(self.task_handles[name], ctr, 'counter task',
                                     DAQmx_Val_Rising, 0, DAQmx_Val_CountUp)
            DAQmxSetCICountEdgesTerm(self.task_handles[name], ctr, name)
            if trig_source is not None:
                DAQmxCfgSampClkTiming(self.task_handles[name], trig_source, 1000,
                            DAQmx_Val_Rising,   DAQmx_Val_FiniteSamps,
                            next(samples))

      
    def start_counter(self, name):
        ''' Start the counter task for a given channel, e.g. Dev2/pfi0 '''
        if name is None:
            name = self.physical_channel[0]
        task_handle = self.task_handles[name]                    
        return DAQmxStartTask(task_handle)
    
    def start_all(self):
        ''' Starts all tasks in the physical channels dict '''
        for name in self.physical_channel:
            task_handle = self.task_handles[name]                    
            DAQmxStartTask(task_handle)
        return 0

    def read_counter(self, name, num_samples=1, timeout_sec=1800):
        ''' Read out the digital counters. 
            A timeout of -1 means infinite wait
        '''
        
        if name is None:
            name = self.physical_channel[0]
        task_handle = self.task_handles[name]

        data = np.zeros((num_samples,), dtype=np.uint32)
        read_samples = int32()
        try:
            DAQmxReadCounterU32(task_handle, num_samples, timeout_sec, data, 
                        num_samples, byref(read_samples), None)
        except:
            print('Num samples expected: {}, actual: {}'.format(num_samples, read_samples.value))
            sys.stderr(traceback.format_exc())
        

        return data
    
    def read_all(self, num_samples_1, num_samples_2):
        ''' Read all counters from the physical channels dict '''
        data = []
        for name, s in zip(self.physical_channel, [num_samples_1, num_samples_2]):
            data.append(self.read_counter(name, num_samples=s))
        
        return data
            
        
    
if __name__ == '__main__':

    # Test the analog output
    import time
    AO = NiDAQ_AnalogOutput(["Dev2/ao0", "Dev2/ao1"])
    AO.configure()
    AO.start_task(name="Dev2/ao0")
    AO.write(val=2.0, name="Dev2/ao0")
    time.sleep(2)
    AO.write(val=1.0, name="Dev2/ao0")
    
#AO.write(val=-2.0, name="Dev2/ao1")