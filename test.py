# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created: Tue Aug 19 22:31:54 2014
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
        MainWindow.resize(726, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 211, 531))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.Mic1PanLcd = QtGui.QLCDNumber(self.groupBox)
        self.Mic1PanLcd.setObjectName(_fromUtf8("Mic1PanLcd"))
        self.verticalLayout.addWidget(self.Mic1PanLcd)
        self.Mic1Pan = QtGui.QDial(self.groupBox)
        self.Mic1Pan.setMaximum(127)
        self.Mic1Pan.setProperty("value", 0)
        self.Mic1Pan.setSliderPosition(0)
        self.Mic1Pan.setWrapping(False)
        self.Mic1Pan.setObjectName(_fromUtf8("Mic1Pan"))
        self.verticalLayout.addWidget(self.Mic1Pan)
        self.Mic1Fader = QtGui.QSlider(self.groupBox)
        self.Mic1Fader.setMaximum(127)
        self.Mic1Fader.setProperty("value", 0)
        self.Mic1Fader.setOrientation(QtCore.Qt.Vertical)
        self.Mic1Fader.setProperty("channel", 0)
        self.Mic1Fader.setProperty("parameter", 0)
        self.Mic1Fader.setObjectName(_fromUtf8("Mic1Fader"))
        self.verticalLayout.addWidget(self.Mic1Fader)
        self.mic1Solo = QtGui.QPushButton(self.groupBox)
        self.mic1Solo.setStyleSheet(_fromUtf8("QPushButton#mic1Solo:checked { background-color: red}"))
        self.mic1Solo.setCheckable(True)
        self.mic1Solo.setAutoExclusive(False)
        self.mic1Solo.setObjectName(_fromUtf8("mic1Solo"))
        self.verticalLayout.addWidget(self.mic1Solo)
        self.Mic1Lcd = QtGui.QLCDNumber(self.groupBox)
        self.Mic1Lcd.setObjectName(_fromUtf8("Mic1Lcd"))
        self.verticalLayout.addWidget(self.Mic1Lcd)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 726, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox.setTitle(_translate("MainWindow", "Mic1/Guitar", None))
        self.mic1Solo.setText(_translate("MainWindow", "Solo", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

