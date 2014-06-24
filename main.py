import sys
import os
import pyportmidi as pm
from PyQt4 import QtGui, QtCore
from main_ui import *
from types import MethodType

def pm_init(device):
    pm.init()
    global pmout
    pmout = pm.midi.Output(device)
    pmout.write_short(0xBF,7,60)

@QtCore.pyqtSlot()
def volumeChange(a,b,val):
    global pmout
    #pmout.write_short(0xBF,7,volume)
    pmout.write_short(0xBF,7,val)
    print hex(a),b,val
    


@QtCore.pyqtSlot()
def mute(stato):
    global pmout
    if (stato == true):
        pmout.write_short(0xBF,18,1)
    else:
        pmout.write_short(0xBF,10,0)


def main():
    pm_init(4) 
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    window.volumeChange = volumeChange
    ui = Ui_MainWindow()
    ui.setupUi(window)
    ui.MasterLine.setProperty("value", 60)
    ui.MasterLine.setProperty("channel", 0xBF)
    ui.MasterLine.setProperty("parameter", 7)
    #portmidi init
    #QtCore.QObject.connect(ui.MasterLine, QtCore.SIGNAL("valueChanged(int)"), ui.MasterLineLcd.display)
    #QtCore.QObject.connect(ui.MasterLine, QtCore.SIGNAL("valueChanged(int)"), functools.partial(window.volumeChange, 0xBF,7))
    #QtCore.QMetaObject.connectSlotsByName(window)
    ui.MasterLine.valueChanged.connect(ui.MasterLineLcd.display)
    ui.MasterLine.valueChanged.connect(functools.partial(window.volumeChange, 0xBF,7))
    
    window.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()

