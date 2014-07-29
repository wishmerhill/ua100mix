import sys
import os
import functools
import pyportmidi as pm
from PyQt4 import QtGui, QtCore
from global_constants import *
from main_ui import *
from main_ui_setup import *
from device_sel_ui import *
from types import MethodType


# Defining costants (taken from UA-100 documentation)
# and copying some useful documentation excerts

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

# ********************************
# ***** DEBUG MODE CONTROL *******
# SET:
#      1: true
#      0: false

DEBUG_MODE = 1

# ********************************

def pm_open(device):
    '''
    Possibly not the best solution.
    '''
    
    # the in and out instances must be in the global scope
    # I'm still convinced that's not the right solution...
    global pmout
    global pmin
    
    # Open device for output
    pmout = pm.midi.Output(device)
    
    # Open "the next" device for input
    pmin = pm.midi.Input(device+1)
    
@QtCore.pyqtSlot()
def valueChange(a,b,val):
    '''
    custom slot to connect to the changes in the interface with write_short to send the control change messages
    '''
    global pmout
    
    pmout.write_short(a,b,val)
    
    if (DEBUG_MODE == 1):
        print hex(a),b,val

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
        print midiDevs[indice][2], midiDevs[indice][3]
        
@QtCore.pyqtSlot()
def setMidiDevice(index):
    '''
    This slot should set the midi device selected in the combo box of the starting dialog
    '''
    global UA100CONTROL
    
    UA100CONTROL=index
    if (DEBUG_MODE ==1):
        print 'Index = ', index
        print 'UA100CONTROL = ',UA100CONTROL

def setupMixer(ui,window):
    '''
    I thought it'd be better to setup the connections here, as qt4designer is not so nice with custom slots.
    Moreover, setting up the connection in qt4designer means that every single new connection must be done outside
    of here.
    '''
    
    # *************** MIC1 *********************

    # Setting Up the Mic1 Fader
    ui.Mic1.valueChanged.connect(ui.Mic1Lcd.display)
    ui.Mic1.valueChanged.connect(functools.partial(window.valueChange, CC_MIC1_CH, CC_MAIN_FADER_PAR))
    #ui.Mic1.setProperty("value", CC_0127_DEFAULT)
    ui.Mic1.setProperty("channel", CC_MIC1_CH)
    ui.Mic1.setProperty("parameter", CC_MAIN_FADER_PAR)
    
    # Setting Up the Mic1 Pan Dial
    ui.Mic1Pan.valueChanged.connect(ui.Mic1PanLcd.display)
    ui.Mic1Pan.valueChanged.connect(functools.partial(window.valueChange, CC_MIC1_CH, CC_PAN_PAR))
    #ui.Mic1Pan.setProperty("value", CC_0127_DEFAULT)
    ui.Mic1Pan.setProperty("channel", CC_MIC1_CH)
    ui.Mic1Pan.setProperty("parameter", CC_PAN_PAR)
    
    # Setting Up the Mic1 Solo Button ** THEY CAN BE ONLY ONE SOLO CHECKED, THUS... **
    
    # *************** MIC2 *********************
    
    # Setting Up the Mic2 Fader
    ui.Mic2.valueChanged.connect(ui.Mic2Lcd.display)
    ui.Mic2.valueChanged.connect(functools.partial(window.valueChange, CC_MIC2_CH, CC_MAIN_FADER_PAR))
    #ui.Mic2.setProperty("value", CC_0127_DEFAULT)
    ui.Mic2.setProperty("channel", CC_MIC2_CH)
    ui.Mic2.setProperty("parameter", CC_MAIN_FADER_PAR)
    
    # Setting Up the Mic2 Pan Dial
    ui.Mic2Pan.valueChanged.connect(ui.Mic2PanLcd.display)
    ui.Mic2Pan.valueChanged.connect(functools.partial(window.valueChange, CC_MIC2_CH, CC_PAN_PAR))
    #ui.Mic2Pan.setProperty("value", CC_0127_DEFAULT)
    ui.Mic2Pan.setProperty("channel", CC_MIC2_CH)
    ui.Mic2Pan.setProperty("parameter", CC_PAN_PAR)
    
    # Setting Up the Mic2 Solo Button ** THEY CAN BE ONLY ONE SOLO CHECKED, THUS... **
    
    # *************** WAVE1 *********************
    
    # Setting up the Wave1 Fader
    ui.Wave1.valueChanged.connect(ui.Wave1Lcd.display)
    ui.Wave1.valueChanged.connect(functools.partial(window.valueChange, CC_WAVE1_CH, CC_MAIN_FADER_PAR))
    #ui.Wave1.setProperty("value", CC_0127_DEFAULT)
    ui.Wave1.setProperty("channel", CC_WAVE1_CH)
    ui.Wave1.setProperty("parameter", CC_MAIN_FADER_PAR)
    
    # Setting Up the Wave1 Solo Button ** THEY CAN BE ONLY ONE SOLO CHECKED, THUS... **
    
    # *************** WAVE2 *********************
    
    # Setting up the Wave1 Fader
    ui.Wave2.valueChanged.connect(ui.Wave2Lcd.display)
    ui.Wave2.valueChanged.connect(functools.partial(window.valueChange, CC_WAVE2_CH, CC_MAIN_FADER_PAR))
    #ui.Wave2.setProperty("value", CC_0127_DEFAULT)
    ui.Wave2.setProperty("channel", CC_WAVE2_CH)
    ui.Wave2.setProperty("parameter", CC_MAIN_FADER_PAR)    
    
    # Setting Up the Wave2 Solo Button ** THEY CAN BE ONLY ONE SOLO CHECKED, THUS... **
    
    # *************** MASTERLINE *********************
    
    # Setting Up the MasterLine Fader
    ui.MasterLine.valueChanged.connect(ui.MasterLineLcd.display)
    ui.MasterLine.valueChanged.connect(functools.partial(window.valueChange, CC_LINE_MASTER_CH, CC_MAIN_FADER_PAR))
    #ui.MasterLine.setProperty("value", CC_0127_DEFAULT)
    ui.MasterLine.setProperty("channel", CC_LINE_MASTER_CH)
    ui.MasterLine.setProperty("parameter", CC_MAIN_FADER_PAR)

def resetMixer(ui,window):
    '''
    Reset all mixer values to average ones.
    ***************************************
    A better idea could be to retrieve the current values (with sysex messages) and use them...
    maybe in the future
    ***************************************
    '''
    ui.MasterLine.setProperty("value", CC_0127_DEFAULT)
    ui.Wave1.setProperty("value", CC_0127_DEFAULT)
    ui.Wave2.setProperty("value", CC_0127_DEFAULT)
    ui.Mic1.setProperty("value", CC_0127_DEFAULT)
    ui.Mic1Pan.setProperty("value", CC_0127_DEFAULT)
    ui.Mic2.setProperty("value", CC_0127_DEFAULT)
    ui.Mic2Pan.setProperty("value", CC_0127_DEFAULT)

def actualMidiDevices():
    '''
    This should enumerate the devices to (later on) give then the possibility to choose one or guess the right one
    Returns a dictionary with tuples like 
    
    midiDevs = { 0: (tuple), 1: (tuple), ... }
    
    where the tuple is in the format:
    
    *add example here*
    
    '''
    # Count the MIDI devices connected
    numDevs = pm.get_count()
    # Initialize the device dictionary
    # midiDevs = { 0: (tuple), 1: (tuple), ... }
    #
    midiDevs = {}
    for dev in range(0,numDevs):
        # the portmidi get_device_info() returns a tuple
        midiDevs[dev]=pm.get_device_info(dev)
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
                print 'Trovato! Il controller e il device ',i, ', ovvero ',midiDevs[i][1]
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
    
def main(): 
    '''
    it already needs a big clean-up. *Andiamo bene...*
    
    '''
    # **************************** MIDI PART: could it go somewhere else? **********************************************
    
    # initialize the portmidi interface
    pm.init()
    
    # get the list of the Midi Devices according to portmidy
    midiDevs=actualMidiDevices()
    
    if (DEBUG_MODE == 1):
        print 'MIDI DEVICES FOUND: ',len(midiDevs),'. They are: ', midiDevs
        
    # guess the right midi device
    UA100CONTROL = rightMidiDevice(midiDevs)
    
    if (DEBUG_MODE == 1):
        print 'UA100CONTROL = ',UA100CONTROL

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
    
    # Add custom slot to the mixerMainWindow instance
    mixerMainWindow.valueChange = valueChange
    
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
            print 'Bye.'
        sys.exit()
    
    # first, open the selected device
    pm_open(UA100CONTROL)
    
    # then set up the mixer
    setupMixer(ui,mixerMainWindow)
    # and reset it to "mean" values
    resetMixer(ui,mixerMainWindow)
    
    # let the drums roll! We are now ready to show the mixer!
    mixerMainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

