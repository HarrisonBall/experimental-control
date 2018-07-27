# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 09:26:21 2017

@author: Harrison Ball
"""
import numpy as np

#=================================================================================================

#     ------------------------              TRAP SURFACE             ------------------------
#     ------------------------  VOLTAGE CONFIGURATIONS DICTIONARIES  ------------------------

#   sets default voltages for all active trap sufraces (i.e. all trap sufraces controlled by 
#   active power supplies, not just fixed at GND). This includes initial voltages for loading, 
#   voltage lists for time-dependent shuttling procedure, and final voltages for trapping in 
#   science trap. 

#=================================================================================================

#=================================================================================================

#       --------------------------  SET GLOBAL RAMPING PARAMETERS  ------------------------

#=================================================================================================

global_ramping_parameters = {}
global_ramping_parameters['tau'] = 0.8
global_ramping_parameters['num_time_segs'] = 44
global_ramping_parameters['num_shuttling_cycles'] = 1
global_ramping_parameters['repetition_time_delay'] = 4

#=================================================================================================

#      --------------------------  DEFINE DATA MANAGEMENT FUNCTIONS   ------------------------

#=================================================================================================

def ramp_speeds(tau, V_ramp_list):
    #print 'tau @ ramp_speeds dict: '+str(tau)
    return [float(abs((abs(V_ramp_list[k+1])-abs(V_ramp_list[k]))/tau)) for k in range(len(V_ramp_list)-1)]
            
def round_list(list_in, decimal_points):
    myFormattedList = [round(elem,decimal_points) for elem in list_in ]
    return myFormattedList            
                           
#=================================================================================================

#            DEFINE VOLTAGE LISTS SAMPLED FROM R. WOLF SIMULATED SHUTTLING POTENTIALS    

#=================================================================================================


Vlist_LTring = [-91.25200000000001, -81.58800000000001, -76.232, -73.204, -71.509, -70.611, -70.077, -69.044, -62.056000000000004, -5.006, -0.0, -0.001, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0]
#Vlist_LTEC2 = [-0.0, -45.071000000000005, -60.327, -65.40899999999999, -67.002, -67.444, -67.557, -67.62, -67.757, -68.15, -67.773, -67.626, -67.575, -67.558, -67.551, -67.547, -67.53699999999999, -67.465, -66.87100000000001, -61.973, -21.919, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0]
Vlist_LTEC2 = [-0.0, -32, -52, -62, -67.002, -67.444, -67.557, -67.62, -67.757, -68.15, -67.773, -67.626, -67.575, -67.558, -67.551, -67.547, -67.53699999999999, -67.465, -66.87100000000001, -61.973, -21.919, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0]
Vlist_STRW = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.001, -0.0, -0.0, -0.0, -0.0, -0.045, -0.024, -133.4, -167.03099999999998, -172.225, -174.82299999999998, -178.84099999999998, -185.625, -196.046, -211.299, -233.143, -264.438, -309.254, -373.48900000000003, -447.153, -358.509, -301.225, -263.695, -238.795, -222.513, -212.291, -206.75799999999998, -100, -50, -25, -5.73]
Vlist_STEC1 = [-0.0, -0.0, -0.0, -0.0, -0.0, 0.0, -0.0, 0.0, -0.0, -5.0, -58.738, -66.47399999999999, -67.411, -67.528, -67.543, -67.546, -67.548, -67.553, -67.567, -67.60600000000001, -67.718, -67.64399999999999, -67.581, -67.55199999999999, -67.51, -67.383, -67.042, -66.268, -64.691, -61.665, -56.035, -45.828, -27.773000000000003, -0.0, -0.0, -0.013999999999999999, 0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0]
Vlist_STring = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.004, -0.0, -0.0, -0.0, -0.0, 0.0, -0.0, -0.0, 0.0, -0.0, -0.0, -0.0, -3.0, -30.765, -45.934, -54.295, -58.95399999999999, -61.54600000000001, -62.963, -63.656000000000006, -63.656000000000006, -63.656000000000006, -63.656000000000006, -63.656000000000006]
Vlist_STEC2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0]


zero_offset = -1
num_dec_pl = 1

                   
Vlist_LTring = round_list(Vlist_LTring,num_dec_pl)
Vlist_LTEC2 = round_list(Vlist_LTEC2,num_dec_pl)
Vlist_STRW = round_list(Vlist_STRW,num_dec_pl)
Vlist_STEC1 = round_list(Vlist_STEC1,num_dec_pl)
Vlist_STring = round_list(Vlist_STring,num_dec_pl)
Vlist_STEC2 = round_list(Vlist_STEC2,num_dec_pl)

#=================================================================================================

#      --------   DEFINE VOLTAGE CONFIGURATION DICTIONARIES FOR TRAP ELECTRODES    --------

#=================================================================================================

# ________________________________________________________________________________________________

# -------------------#                    LOADING TRAP (FT#2)                 # ------------------
# ________________________________________________________________________________________________

#____________________ 'Loading Trap: end-cap #1' _____________________

#Loading_EndCap1 = {}
#Loading_EndCap1['V_ramp_list'] = [0, 0/2, 0/2, 0, 0]
#Loading_EndCap1['tau_list'] = [10, 20, 20, 20, 10]

#____________________ 'Loading Trap: centre ring' _____________________

Loading_CentreRing = {}

Loading_CentreRing['V_ramp_list'] = np.array(Vlist_LTring)+zero_offset
#Loading_CentreRing['tau_list'] = [global_ramping_parameters['tau']]*global_ramping_parameters['num_time_segs']
Loading_CentreRing['ramp_speeds'] = ramp_speeds(global_ramping_parameters['tau'],Loading_CentreRing['V_ramp_list'])
Loading_CentreRing['V_initial'] = Loading_CentreRing['V_ramp_list'][0]
Loading_CentreRing['V_final'] = Loading_CentreRing['V_ramp_list'][-1]

#____________________ 'Loading Trap: end-cap #2' _____________________

Loading_EndCap2 = {}
Loading_EndCap2['V_ramp_list'] = np.array(Vlist_LTEC2)+zero_offset
#Loading_EndCap2['tau_list'] = [2]*13
Loading_EndCap2['ramp_speeds'] = ramp_speeds(global_ramping_parameters['tau'],Loading_EndCap2['V_ramp_list'])
Loading_EndCap2['V_initial'] = Loading_EndCap2['V_ramp_list'][0]
Loading_EndCap2['V_final'] = Loading_EndCap2['V_ramp_list'][-1]
#
#
#
# ________________________________________________________________________________________________

# -------------------#                    ROTATING WALL (FT#3)                 # ------------------
# ________________________________________________________________________________________________
#
#
#____________________ 'Rotating Wall: Quadruplet #1' _____________________

RW1 = {}

RW1['V_ramp_list'] = np.array(Vlist_STRW)+zero_offset
#RW1['tau_list'] = [2]*13
RW1['ramp_speeds'] = ramp_speeds(global_ramping_parameters['tau'],RW1['V_ramp_list'])
RW1['V_initial'] = RW1['V_ramp_list'][0]
RW1['V_final'] = RW1['V_ramp_list'][-1]
#[5]*10
#
#
#
# ________________________________________________________________________________________________

# -------------------#                    SCIENCE TRAP (FT#4)                 # ------------------
# ________________________________________________________________________________________________
#
#
#____________________ 'Science Trap: end-cap #1' _____________________

Science_EndCap1 = {}

Science_EndCap1['V_ramp_list'] = np.array(Vlist_STEC1)+zero_offset
#Science_EndCap1['tau_list'] = [2]*13
Science_EndCap1['ramp_speeds'] = ramp_speeds(global_ramping_parameters['tau'],Science_EndCap1['V_ramp_list'])
Science_EndCap1['V_initial'] = Science_EndCap1['V_ramp_list'][0]
Science_EndCap1['V_final'] = Science_EndCap1['V_ramp_list'][-1]
#[5]*5

#____________________ 'Science Trap: centre ring' _____________________

Science_CentreRing = {}

Science_CentreRing['V_ramp_list'] = np.array(Vlist_STring)+zero_offset
#Science_CentreRing['tau_list'] = [2]*13
Science_CentreRing['ramp_speeds'] = ramp_speeds(global_ramping_parameters['tau'],Science_CentreRing['V_ramp_list'])
Science_CentreRing['V_initial'] = Science_CentreRing['V_ramp_list'][0]
Science_CentreRing['V_final'] = Science_CentreRing['V_ramp_list'][-1]
#[5]*10

#____________________ 'Science Trap: end-cap #2' _____________________

Science_EndCap2 = {}

Science_EndCap2['V_ramp_list'] = np.array(Vlist_STEC2)+zero_offset
#Science_EndCap2['tau_list'] = [2]*13
Science_EndCap2['ramp_speeds'] = ramp_speeds(global_ramping_parameters['tau'],Science_EndCap2['V_ramp_list'])
Science_EndCap2['V_initial'] = Science_EndCap2['V_ramp_list'][0]
Science_EndCap2['V_final'] = Science_EndCap2['V_ramp_list'][-1]
#[2,6,10,6,5]

#=================================================================================================

#     --------------------                  ELECTRON GUNS               ----------------------
#     --------------------      VOLTAGE CONFIGURATIONS DICTIONARIES     ----------------------

#                        sets default voltages for all electron gun components 

#=================================================================================================

# ________________________________________________________________________________________________

# ----------------------#               ELECTRON GUN #1              # ------------------------
# ________________________________________________________________________________________________

# ----------------------# ----------------------# ----------------------# ------------------------
# ----------------------#                     FT #1                     # ------------------------
# ----------------------# ----------------------# ----------------------# ------------------------
#
#____________________ 'Electron Gun #1: emission-bias' _____________________

egun1_emission_bias = {}
egun1_emission_bias['V_OP'] = 'N/A'
egun1_emission_bias['I_OP'] = 'N/A'
egun1_emission_bias['V_set'] = -0.1
egun1_emission_bias['I_set'] = 'N/A'

#____________________ 'Electron Gun #1: emission-source' _____________________

egun1_emission_source = {}
egun1_emission_source['V_OP'] = 16
egun1_emission_source['I_OP'] = 2.9
egun1_emission_source['V_set'] = 0.0
egun1_emission_source['I_set'] = 0.0


#____________________ 'Electron Gun #1: cathode plate' _____________________

egun1_cathode = {}
egun1_cathode['V_OP'] = 70
egun1_cathode['I_OP'] = 0.1
egun1_cathode['V_set'] = 69
egun1_cathode['I_set'] = 'N/A'

#____________________ 'Electron Gun #1: annode plate' _____________________

egun1_anode = {}
egun1_anode['V_OP'] = 35
egun1_anode['I_OP'] = 0.1
egun1_anode['V_set'] = 25
egun1_anode['I_set'] = 'N/A'

# ----------------------# ----------------------# ----------------------# ------------------------
# ----------------------#               FT #2   (ExB plates)            # ------------------------
# ----------------------# ----------------------# ----------------------# ------------------------

#____________________ 'Electron Gun #1: ExB plate (LHS)' _____________________

egun1ExB_LHS = {}
egun1ExB_LHS['V_OP'] = 'N/A'
egun1ExB_LHS['I_OP'] = 'N/A'
egun1ExB_LHS['V_set'] = -150
egun1ExB_LHS['I_set'] = 'N/A'

#____________________ 'Electron Gun #1: ExB plate (RHS)' _____________________

egun1ExB_RHS = {}
egun1ExB_RHS['V_OP'] = 'N/A'
egun1ExB_RHS['I_OP'] = 'N/A'
egun1ExB_RHS['V_set'] = 150
egun1ExB_RHS['I_set'] = 'N/A'

# ________________________________________________________________________________________________

# ----------------------#                ELECTRON GUN #2               # ------------------------
# ________________________________________________________________________________________________

# ----------------------# ----------------------# ----------------------# ------------------------
# ----------------------#                     FT #1                     # ------------------------
# ----------------------# ----------------------# ----------------------# ------------------------

#____________________ 'Electron Gun #2: emission-bias' _____________________

egun2_emission_bias = {}
egun2_emission_bias['V_OP'] = 5
egun2_emission_bias['I_OP'] = 5
egun2_emission_bias['V_set'] = 3

#____________________ 'Electron Gun #2: cathode plate' _____________________

egun2_cathode = {}
egun2_cathode['V_OP'] = 5
egun2_cathode['I_OP'] = 5
egun2_cathode['V_set'] = 3

#____________________ 'Electron Gun #2: annode plate' _____________________

egun2_anode = {}
egun2_anode['V_OP'] = 5
egun2_anode['I_OP'] = 5
egun2_anode['V_set'] = 3

# ----------------------# ----------------------# ----------------------# ------------------------
# ----------------------#               FT #2   (ExB plates)            # ------------------------
# ----------------------# ----------------------# ----------------------# ------------------------

#____________________ 'Electron Gun #2: ExB plate (LHS)' _____________________

egun2ExB_LHS = {}
egun2ExB_LHS['V_OP'] = 'N/A'
egun2ExB_LHS['V_set'] = -100

#____________________ 'Electron Gun #2: ExB plate (RHS)' _____________________

egun2ExB_RHS = {}
egun2ExB_RHS['V_OP'] = 'N/A'
egun2ExB_RHS['V_set'] = 100


#=================================================================================================

#  ------------------     TOP-LEVEL DICTIONARY FOR CALLING SUB-DICTIONARIES   -------------------

#=================================================================================================


volt_config_dict = {}

# ________________________________________________________________________________________________

# ----------------------#                 TRAP SUFRACES                 # ------------------------
# ________________________________________________________________________________________________

volt_config_dict['global ramping parameters']= global_ramping_parameters

#volt_config_dict['Loading Trap: end-cap #1']= Loading_EndCap1
volt_config_dict['Loading Trap: centre ring']= Loading_CentreRing
volt_config_dict['Loading Trap: end-cap #2']= Loading_EndCap2

volt_config_dict['Rotating Wall: Quadruplet #1']= RW1
#volt_config_dict['Rotating Wall: Quadruplet #2']= RW2
#volt_config_dict['Rotating Wall: Quadruplet #3']= RW3
#volt_config_dict['Rotating Wall: Quadruplet #4']= RW4

volt_config_dict['Science Trap: end-cap #1']= Science_EndCap1
volt_config_dict['Science Trap: centre ring']= Science_CentreRing
volt_config_dict['Science Trap: end-cap #2']= Science_EndCap2

#volt_config_dict['Wire Mesh']= WireMesh

# ________________________________________________________________________________________________

# ----------------------#                 ELECTRON GUNS                 # ------------------------
# ________________________________________________________________________________________________
       
volt_config_dict['Electron Gun #1: cathode plate']= egun1_cathode           
volt_config_dict['Electron Gun #1: anode plate']= egun1_anode           

volt_config_dict['Electron Gun #1: emission-source']= egun1_emission_source    
volt_config_dict['Electron Gun #1: emission-bias']= egun1_emission_bias

volt_config_dict['Electron Gun #1: ExB plate (LHS)']= egun1ExB_LHS            
volt_config_dict['Electron Gun #1: ExB plate (RHS)']= egun1ExB_RHS

volt_config_dict['Electron Gun #2: emission-bias']= egun2_emission_bias           
volt_config_dict['Electron Gun #2: cathode plate']= egun2_cathode           
volt_config_dict['Electron Gun #2: anode plate']= egun2_anode           
volt_config_dict['Electron Gun #2: ExB plate (LHS)']= egun2ExB_LHS            
volt_config_dict['Electron Gun #2: ExB plate (RHS)']= egun2ExB_RHS
              

                  

