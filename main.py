import sys
import os
import pyportmidi as pm
from PyQt4 import QtGui, QtCore
from main_ui import *
from types import MethodType
import functools

CC_LINE_MASTER_CH = 0xBF
CC_MAIN_FADER_PAR = 7
CC_SUB_FADER_PAR = 20
CC_0127_DEFAULT = 60
CC_WAVE1_CH = 0xb2


def pm_init(device):
    pm.init()
    global pmout
    pmout = pm.midi.Output(device)
    #pmout.write_short(0xBF,7,60)

@QtCore.pyqtSlot()
def volumeChange(a,b,val):
    global pmout
    #pmout.write_short(0xBF,7,volume)
    pmout.write_short(a,b,val)
    print hex(a),b,val
    
def main():
    pm_init(4) 
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    window.volumeChange = volumeChange
    ui = Ui_MainWindow()
    ui.setupUi(window)
    
    
    # Setting Up the MasterLine Fader
    ui.MasterLine.valueChanged.connect(ui.MasterLineLcd.display)
    ui.MasterLine.valueChanged.connect(functools.partial(window.volumeChange, CC_LINE_MASTER_CH, CC_MAIN_FADER_PAR))
    ui.MasterLine.setProperty("value", CC_0127_DEFAULT)
    ui.MasterLine.setProperty("channel", CC_LINE_MASTER_CH)
    ui.MasterLine.setProperty("parameter", CC_MAIN_FADER_PAR)
    
    
    ui.Wave1.valueChanged.connect(ui.Wave1Lcd.display)
    ui.Wave1.valueChanged.connect(functools.partial(window.volumeChange, CC_WAVE1_CH, CC_MAIN_FADER_PAR))
    ui.Wave1.setProperty("value", CC_0127_DEFAULT)
    ui.Wave1.setProperty("channel", CC_WAVE1_CH)
    ui.Wave1.setProperty("parameter", CC_MAIN_FADER_PAR)
    
    window.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()

