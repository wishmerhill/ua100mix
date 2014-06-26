import sys
import os
import pyportmidi as pm
from PyQt4 import QtGui, QtCore
from main_ui import *
from types import MethodType
import functools

CC_MIC1_CH = 0xb0
CC_MIC2_CH = 0xb1
CC_WAVE1_CH = 0xb2
CC_WAVE2_CH = 0xb3
CC_LINE_MASTER_CH = 0xBF

CC_PAN_PAR = 10
CC_SUB_FADER_PAR = 20
CC_MAIN_FADER_PAR = 7




CC_0127_DEFAULT = 64


def pm_init(device):
    pm.init()
    global pmout
    pmout = pm.midi.Output(device)
    #pmout.write_short(0xBF,7,60)

@QtCore.pyqtSlot()
def valueChange(a,b,val):
    global pmout
    #pmout.write_short(0xBF,7,volume)
    pmout.write_short(a,b,val)
    print hex(a),b,val

def setupMixer(ui,window):
    # Setting Up the MasterLine Fader
    ui.MasterLine.valueChanged.connect(ui.MasterLineLcd.display)
    ui.MasterLine.valueChanged.connect(functools.partial(window.valueChange, CC_LINE_MASTER_CH, CC_MAIN_FADER_PAR))
    #ui.MasterLine.setProperty("value", CC_0127_DEFAULT)
    ui.MasterLine.setProperty("channel", CC_LINE_MASTER_CH)
    ui.MasterLine.setProperty("parameter", CC_MAIN_FADER_PAR)
    
    # Setting up the Wave1 Fader
    ui.Wave1.valueChanged.connect(ui.Wave1Lcd.display)
    ui.Wave1.valueChanged.connect(functools.partial(window.valueChange, CC_WAVE1_CH, CC_MAIN_FADER_PAR))
    #ui.Wave1.setProperty("value", CC_0127_DEFAULT)
    ui.Wave1.setProperty("channel", CC_WAVE1_CH)
    ui.Wave1.setProperty("parameter", CC_MAIN_FADER_PAR)
    
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
    
    

def resetMixer(ui,window):
     ui.MasterLine.setProperty("value", CC_0127_DEFAULT)
     ui.Wave1.setProperty("value", CC_0127_DEFAULT)
     ui.Mic1.setProperty("value", CC_0127_DEFAULT)
     ui.Mic1Pan.setProperty("value", CC_0127_DEFAULT)
     ui.Mic2.setProperty("value", CC_0127_DEFAULT)
     ui.Mic2Pan.setProperty("value", CC_0127_DEFAULT)

def main():
    pm_init(4) 
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    window.valueChange = valueChange
    ui = Ui_MainWindow()
    ui.setupUi(window)
    setupMixer(ui,window)
    resetMixer(ui,window)
    
    
    
    window.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()

