import sys
import os
import pyportmidi as pm
from PyQt4 import QtGui, QtCore
from global_constants import *
from main_ui import *
from main_ui_setup import *
from device_sel_ui import *
from types import MethodType
import functools

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
    midiDevsDialog= QtGui.QDialog()
    midiDevsDialog_ui = Ui_deviceSelection()
    midiDevsDialog_ui.setupUi(midiDevsDialog)
    setupSelectorDialog(midiDevsDialog_ui,midiDevsDialog)
    midiDevsDialog.updateDeviceLabels = updateDeviceLabels
    
    mixerMainWindow = QtGui.QMainWindow()
    
    # Add custom slot to the mixerMainWindow instance
    mixerMainWindow.valueChange = valueChange
    
    # inizializing the UI inside the mixerMainWindow
    ui = Ui_MainWindow()
    ui.setupUi(mixerMainWindow)
    
    # Changing the device in the device list ACTUALLY DOES NOT WORK!
    # **************************************************************
    setupDevicesList(midiDevsDialog_ui,midiDevsDialog,midiDevs,UA100CONTROL)
    # **************************************************************
    
    setupMixer(ui,mixerMainWindow)
    resetMixer(ui,mixerMainWindow)
    
    mixerMainWindow.show()
    midiDevsDialog.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

