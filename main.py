import sys
import os
import pyportmidi as pm
from PyQt4 import QtGui, QtCore
from main_ui import *
from main_ui_setup import *
from device_sel_ui import *
from types import MethodType
import functools

# Defining costants (taken from UA-100 documentation)

# Control Change Messages (for the Mixer part) - SysEx messages will be implemented later on (maybe)

# Control Change *CHANNELS*
CC_MIC1_CH = 0xb0
CC_MIC2_CH = 0xb1
CC_WAVE1_CH = 0xb2
CC_WAVE2_CH = 0xb3
CC_SYSRET_CH = 0xb4
CC_SYSSUB_CH = 0xb5
CC_WAVEREC_CH = 0xbE
CC_LINE_MASTER_CH = 0xBF

# Control Change *PARAMETERS* 
CC_MICLINESELECTOR_PAR = 21 # 0x15
CC_PAN_PAR = 10 # 0x0A - 0 - 64 - 127 (LEFT - CENTER - RIGHT)
CC_SEND1_PAR = 16 # 0x10
CC_SEND2_PAR = 17 # 0x11
CC_MUTE_PAR = 18 # 0x12
CC_SOLO_PAR = 19 # 0x13
CC_SUB_FADER_PAR = 20 # 0x14
CC_MAIN_FADER_PAR = 7 # 0x70
CC_SELECTOR_PAR = 22 # 0x16
CC_EFFECTSWITHC_PAR = 23 # 0x23

# Control Change Setting range

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


CC_0127_DEFAULT = 64 # I think 'in media stat virtus'

# DEBUG MODE CONTROL
# 1: true
# 0: false

DEBUG_MODE = 1

def pm_open(device):
    '''
    Possibly not the best solution.
    '''
    global pmout
    pmout = pm.midi.Output(device)

@QtCore.pyqtSlot()
def valueChange(a,b,val):
    '''
    I had to create a custom slot to connect to the changes in the interface. Hope it's the right way.
    '''
    global pmout
    
    pmout.write_short(a,b,val)
    
    if (DEBUG_MODE == 1):
        print hex(a),b,val

@QtCore.pyqtSlot()
def updateDeviceLabels(ui, midiDevs, indice):
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
    
    if (DEBUG_MODE == 1):
        print midiDevs[indice][2], midiDevs[indice][3]

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

def setupDevicesList(ui,window,midiDevs,UA100CONTROL):
    '''
    Sets up the ComboBox with a list of MIDI devices. Not that the combo box must be connected: at the moment it is not.
    '''
    for i in range(0,len(midiDevs)):
        ui.outputDevicesList.addItem(str(midiDevs[i]), i)
    
    ui.outputDevicesList.currentIndexChanged.connect(functools.partial(window.updateDeviceLabels, ui, midiDevs))
    
    ui.outputDevicesList.setCurrentIndex(UA100CONTROL)

def resetMixer(ui,window):
    '''
    Reset all mixer values to average ones.
    '''
    ui.MasterLine.setProperty("value", CC_0127_DEFAULT)
    ui.Wave1.setProperty("value", CC_0127_DEFAULT)
    ui.Wave2.setProperty("value", CC_0127_DEFAULT)
    ui.Mic1.setProperty("value", CC_0127_DEFAULT)
    ui.Mic1Pan.setProperty("value", CC_0127_DEFAULT)
    ui.Mic2.setProperty("value", CC_0127_DEFAULT)
    ui.Mic2Pan.setProperty("value", CC_0127_DEFAULT)

def setupSelectorDialog(ui,window):
    ui.dialogOK.clicked.connect(window.close)

def main(): 
    '''
    it already needs a big clean-up. *Andiamo bene...*
    
    '''
    # **************************** MIDI PART: could it go somewhere else? **********************************************
    pm.init()
    midiDevs=actualMidiDevices()
    if (DEBUG_MODE == 1):
        print 'MIDI DEVICES FOUND: ',len(midiDevs),'. They are: ', midiDevs
        
    UA100CONTROL = rightMidiDevice(midiDevs)
    
    pm_open(UA100CONTROL)
    # *******************************************************************************************************************

    app = QtGui.QApplication(sys.argv)
    
    # Showing the device selection dialog to select the midi device to use for the UA-100 controller
    # Actually, given the right portmidi API, the correct one should be automatically guessed.
    dialog= QtGui.QDialog()
    selector = Ui_deviceSelection()
    selector.setupUi(dialog)
    setupSelectorDialog(selector,dialog)
    dialog.updateDeviceLabels = updateDeviceLabels
    
    mixerMainWindow = QtGui.QMainWindow()
    
    # Add custom slot to the mixerMainWindow instance
    mixerMainWindow.valueChange = valueChange
    
    # inizializing the UI inside the mixerMainWindow
    ui = Ui_MainWindow()
    ui.setupUi(mixerMainWindow)
    
    # Changing the device in the device list ACTUALLY DOES NOT WORK!
    # **************************************************************
    setupDevicesList(selector,dialog,midiDevs,UA100CONTROL)
    # **************************************************************
    
    setupMixer(ui,mixerMainWindow)
    resetMixer(ui,mixerMainWindow)
    
    mixerMainWindow.show()
    dialog.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

