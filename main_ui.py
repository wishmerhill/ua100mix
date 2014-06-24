# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Wed Jun 25 01:10:08 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(629, 564)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.MasterLine = QtGui.QSlider(self.centralwidget)
        self.MasterLine.setGeometry(QtCore.QRect(60, 100, 23, 301))
        self.MasterLine.setMaximum(127)
        self.MasterLine.setProperty("value", 0)
        self.MasterLine.setOrientation(QtCore.Qt.Vertical)
        self.MasterLine.setProperty("channel", 0)
        self.MasterLine.setProperty("parameter", 0)
        self.MasterLine.setObjectName(_fromUtf8("MasterLine"))
        self.MasterLineLcd = QtGui.QLCDNumber(self.centralwidget)
        self.MasterLineLcd.setGeometry(QtCore.QRect(40, 60, 64, 23))
        self.MasterLineLcd.setObjectName(_fromUtf8("MasterLineLcd"))
        self.masterLabel = QtGui.QLabel(self.centralwidget)
        self.masterLabel.setGeometry(QtCore.QRect(20, 430, 111, 21))
        self.masterLabel.setStyleSheet(_fromUtf8(""))
        self.masterLabel.setObjectName(_fromUtf8("masterLabel"))
        self.wave1Label = QtGui.QLabel(self.centralwidget)
        self.wave1Label.setGeometry(QtCore.QRect(140, 430, 111, 21))
        self.wave1Label.setStyleSheet(_fromUtf8(""))
        self.wave1Label.setObjectName(_fromUtf8("wave1Label"))
        self.Wave1 = QtGui.QSlider(self.centralwidget)
        self.Wave1.setGeometry(QtCore.QRect(180, 100, 23, 301))
        self.Wave1.setMaximum(127)
        self.Wave1.setProperty("value", 0)
        self.Wave1.setOrientation(QtCore.Qt.Vertical)
        self.Wave1.setProperty("channel", 0)
        self.Wave1.setProperty("parameter", 0)
        self.Wave1.setObjectName(_fromUtf8("Wave1"))
        self.Wave1Lcd = QtGui.QLCDNumber(self.centralwidget)
        self.Wave1Lcd.setGeometry(QtCore.QRect(160, 60, 64, 23))
        self.Wave1Lcd.setObjectName(_fromUtf8("Wave1Lcd"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 629, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.masterLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">MASTER</span></p></body></html>", None))
        self.wave1Label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">WAVE1</span></p></body></html>", None))
        self.menuAbout.setTitle(_translate("MainWindow", "About", None))

