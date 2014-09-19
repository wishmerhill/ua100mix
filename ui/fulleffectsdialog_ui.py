# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fulleffectsdialog.ui'
#
# Created: Sun Sep  7 23:33:08 2014
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
        FullEffectsDialog.resize(331, 382)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/Sound-Mixer-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FullEffectsDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(FullEffectsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.EffTypeLabel = QtGui.QLabel(FullEffectsDialog)
        self.EffTypeLabel.setObjectName(_fromUtf8("EffTypeLabel"))
        self.verticalLayout.addWidget(self.EffTypeLabel)
        self.EffectTypeList = QtGui.QComboBox(FullEffectsDialog)
        self.EffectTypeList.setObjectName(_fromUtf8("EffectTypeList"))
        self.verticalLayout.addWidget(self.EffectTypeList)
        self.EffectParameters = QtGui.QTreeWidget(FullEffectsDialog)
        self.EffectParameters.setRootIsDecorated(False)
        self.EffectParameters.setItemsExpandable(False)
        self.EffectParameters.setExpandsOnDoubleClick(False)
        self.EffectParameters.setColumnCount(3)
        self.EffectParameters.setObjectName(_fromUtf8("EffectParameters"))
        item_0 = QtGui.QTreeWidgetItem(self.EffectParameters)
        self.verticalLayout.addWidget(self.EffectParameters)
        self.EffectDesc = QtGui.QPlainTextEdit(FullEffectsDialog)
        self.EffectDesc.setEnabled(False)
        self.EffectDesc.setObjectName(_fromUtf8("EffectDesc"))
        self.verticalLayout.addWidget(self.EffectDesc)
        self.ToggleEffect = QtGui.QPushButton(FullEffectsDialog)
        self.ToggleEffect.setCheckable(True)
        self.ToggleEffect.setObjectName(_fromUtf8("ToggleEffect"))
        self.verticalLayout.addWidget(self.ToggleEffect)

        self.retranslateUi(FullEffectsDialog)
        QtCore.QMetaObject.connectSlotsByName(FullEffectsDialog)

    def retranslateUi(self, FullEffectsDialog):
        FullEffectsDialog.setWindowTitle(_translate("FullEffectsDialog", "Full Effects", None))
        self.EffTypeLabel.setText(_translate("FullEffectsDialog", "Effect Type", None))
        self.EffectParameters.headerItem().setText(0, _translate("FullEffectsDialog", "Parameter", None))
        self.EffectParameters.headerItem().setText(1, _translate("FullEffectsDialog", "Value", None))
        self.EffectParameters.headerItem().setText(2, _translate("FullEffectsDialog", "Setting Values", None))
        __sortingEnabled = self.EffectParameters.isSortingEnabled()
        self.EffectParameters.setSortingEnabled(False)
        self.EffectParameters.topLevelItem(0).setText(0, _translate("FullEffectsDialog", "pippo", None))
        self.EffectParameters.topLevelItem(0).setText(1, _translate("FullEffectsDialog", "pluto", None))
        self.EffectParameters.setSortingEnabled(__sortingEnabled)
        self.ToggleEffect.setText(_translate("FullEffectsDialog", "Set Effect", None))

