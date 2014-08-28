# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'device_sel.ui'
#
# Created: Thu Aug 28 09:04:53 2014
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_deviceSelection(object):
    def setupUi(self, deviceSelection):
        deviceSelection.setObjectName(_fromUtf8("deviceSelection"))
        deviceSelection.setWindowModality(QtCore.Qt.ApplicationModal)
        deviceSelection.resize(536, 175)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/Sound-Mixer-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        deviceSelection.setWindowIcon(icon)
        deviceSelection.setModal(True)
        self.outputDevicesList = QtGui.QComboBox(deviceSelection)
        self.outputDevicesList.setGeometry(QtCore.QRect(20, 30, 271, 23))
        self.outputDevicesList.setObjectName(_fromUtf8("outputDevicesList"))
        self.deviceIOLabel = QtGui.QLabel(deviceSelection)
        self.deviceIOLabel.setGeometry(QtCore.QRect(20, 100, 101, 16))
        self.deviceIOLabel.setObjectName(_fromUtf8("deviceIOLabel"))
        self.deviceNameText = QtGui.QLabel(deviceSelection)
        self.deviceNameText.setGeometry(QtCore.QRect(140, 80, 101, 16))
        self.deviceNameText.setObjectName(_fromUtf8("deviceNameText"))
        self.deviceIOText = QtGui.QLabel(deviceSelection)
        self.deviceIOText.setGeometry(QtCore.QRect(140, 100, 101, 16))
        self.deviceIOText.setObjectName(_fromUtf8("deviceIOText"))
        self.outputDevicesListLabel = QtGui.QLabel(deviceSelection)
        self.outputDevicesListLabel.setGeometry(QtCore.QRect(20, 10, 191, 16))
        self.outputDevicesListLabel.setObjectName(_fromUtf8("outputDevicesListLabel"))
        self.midiApiText = QtGui.QLabel(deviceSelection)
        self.midiApiText.setGeometry(QtCore.QRect(140, 60, 101, 16))
        self.midiApiText.setObjectName(_fromUtf8("midiApiText"))
        self.midiApiLabel = QtGui.QLabel(deviceSelection)
        self.midiApiLabel.setGeometry(QtCore.QRect(20, 60, 57, 14))
        self.midiApiLabel.setObjectName(_fromUtf8("midiApiLabel"))
        self.deviceNameLabel = QtGui.QLabel(deviceSelection)
        self.deviceNameLabel.setGeometry(QtCore.QRect(20, 80, 101, 16))
        self.deviceNameLabel.setObjectName(_fromUtf8("deviceNameLabel"))
        self.layoutWidget = QtGui.QWidget(deviceSelection)
        self.layoutWidget.setGeometry(QtCore.QRect(320, 130, 211, 31))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.dialogQuit = QtGui.QPushButton(self.layoutWidget)
        self.dialogQuit.setObjectName(_fromUtf8("dialogQuit"))
        self.horizontalLayout.addWidget(self.dialogQuit)
        self.dialogOK = QtGui.QPushButton(self.layoutWidget)
        self.dialogOK.setObjectName(_fromUtf8("dialogOK"))
        self.horizontalLayout.addWidget(self.dialogOK)
        self.reccomendedLabel = QtGui.QLabel(deviceSelection)
        self.reccomendedLabel.setGeometry(QtCore.QRect(300, 20, 221, 31))
        self.reccomendedLabel.setText(_fromUtf8(""))
        self.reccomendedLabel.setObjectName(_fromUtf8("reccomendedLabel"))

        self.retranslateUi(deviceSelection)
        QtCore.QMetaObject.connectSlotsByName(deviceSelection)

    def retranslateUi(self, deviceSelection):
        deviceSelection.setWindowTitle(_translate("deviceSelection", "Select device", None))
        self.deviceIOLabel.setText(_translate("deviceSelection", "Device I/O", None))
        self.deviceNameText.setText(_translate("deviceSelection", "NO DEVICE", None))
        self.deviceIOText.setText(_translate("deviceSelection", "N/A", None))
        self.outputDevicesListLabel.setText(_translate("deviceSelection", "Control Change Device:", None))
        self.midiApiText.setText(_translate("deviceSelection", "NO API", None))
        self.midiApiLabel.setText(_translate("deviceSelection", "MIDI API:", None))
        self.deviceNameLabel.setText(_translate("deviceSelection", "Device Name", None))
        self.dialogQuit.setText(_translate("deviceSelection", "Quit", None))
        self.dialogOK.setText(_translate("deviceSelection", "OK", None))

