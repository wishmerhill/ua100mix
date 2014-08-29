# ********************************
# ***** DEBUG MODE CONTROL *******
# SET:
#      1: debug messages on stdout ON
#      0: debug messages on stdout OFF

DEBUG_MODE = 1

# ********************************
# ***** UA MODE CONTROL **********
#
# SET:
#      0: No UA-100 present, for test purposes on other machines
#      1: UA-100 present and working
# NOTE: Could (and will) be automatically set to 0 if no UA-100 is found.
#       The UA-100 discovery routine is based on ALSA - **** 
#       ******* TO DO *******
#       Let the discovery be usb id based.

REAL_UA_MODE = 1

# ********************************


import sys
import os
import functools
try:
    import pyportmidi as pm
except ImportError:
    print('*** Warning *** pyPortmidi not found - Swithing to testing mode (REAL_UA_MODE = 0) ***')
    REAL_UA_MODE = 0
from PyQt4 import QtGui, QtCore
from global_constants import *
from main_ui import *
from main_ui_setup import *
from device_sel_ui import *
from types import MethodType
import signal
import time

# Defining costants (taken from UA-100 documentation)
# and copying some useful documentation excerts

if (DEBUG_MODE):
    print('Reading some constants...')

# **************** this will and should be replaced with the real values obtained with sysex messages...
CC_0127_DEFAULT = 64 # I think 'in media stat virtus'

# ***************************************************************
# *** 1. RECEIVE DATA
# ***************************************************************
# *************************
# ** Channel Voice Messages
# *************************
#
#         Status         |       2nd byte         |     3rd byte
#          9nH           |          kkH           |       vvH
#
#
# n = MIDI channel number: 0H-FH (ch.1-ch.16)
# kk = note number : 00H-7FH (0-127)
# NOTE: Used for pitch changes when using VT effect
#
# **********************************
# Channel Voice Change STATUS Values
# **********************************
CV_MIC1_CH = 0x90
CV_MIC2_CH = 0x91
CV_WAVE1_CH = 0x92
CV_WAVE2_CH = 0x93
CV_SYSRET_CH = 0x94
CV_SYSSUB_CH = 0x95
CV_WAVEREC_CH = 0x9E
CV_LINE_MASTER_CH = 0x9F
#
# ************************* 
# ** Pitch Bend Change
# *************************
#
#         Status         |       2nd byte         |     3rd byte
#          EnH           |         llH            |       mmH
#
#
# n = MIDI channel number: 0H-FH (ch.1-ch.16)
# mm, ll = Pitch Bend value: 00 00H-40 00H-7F 7FH (-8192-0- +8191)
# NOTE: Used for pitch changes when using VT effect
#
# *******************************
# Pitch Bend Change STATUS Values
# *******************************
PB_MIC1_CH = 0xE0
PB_MIC2_CH = 0xE1
PB_WAVE1_CH = 0xE2
PB_WAVE2_CH = 0xE3
PB_SYSRET_CH = 0xE4
PB_SYSSUB_CH = 0xe5
PB_WAVEREC_CH = 0xEE
PB_LINE_MASTER_CH = 0xEF
#
# *************************
# ** Control Change
# *************************
#
#         Status         |       2nd byte         |     3rd byte
#          BnH                       mmH                   llH
#
# n = MIDI channel number: 0H-FH (ch. 1 to ch. 16:Refer to the correspondence chart)
# mm = Mixer parameter number:Refer to the correspondence chart
# ll = Mixer parameter value: 00H - 7FH (0 - 127)
# ****************************
# Control Change STATUS Values
# ****************************
CC_MIC1_CH = 0xB0
CC_MIC2_CH = 0xB1
CC_WAVE1_CH = 0xB2
CC_WAVE2_CH = 0xB3
CC_SYSRET_CH = 0xB4
CC_SYSSUB_CH = 0xB5
CC_WAVEREC_CH = 0xBE
CC_LINE_MASTER_CH = 0xBF
#
# *********************************************************
# * Correspondences Between MIDI Channels and Mixer Signals
# *********************************************************
#
#      MIDI channel      |           Signal
#           1Ch.         |  LINE (Line Mode), MIC1/GUITAR (Mic Mode), MIC1+MIC2 (MIC1+MIC2 Mode)
#           2Ch.         |  MIC2 (Mic mode only)
#           3Ch.         |  WAVE1
#           4Ch.         |  WAVE2
#           5Ch.         |  SysRET(system effect return Main bus)
#           6Ch.         |  SysSUB(system effect return Sub bus)
#           15Ch.        |  WAVE (Rec)
#           16Ch.        |  LINE (Master)
#
# **********************************************************
# * Mixer parameters and setting ranges
# **********************************************************
#
# Parameter              |           mm           |             ll (setting range)
# MIC/LINE Selector      |        21 (15H)        |     0: Mic Mode, 1: Line Mode, 2: MIC1+MIC2 Mode
# Pan                    |        10 (0AH)        |     0 (left) - 64 (center) - 127 (right)
# Send 1                 |        16 (10H)        |     0 - 127: Full/Compact Effect mode only
# Send 2                 |        17 (11H)        |     0 - 127: Full/Compact Effect mode only
# Mute                   |        18 (12H)        |     0 (OFF), 1 (ON: Mute)
# Solo                   |        19 (13H)        |     0 (OFF), 1 (ON: Solo)
# Sub Fader              |        20 (14H)        |     0 - 127
# Main Fader             |         7 (07H)        |     0 - 127
# Selector               |        22 (16H)        |     <Full/Compact Effect mode> 
#                                                        0: MIC1 (Mic Mode), LINE (Line Mode), MIC1+MIC2 (MIC1+MIC2 Mode),
#                                                        1: MIC2 (Mic Mode only), 
#                                                        2: WAVE1,
#                                                        3: WAVE2,
#                                                        4 to 7: CH1 to 4,
#                                                        8: SUB,
#                                                        9: MAIN 
#                                                       <VT Effect mode>
#                                                        0: MIC1 (Mic Mode), LINE (Line Mode),
#                                                        1: MIC2 (Mic Mode only),
#                                                        2: WAVE1,
#                                                        3: WAVE2,
#                                                        4: VT_OUT,
#                                                        5: MAIN
# Effect Switch          |        23 (17H)        |      0 (OFF), 1 (ON: Apply effect)

CC_MICLINESELECTOR_PAR = 21 # 0x15
# CC_MICLINESELECTOR_RANGE = { 'Mic Mode': 0, 'Line Mode': 1, 'MIC1+MIC2 Mode': 2}
CC_PAN_PAR = 10 # 0x0A - 0 - 64 - 127 (LEFT - CENTER - RIGHT)
CC_SEND1_PAR = 16 # 0x10
CC_SEND2_PAR = 17 # 0x11
CC_MUTE_PAR = 18 # 0x12
CC_SOLO_PAR = 19 # 0x13
CC_SUB_FADER_PAR = 20 # 0x14
CC_MAIN_FADER_PAR = 7 # 0x70
CC_SELECTOR_PAR = 22 # 0x16
CC_EFFECTSWITHC_PAR = 23 # 0x23

# ******************************************************
# * Correspondences Between Mixer Signals and Parameters
# ******************************************************
#
#                   |  MIC1/LINE/ | MIC2 | WAVE1 | WAVE2 | SysRET |  SysSUB | WAVE  | LINE 
#    Parameter      |  MIC1MIC2   | 2Ch. |  3Ch. |  4Ch. |   5Ch. |    6Ch. | 15Ch. | 16Ch.
#                   |    1Ch.     |      |       |       |        |         |       |
#                   |             |      |       |       |        |         |       |
# MIC/LINE Selector |     O       |   -  |   -   |   -   |    -   |    -    |   -   |   -
#    21 (15H)       |             |      |       |       |        |         |       |
#                   |             |      |       |       |        |         |       |
#       Pan         |     O       |   O  |   -   |   -   |    -   |    -    |   -   |   -
#    10 (0AH)       |             |      |       |       |        |         |       |
#                   |             |      |       |       |        |         |       |
#     Send 1        |     O       |   O  |   O   |   O   |    O   |    O    |   -   |   -
#    16 (10H)       |             |      |       |       |        |         |       |
#                   |             |      |       |       |        |         |       |
#     Send 2        |     O       |   O  |   O   |   O   |    O   |    O    |   -   |   -
#    17 (11H)       |             |      |       |       |        |         |       |
#                   |             |      |       |       |        |         |       |
#      Mute         |     O       |   O  |   O   |   O   |    -   |    -    |   -   |   -
#    18 (12H)       |             |      |       |       |        |         |       |
#                   |             |      |       |       |        |         |       |
#      Solo         |     O       |   O  |   O   |   O   |    -   |    -    |   -   |   -
#    19 (13H)       |             |      |       |       |        |         |       |
#                   |             |      |       |       |        |         |       |
#    Sub Fader      |     O       |   O  |   O   |   O   |    -   |    -    |   -   |   -
#    20 (14H)       |             |      |       |       |        |         |       |
#                   |             |      |       |       |        |         |       |
#    Main Fader     |     O       |   O  |   O   |   O   |    -   |    -    |   O   |   O
#     7 (07H)       |             |      |       |       |        |         |       |
#                   |             |      |       |       |        |         |       |
#     Selector      |     -       |   -  |   -   |   -   |    -   |    -    |   O   |   O
#    22 (16H)       |             |      |       |       |        |         |       |
#                   |             |      |       |       |        |         |       |
#   Effect Switch   |     O       |   O  |   O   |   O   |    O   |    O    |   -   |   -
#    23 (17H)       |             |      |       |       |        |         |       |
# **********************************************************************************************
#
# Omitting the RPN MSB/LSB and Data Entry part. TODO in a near future, at least for documentation purposes
# 
# MIDI EXCLUSIVE
# ********** I SHALL PUT SOME CONSTANTS FOR THE SYSEXs AND PASTE THE DOCUMENTATION AS WELL **********
# LET'S START
#
# let's set the sleep time between SYSEXex (in seconds)
SLEEP_TIME = 0.05 

# This should be common for all SYSEXes
UA_SYSEX_ID= [0x41,0x10,0x00,0x11]

# Request data 1 RQ1 (0x11)
RQ1_STATUS = [0xF0]
RQ1_COMMAND = [0x11]

# Data set 1 (DT1)
DT1_STATUS = [0xF0]
DT1_COMMAND = [0x12]

# Address map (one last 0xnn is the actual parameter)

# Mixer Parameters


# UA-100 Control

UA100_CONTROL = [0x00, 0x40, 0x00]

# MODE
UA100_MODE = [0x00]
UA100_MODE_SIZE = [0x00, 0x00, 0x00, 0x01]
#UA100_MODE_DATARANGE = range(0x01,10)
    # 1: PC Mode(VT Effect Mode)
    # 3: PC Mode(Compact Effect Mode)
    # 4: PC Mode(Full Effect Mode)
    # 5: VT Mode
    # 6: Vocal Mode
    # 7: Guitar Mode
    # 8: GAME Mode
    # 9: BYPASS Mode
    # * Send only (sent when the Effect Type Selector is switched or when a requested by Data Request 1)

# COPYRIGHT
COPYRIGHT = [0x01]
COPYRIGHT_SIZE = [0x00, 0x00, 0x00, 0x01]

# Mixer Input Control
MIXER_INPUT_CONTROL = [0x00, 0x40, 0x10]
MIXER_INPUT_PAN1 = [0x01]
MIXER_INPUT_PAN1_SIZE = [0x00, 0x00, 0x00, 0x01]
MIXER_INPUT_PAN2 = [0x02]
MIXER_INPUT_PAN2_SIZE = [0x00, 0x00, 0x00, 0x01]
MIXER_INPUT_MONITOR_SW = [0x03]
MIXER_INPUT_MONITOR_SW_SIZE = [0x00, 0x00, 0x00, 0x01]

#...
MIC1_FADER = [0x00, 0x40, 0x11, 0x05]
MIC1_FADER_SIZE = [0x00, 0x00, 0x00, 0x01]
MIC2_FADER = [0x00, 0x40, 0x12, 0x05]
MIC2_FADER_SIZE = [0x00, 0x00, 0x00, 0x01]
WAVE1_FADER = [0x00, 0x40, 0x13, 0x05]
WAVE1_FADER_SIZE = [0x00, 0x00, 0x00, 0x01]
# WAVE1_FADER_RANGErange(0x00, 0x80)
WAVE2_FADER = [0x00, 0x40, 0x14, 0x05]
WAVE2_FADER_SIZE = [0x00, 0x00, 0x00, 0x01]
#...

EFFECT_PARAMETER = [0x00, 0x40, 0x01]

MIXER_EFFECT_CONTROL = [0x00, 0x40, 0x40]

# Mixer Output Control
MIXER_OUTPUT_CONTROL = [0x00, 0x40, 0x50]
#
MASTER_SELECT_MIXERMODE = {0x00: 'LINE/MIC1/MIC1+MIC2',\
                           0x01: 'MIC2',\
                           0x02: 'WAVE1',\
                           0x03: 'WAVE2',\
                           0x04: 'CH1',\
                           0x05: 'CH2',\
                           0x06: 'CH3',\
                           0x07: 'CH4',\
                           0x08: 'SUB',\
                           0x09: 'MAIN',\
                           0x0A: 'WAVE(REC)OUT'}
MASTER_SELECT_VTMIXERMODE = {0x00: 'LINE/MIC1',\
                             0x01: 'MIC2',\
                             0x02: 'WAVE1',\
                             0x03: 'WAVE2',\
                             0x04: 'VT_OUT',\
                             0x05: 'MAIN',\
                             0x06: 'WAVE(REC)OUT'}
WAVE_SELECT_MIXERMODE = {0x00: 'LINE/MIC1/MIC1+MIC2',\
                           0x01: 'MIC2',\
                           0x02: 'WAVE1',\
                           0x03: 'WAVE2',\
                           0x04: 'CH1',\
                           0x05: 'CH2',\
                           0x06: 'CH3',\
                           0x07: 'CH4',\
                           0x08: 'SUB',\
                           0x09: 'MAIN'}
WAVE_SELECT_VTMIXERMODE = {0x00: 'LINE/MIC1',\
                             0x01: 'MIC2',\
                             0x02: 'WAVE1',\
                             0x03: 'WAVE2',\
                             0x04: 'VT_OUT',\
                             0x05: 'MAIN'}

# Mixer Output Mode:
# 0: VT MIXER MODE
# 1: MIXER MODE
MIXER_OUTPUT_MODE = 1

#...
MIXER_OUTPUT_MASTERLEVEL = [0x03]
MIXER_OUTPUT_MASTERLEVEL_SIZE = [0x00, 0x00, 0x00, 0x01]
#MIXER_OUTPUT_MASTERLEVEL_RANGE = range(0x00, 0x80)
MIXER_OUTPUT_WAVEREC = [0x02]
MIXER_OUTPUT_WAVEREC_SIZE = [0x00, 0x00, 0x00, 0x01]
#...


PRESET_EFFECT_CONTROL = [0x00, 0x40, 0x60]

# End of exclusive (EOX)
EOX = [0xF7]

if (DEBUG_MODE):
    print('Done!')


def pm_open(device):
    '''
    Possibly not the best solution.
    '''
    
    # the in and out instances must be in the global scope
    # I'm still convinced that's not the right solution...
    global pmout
    global pmin
    
    if (REAL_UA_MODE):
        if (DEBUG_MODE):
            print('Opening device: ',device,' for ouput and device: ', device+1, 'for input')
        # Open device for output
        pmout = pm.midi.Output(device)
        # Open "the next" device for input
        pmin = pm.midi.Input(device+1)
        

@QtCore.pyqtSlot()
def mutes(window, checked):
    '''
    Muting channels.
    Actually, the mute button should disappear from not soloed channels. To be done.
    '''
    global pmout
    
    if (DEBUG_MODE):
        pass
    
    if (checked):
        if (REAL_UA_MODE):
            pmout.write_short(window.sender().parent().property('channel').toPyObject(), CC_MUTE_PAR ,1)
        else:
            print('write_short to pmout on channel: ',window.sender().parent().property('channel').toPyObject(), ', parameter: ', CC_MUTE_PAR , 'value: 1')
    else:
        if (REAL_UA_MODE):
            pmout.write_short(window.sender().parent().property('channel').toPyObject(), CC_MUTE_PAR ,0)
        else:
            print('write_short to pmout on channel: ',window.sender().parent().property('channel').toPyObject(), ', parameter: ', CC_MUTE_PAR , 'value: 0')

@QtCore.pyqtSlot()
def uniqueSolos(window, ui, checked):
    '''
    unchecks all other solo buttons if the present is checked.
    besides, it actually soloes/unsoloes the channel
    '''
    
    global pmout
    
    soloers =['Mic1','Mic2','Wave1','Wave2']
    soloers.remove(str(window.sender().parent().objectName()))
    if (checked):
        if (DEBUG_MODE == 1):
            print(soloers)
            print('unchecking and desoloing ')
            print('soloing ',str(window.sender().parent().objectName()))
        if (REAL_UA_MODE):
            pmout.write_short(window.sender().parent().property('channel').toPyObject(),CC_SOLO_PAR,1)
        for soloer in soloers:
            soloingObj = window.findChild(QtGui.QGroupBox, soloer)
            pmout.write_short(soloingObj.property('channel').toPyObject(),CC_SOLO_PAR,0)
            soloingButtonStr = soloer+'Solo'
            #print soloingButtonStr
            soloingButton = soloingObj.findChild(QtGui.QPushButton, soloingButtonStr)
            soloingButton.setChecked(False)
            if (DEBUG_MODE):
                # review those fucking debug messages. They are just fucking messed up!
                print('desoloing: ',soloingObj.objectName())
                print(soloingObj.property('channel').toPyObject())
    else:
        if (REAL_UA_MODE):
            pmout.write_short(window.sender().parent().property('channel').toPyObject(),CC_SOLO_PAR,0)
        else:
            print('pmout.write_short(',window.sender().parent().property('channel').toPyObject(),',',CC_SOLO_PAR,'0)')

@QtCore.pyqtSlot()
def valueChange(a,b,val):
    '''
    custom slot to connect to the changes in the interface with write_short to send the control change messages
    '''
    global pmout
    
    if (REAL_UA_MODE):
        pmout.write_short(a,b,val)
    
    if (DEBUG_MODE == 1):
        print(hex(a),b,val)

@QtCore.pyqtSlot()
def updateDeviceLabels(ui, midiDevs, indice, defaultDevice):
    '''
    I should be an easy task to update label according to a combo box...
    '''
    ui.midiApiText.setText(str(midiDevs[indice][0]))
    ui.deviceNameText.setText(str(midiDevs[indice][1]))
    if (midiDevs[indice][2] == 1 and midiDevs[indice][3] == 0):
        ui.deviceIOText.setText('INPUT')
    elif (midiDevs[indice][2] == 0 and midiDevs[indice][3] == 1):
        ui.deviceIOText.setText('OUTPUT')
    else:
        ui.deviceIOText.setText('N/A')
    
    if (indice == defaultDevice):
        ui.reccomendedLabel.setText('RECCOMENDED!\r\nYou don\'t really want to change it!')
        ui.reccomendedLabel.setStyleSheet('color: red; font-style: bold')
    else:
        ui.reccomendedLabel.setText('')
    
    if (DEBUG_MODE == 1):
        print(midiDevs[indice][2], midiDevs[indice][3])
        

@QtCore.pyqtSlot()
def setMidiDevice(index):
    '''
    This slot should set the midi device selected in the combo box of the starting dialog
    '''
    global UA100CONTROL
    
    UA100CONTROL=index
    if (DEBUG_MODE ==1):
        print('Index = ', index)
        print('UA100CONTROL = ',UA100CONTROL)

#@QtCore.pyqtSlot(int)
#def testing_self(self, value):
#    '''
#    test of self
#    '''
#    if (DEBUG_MODE == 1):
#        print('Self = ', self.sender().parent().objectName(), ' Value: ',value)
#    pass

def setupMenus(ui, window):
    ui.actionReset_Mixer.triggered.connect(functools.partial(resetMixer, ui))
    ui.actionQuit.triggered.connect(QtGui.qApp.quit)

def setupMixer(ui,window):
    '''
    I thought it'd be better to setup the connections here, as qt4designer is not so nice with custom slots.
    Moreover, setting up the connection in qt4designer means that every single new connection must be done outside
    of here.
    '''
    
    #ui.Mic1Fader.valueChanged.connect(functools.partial(testing_self, window))

    # *************** MIC1 *********************

    ui.Mic1.setProperty("channel", CC_MIC1_CH)
    
    # Setting Up the Mic1 Fader
    ui.Mic1Fader.valueChanged.connect(ui.Mic1Lcd.display)
    ui.Mic1Fader.valueChanged.connect(functools.partial(valueChange, CC_MIC1_CH, CC_MAIN_FADER_PAR))
    ui.Mic1Fader.setProperty("parameter", CC_MAIN_FADER_PAR)

    # Setting Up the Mic1 Pan Dial
    ui.Mic1Pan.valueChanged.connect(ui.Mic1PanLcd.display)
    ui.Mic1Pan.valueChanged.connect(functools.partial(valueChange, CC_MIC1_CH, CC_PAN_PAR))
    ui.Mic1Pan.setProperty("parameter", CC_PAN_PAR)
    
    # Setting up Ins1&2
    ui.Mic1Ins1.valueChanged.connect(functools.partial(valueChange, CC_MIC1_CH, CC_SEND1_PAR))
    ui.Mic1Ins2.valueChanged.connect(functools.partial(valueChange, CC_MIC1_CH, CC_SEND2_PAR))
    
    # Setting Up the Mic1 Solo Button ** THERE CAN ONLY BE ONE "SOLO" CHECKED, THUS... **
    ui.Mic1Solo.toggled.connect(functools.partial(uniqueSolos, window, ui))
    
    ui.Mic1Mute.toggled.connect(functools.partial(valueChange, CC_MIC1_CH, CC_MUTE_PAR))
    
    # Setting Up the SubFader
    ui.Mic1SubFader.valueChanged.connect(ui.Mic1SubLcd.display)
    ui.Mic1SubFader.valueChanged.connect(functools.partial(valueChange, CC_MIC1_CH, CC_SUB_FADER_PAR))
    
    # hiding the subs...
    ui.Mic1SubFader.hide()
    ui.Mic1SubLcd.hide()
    
    
    # *************** MIC2 *********************
    
    ui.Mic2.setProperty("channel", CC_MIC2_CH)
    
    # Setting Up the Mic2 Fader
    ui.Mic2Fader.valueChanged.connect(ui.Mic2Lcd.display)
    ui.Mic2Fader.valueChanged.connect(functools.partial(valueChange, CC_MIC2_CH, CC_MAIN_FADER_PAR))
    ui.Mic2Fader.setProperty("parameter", CC_MAIN_FADER_PAR)
    
    # Setting Up the Mic2 Pan Dial
    ui.Mic2Pan.valueChanged.connect(ui.Mic2PanLcd.display)
    ui.Mic2Pan.valueChanged.connect(functools.partial(valueChange, CC_MIC2_CH, CC_PAN_PAR))
    ui.Mic2Pan.setProperty("parameter", CC_PAN_PAR)
    
    # Setting up Ins1&2
    ui.Mic2Ins1.valueChanged.connect(functools.partial(valueChange, CC_MIC2_CH, CC_SEND1_PAR))
    ui.Mic2Ins2.valueChanged.connect(functools.partial(valueChange, CC_MIC2_CH, CC_SEND2_PAR))
    
    # Setting Up the Mic2 Solo Button ** THEY CAN BE ONLY ONE SOLO CHECKED, THUS... **
    #ui.mic2Solo.toggled.connect(functools.partial(uniqueSolos, ui, window, ui.mic2Solo, 2))
    #ui.mic2Solo.toggled.connect(functools.partial(uniqueSolos, ui.mic1Solo, ui.wave1Solo, ui.wave2Solo))
    ui.Mic2Solo.toggled.connect(functools.partial(uniqueSolos, window, ui))
    
    ui.Mic2Mute.toggled.connect(functools.partial(valueChange, CC_MIC2_CH, CC_MUTE_PAR))
    
    # hiding the subs...
    ui.Mic2SubFader.hide()
    ui.Mic2SubLcd.hide()
    
    # Setting Up the SubFader
    ui.Mic2SubFader.valueChanged.connect(ui.Mic2SubLcd.display)
    ui.Mic2SubFader.valueChanged.connect(functools.partial(valueChange, CC_MIC2_CH, CC_SUB_FADER_PAR))
    
    
    # *************** WAVE1 *********************
    
    ui.Wave1.setProperty("channel", CC_WAVE1_CH)
    
    # Setting up the Wave1 Fader
    ui.Wave1Fader.valueChanged.connect(ui.Wave1Lcd.display)
    ui.Wave1Fader.valueChanged.connect(functools.partial(valueChange, CC_WAVE1_CH, CC_MAIN_FADER_PAR))
    #ui.Wave1Fader.setProperty("value", CC_0127_DEFAULT)
    ui.Wave1Fader.setProperty("parameter", CC_MAIN_FADER_PAR)
    
    # Setting up Ins1&2
    ui.Wave1Ins1.valueChanged.connect(functools.partial(valueChange, CC_WAVE1_CH, CC_SEND1_PAR))
    ui.Wave1Ins2.valueChanged.connect(functools.partial(valueChange, CC_WAVE1_CH, CC_SEND2_PAR))
    
    # Setting Up the Wave1 Solo Button ** THEY CAN BE ONLY ONE SOLO CHECKED, THUS... **
    #ui.wave1Solo.toggled.connect(functools.partial(uniqueSolos, ui, window, ui.wave1Solo, 3))
    #ui.wave1Solo.toggled.connect(functools.partial(uniqueSolos, ui.mic1Solo, ui.wave2Solo, ui.mic2Solo))
    ui.Wave1Solo.toggled.connect(functools.partial(uniqueSolos, window, ui))
    ui.Wave1Mute.toggled.connect(functools.partial(valueChange, CC_WAVE1_CH, CC_MUTE_PAR))
    
    # Setting Up the SubFader
    ui.Wave1SubFader.valueChanged.connect(ui.Wave1SubLcd.display)
    ui.Wave1SubFader.valueChanged.connect(functools.partial(valueChange,CC_WAVE1_CH, CC_SUB_FADER_PAR))
    
    # hiding the subs...
    ui.Wave1SubFader.hide()
    ui.Wave1SubLcd.hide()
    
    
    # *************** WAVE2 *********************
    
    ui.Wave2.setProperty("channel", CC_WAVE2_CH)
    
    # Setting up the Wave1 Fader
    ui.Wave2Fader.valueChanged.connect(ui.Wave2Lcd.display)
    ui.Wave2Fader.valueChanged.connect(functools.partial(valueChange, CC_WAVE2_CH, CC_MAIN_FADER_PAR))
    #ui.Wave2Fader.setProperty("value", CC_0127_DEFAULT)
    ui.Wave2Fader.setProperty("parameter", CC_MAIN_FADER_PAR)    
    
    # Setting up Ins1&2
    ui.Wave2Ins1.valueChanged.connect(functools.partial(valueChange, CC_WAVE2_CH, CC_SEND1_PAR))
    ui.Wave2Ins2.valueChanged.connect(functools.partial(valueChange, CC_WAVE2_CH, CC_SEND2_PAR))
    
    # Setting Up the Wave2 Solo Button ** THEY CAN BE ONLY ONE SOLO CHECKED, THUS... **
    #ui.wave2Solo.toggled.connect(functools.partial(uniqueSolos, ui, window, ui.wave1Solo, 4))
    #ui.wave2Solo.toggled.connect(functools.partial(uniqueSolos, ui.mic1Solo, ui.wave1Solo, ui.mic2Solo))
    ui.Wave2Solo.toggled.connect(functools.partial(uniqueSolos, window, ui))
    
    ui.Wave2Mute.toggled.connect(functools.partial(valueChange, CC_WAVE2_CH, CC_MUTE_PAR))
    
    # Setting Up the SubFader
    ui.Wave2SubFader.valueChanged.connect(ui.Wave2SubLcd.display)
    ui.Wave2SubFader.valueChanged.connect(functools.partial(valueChange, CC_WAVE2_CH, CC_SUB_FADER_PAR))
    
    # hiding the subs...
    ui.Wave2SubFader.hide()
    ui.Wave2SubLcd.hide()
    
    
    # *************** MASTERLINE *********************
    
    ui.MasterLineFader.setProperty("channel", CC_LINE_MASTER_CH)
    
    # Setting Up the MasterLine Fader
    ui.MasterLineFader.valueChanged.connect(ui.MasterLineLcd.display)
    ui.MasterLineFader.valueChanged.connect(functools.partial(valueChange, CC_LINE_MASTER_CH, CC_MAIN_FADER_PAR))
    ui.MasterLineFader.setProperty("parameter", CC_MAIN_FADER_PAR)
    
    # *************** WAVE (REC) **********************
    
    # Setting up the Wave (Rec) Fader
    ui.WaveRecFader.valueChanged.connect(ui.WaveRecLcd.display)
    ui.WaveRecFader.valueChanged.connect(functools.partial(valueChange, CC_WAVEREC_CH, CC_MAIN_FADER_PAR))
    
    
    # *************** SYSEFF **************************
    
    # Return
    ui.SysEffRet1.valueChanged.connect(functools.partial(valueChange, CC_SYSRET_CH, CC_SEND1_PAR))
    ui.SysEffRet2.valueChanged.connect(functools.partial(valueChange, CC_SYSRET_CH, CC_SEND2_PAR))
    # Sub
    ui.SysEffSub1.valueChanged.connect(functools.partial(valueChange, CC_SYSSUB_CH, CC_SEND1_PAR))
    ui.SysEffSub2.valueChanged.connect(functools.partial(valueChange, CC_SYSSUB_CH, CC_SEND2_PAR))
    
    
    
    # SUB BUTTON
    
    ui.SubButton.toggled.connect(functools.partial(showHideSub, ui, window))
    
    # hiding more...
    ui.SysEffSub1.hide()
    ui.SysEffSub2.hide()
    ui.SysEffSubLabel.hide()
    
    # Setting Up Mixer Output Sources for Master
    ui.OutputMasterSourceSelect.currentIndexChanged.connect(functools.partial(valueChange, CC_LINE_MASTER_CH, CC_SELECTOR_PAR))
    if (MIXER_OUTPUT_MODE):
        for key in MASTER_SELECT_MIXERMODE.keys():
            ui.OutputMasterSourceSelect.addItem(MASTER_SELECT_MIXERMODE[key])
        ui.OutputMasterSourceSelect.setCurrentIndex(0x09)
        
    # Setting Up Mixer Output Sources for Wave(Rec)
    ui.OutputWaveRecSourceSelect.currentIndexChanged.connect(functools.partial(valueChange, CC_WAVEREC_CH, CC_SELECTOR_PAR))
    if (MIXER_OUTPUT_MODE):
        for key in WAVE_SELECT_MIXERMODE.keys():
            ui.OutputWaveRecSourceSelect.addItem(WAVE_SELECT_MIXERMODE[key])
        ui.OutputWaveRecSourceSelect.setCurrentIndex(0x09)
        

def showHideSub(ui, window, checked):
    if (checked):
        ui.Mic1SubFader.show()
        ui.Mic1SubLcd.show()
        ui.Mic2SubFader.show()
        ui.Mic2SubLcd.show()
        ui.Wave1SubFader.show()
        ui.Wave1SubLcd.show()
        ui.Wave2SubFader.show()
        ui.Wave2SubLcd.show()
        ui.SysEffSub1.show()
        ui.SysEffSub2.show()
        ui.SysEffSubLabel.show()
    else:
        ui.Mic1SubFader.hide()
        ui.Mic1SubLcd.hide()
        ui.Mic2SubFader.hide()
        ui.Mic2SubLcd.hide()
        ui.Wave1SubFader.hide()
        ui.Wave1SubLcd.hide()
        ui.Wave2SubFader.hide()
        ui.Wave2SubLcd.hide()
        ui.SysEffSub1.hide()
        ui.SysEffSub2.hide()
        ui.SysEffSubLabel.hide()

def resetMixer(ui):
    '''
    Reset all mixer values to average ones.
    ***************************************
    A better idea could be to retrieve the current values (with sysex messages) and use them...
    maybe in the future
    ***************************************
    '''
    ui.MasterLineFader.setProperty("value", CC_0127_DEFAULT)
    ui.Wave1Fader.setProperty("value", CC_0127_DEFAULT)
    #ui.Wave1SubFader.setProperty("value", CC_0127_DEFAULT)
    ui.Wave2Fader.setProperty("value", CC_0127_DEFAULT)
    #ui.Wave2SubFader.setProperty("value", CC_0127_DEFAULT)
    ui.Mic1Fader.setProperty("value", CC_0127_DEFAULT)
    ui.Mic1Pan.setProperty("value", CC_0127_DEFAULT)
    #ui.Mic1SubFader.setProperty("value", CC_0127_DEFAULT)
    ui.Mic2Fader.setProperty("value", CC_0127_DEFAULT)
    ui.Mic2Pan.setProperty("value", CC_0127_DEFAULT)
    #ui.Mic2SubFader.setProperty("value", CC_0127_DEFAULT)

def actualMidiDevices():
    '''
    This should enumerate the devices to (later on) give then the possibility to choose one or guess the right one
    Returns a dictionary with tuples like 
    
    midiDevs = { 0: (tuple), 1: (tuple), ... }
    
    where the tuple is in the format:
    
    ('ALSA', 'UA-100 MIDI 2', 0, 1, 0)
    
    '''
    # Count the MIDI devices connected
    if (REAL_UA_MODE):
        numDevs = pm.get_count()
    else:
        numDevs = 5 
    # Initialize the device dictionary
    # midiDevs = { 0: (tuple), 1: (tuple), ... }
    #
    midiDevs = {}
    for dev in range(0,numDevs):
        # the portmidi get_device_info() returns a tuple
        if (REAL_UA_MODE):
            midiDevs[dev]=pm.get_device_info(dev)
        else:
            # fake entries...
            midiDevs[dev]=('pippo','pluto',1,1,1)
    return midiDevs

def rightMidiDevice(midiDevs):
    '''
    Guess the right device for sending Control Change and SysEx messages.
    
    I suppose it is HEAVY dependant on pyPortMidi and ALSA: 
    if *they* change something in the structure of the device info, we are lost!
    
    It scans the midiDevs (dictionary!) looking for something like 'UA-100 Control' with the output flag set to 1.
    '''
    for i in range(0,len(midiDevs)):
        if (midiDevs[i][1] == 'UA-100 Control') & (midiDevs[i][3] == 1):
            if (DEBUG_MODE == 1):
                print('Trovato! Il controller e il device ',i, ', ovvero ',midiDevs[i][1])
            return int(i)

def setupDevicesList(ui,window,midiDevs,defaultUA100Control):
    '''
    Sets up the ComboBox with a list of MIDI devices. Not that the combo box must be connected: at the moment it is not.
    '''
    
    global UA100CONTROL
    for i in range(0,len(midiDevs)):
        ui.outputDevicesList.addItem(str(midiDevs[i]), i)
    
    # update the device information when selecting the devices in the combobox
    ui.outputDevicesList.currentIndexChanged.connect(functools.partial(window.updateDeviceLabels, ui, midiDevs, defaultUA100Control))
    
    # call the setMidiDevice custom slot to tell everyone whitch one is the selected device (output)
    ui.outputDevicesList.currentIndexChanged.connect(window.setMidiDevice)
    
    # send true if OK is clicked
    ui.dialogOK.clicked.connect(window.accept)
    
    # send false if Quit is clicked (and close application)
    ui.dialogQuit.clicked.connect(window.reject)
    
    # set the current index to the guessed right outpud midi device for the UA100 controller
    ui.outputDevicesList.setCurrentIndex(defaultUA100Control)
    
def setInitMixerLevels(ui, window):
    '''
    It works. It send SYSEX and reads answers. But there must me a better way to read and write.
    Actually there is, but I'm lazy.
    '''
    
    global pmout, pmin

    send_RQ1(MIXER_OUTPUT_CONTROL + MIXER_OUTPUT_MASTERLEVEL + MIXER_OUTPUT_MASTERLEVEL_SIZE)
    time.sleep(SLEEP_TIME)
    answerList = sysexRead(4)
    masterLevel= answerList[2][0][2]
    ui.MasterLineFader.setProperty("value", masterLevel)
    
    send_RQ1(MIXER_OUTPUT_CONTROL + MIXER_OUTPUT_WAVEREC + MIXER_OUTPUT_WAVEREC_SIZE)
    time.sleep(SLEEP_TIME)
    answerList = sysexRead(4)
    waverecLevel= answerList[2][0][2]
    ui.WaveRecFader.setProperty("value", waverecLevel)
    
    send_RQ1(MIC1_FADER + MIC1_FADER_SIZE)
    time.sleep(SLEEP_TIME)
    answerList = sysexRead(4)
    mic1Level= answerList[2][0][2]
    ui.Mic1Fader.setProperty("value", mic1Level)
    
    send_RQ1(MIC2_FADER + MIC2_FADER_SIZE)
    time.sleep(SLEEP_TIME)
    answerList = sysexRead(4)
    mic2Level= answerList[2][0][2]
    ui.Mic2Fader.setProperty("value", mic2Level)
    
    send_RQ1(WAVE1_FADER + WAVE1_FADER_SIZE)
    time.sleep(SLEEP_TIME)
    answerList = sysexRead(4)
    wave1Level= answerList[2][0][2]
    ui.Wave1Fader.setProperty("value", wave1Level)
    
    send_RQ1(WAVE2_FADER + WAVE2_FADER_SIZE)
    time.sleep(SLEEP_TIME)
    answerList = sysexRead(4)
    wave2Level= answerList[2][0][2]
    ui.Wave2Fader.setProperty("value", wave2Level)

def sysexRead(buffer_size):
    global pmin
    
    if (REAL_UA_MODE):
        answer = pmin.read(buffer_size)
    else:
        answer = CC_0127_DEFAULT
    
    return answer
    
    
def send_RQ1(data):
    '''
    Here we are about to send a Request Data 1.
    Never forget to checksum!
    
    ** Note
    The first part of the message is fixed. What can change is the data (of course, it's function agument!)
    AND the checksum, which on his side, depends on the data.
    '''
    global pmout, pmin
    checksum_result = checksum(data)
    message = RQ1_STATUS \
              +UA_SYSEX_ID \
              + RQ1_COMMAND \
              + data \
              + checksum_result\
              + EOX
    if (REAL_UA_MODE):
        pmout.write_sys_ex(pm.time(),message)
    
def checksum(toChecksum):
    '''
    That's how the UA-100 does the checksum:
    Take the data part of SYSEXES and do the maths.
    '''
    checksum_value = (128 - (sum(toChecksum) % 128))
    checksum_list = [checksum_value]
    return list(checksum_list)
    
    pass

def main(): 
    '''
    it already needs a big clean-up. *Andiamo bene...*
    
    '''
    
    # **************************** MIDI PART: could it go somewhere else? **********************************************
    
    # initialize the portmidi interface
    
    if (REAL_UA_MODE):
        pm.init()
    
    # get the list of the Midi Devices according to portmidy
    midiDevs=actualMidiDevices()
    
    if (DEBUG_MODE == 1):
        print('MIDI DEVICES FOUND: ',len(midiDevs),'. They are: ', midiDevs)
        
    # guess the right midi device
    if (REAL_UA_MODE):
        UA100CONTROL = rightMidiDevice(midiDevs)
    else:
        UA100CONTROL = 1
    
    if (DEBUG_MODE == 1):
        print('UA100CONTROL = ',UA100CONTROL)

    # *******************************************************************************************************************

    app = QtGui.QApplication(sys.argv)
    
    # Showing the device selection dialog to select the midi device to use for the UA-100 controller
    # Actually, given the right portmidi API, the correct one should be automatically guessed.
    midiDevsDialog= QtGui.QDialog()
    midiDevsDialog_ui = Ui_deviceSelection()
    midiDevsDialog_ui.setupUi(midiDevsDialog)
    
    midiDevsDialog.updateDeviceLabels = updateDeviceLabels
    midiDevsDialog.setMidiDevice = setMidiDevice

    mixerMainWindow = QtGui.QMainWindow()
    
    # Add custom slots to the mixerMainWindow instance
    # *** I discovered this is not needed. So they just stay as memory. ***
    #mixerMainWindow.valueChange = valueChange
    #mixerMainWindow.uniqueSolos = uniqueSolos
    #mixerMainWindow.testing_self = testing_self
    
    # inizializing the UI inside the mixerMainWindow
    ui = Ui_MainWindow()
    ui.setupUi(mixerMainWindow)

    # Changing the device in the device list
    # **************************************************************
    setupDevicesList(midiDevsDialog_ui,midiDevsDialog,midiDevs,UA100CONTROL)
    # **************************************************************

    if not midiDevsDialog.exec_():
        # We quit if the the selection dialog quits
        if (DEBUG_MODE == 1):
            print('Bye.')
        sys.exit()
    
    # first, open the selected device
    pm_open(UA100CONTROL)
    
    # then set up the mixer
    setupMixer(ui,mixerMainWindow)
    
    # and the menus
    setupMenus(ui, mixerMainWindow)
    
    # and reset it to "mean" values
    # resetMixer(ui,mixerMainWindow)
    # NO. I try to read the actual values
    
    if (REAL_UA_MODE):
        setInitMixerLevels(ui, mixerMainWindow)
    
    # let the drums roll! We are now ready to show the mixer!
    mixerMainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # brutal way to catch the CTRL+C signal if run in the console...
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    #starting the program
    main()
