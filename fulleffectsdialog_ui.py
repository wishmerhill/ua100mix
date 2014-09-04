# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fulleffectsdialog.ui'
#
# Created: Tue Sep  2 23:52:06 2014
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

class Ui_FullEffectsDialog(object):
    def setupUi(self, FullEffectsDialog):
        FullEffectsDialog.setObjectName(_fromUtf8("FullEffectsDialog"))
        FullEffectsDialog.resize(421, 378)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/Sound-Mixer-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FullEffectsDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(FullEffectsDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.EffectTypeList = QtGui.QComboBox(FullEffectsDialog)
        self.EffectTypeList.setObjectName(_fromUtf8("EffectTypeList"))
        self.gridLayout.addWidget(self.EffectTypeList, 1, 2, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(FullEffectsDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.treeWidget = QtGui.QTreeWidget(FullEffectsDialog)
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.gridLayout.addWidget(self.treeWidget, 2, 2, 1, 1)
        self.plainTextEdit = QtGui.QPlainTextEdit(FullEffectsDialog)
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.gridLayout.addWidget(self.plainTextEdit, 3, 2, 1, 1)
        self.label_2 = QtGui.QLabel(FullEffectsDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.checkBox = QtGui.QCheckBox(FullEffectsDialog)
        self.checkBox.setText(_fromUtf8(""))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 2, 1, 1, 1)
        self.pushButton = QtGui.QPushButton(FullEffectsDialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 1)

        self.retranslateUi(FullEffectsDialog)
        QtCore.QMetaObject.connectSlotsByName(FullEffectsDialog)
        
        print self.sender()

    def retranslateUi(self, FullEffectsDialog):
        FullEffectsDialog.setWindowTitle(_translate("FullEffectsDialog", "Full Effects", None))
        self.label.setText(_translate("FullEffectsDialog", "Effect On/Off", None))
        self.treeWidget.headerItem().setText(0, _translate("FullEffectsDialog", "Parameter", None))
        self.treeWidget.headerItem().setText(1, _translate("FullEffectsDialog", "Value", None))
        self.label_2.setText(_translate("FullEffectsDialog", "Effect Type", None))
        self.pushButton.setText(_translate("FullEffectsDialog", "PushButton", None))

