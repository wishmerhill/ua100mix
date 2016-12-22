#!/usr/bin/python ~devel/ua100mix/main.py

"""
ua100mix is just a try for creating a tool to control the Roland/Edirol UA-100,
an USB Audio & MIDI processing Unit.
"""

# define authorship information
__authors__ = ['Alberto "wishmehill" Azzalini']
__author__ = ','.join(__authors__)
__credits__ = []
__copyright__ = 'Copyright (c) 2014'
__license__ = 'GPL'

# maintanence information
__maintainer__ = 'Alberto Azzalini'
__email__ = 'alberto.azzalini@gmail.com'

# ********************************
# ***** DEBUG MODE CONTROL *******
# SET:
# 1: debug messages on stdout ON
# 0: debug messages on stdout OFF

# DEBUG_MODE = 1

# Let's get rid of DEBUG_MODE and move to the more professional logging!
# From now on, DEBUG_MODE is DEPRECATED!
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('Starting the us100mix')



# ********************************
# ***** UA MODE CONTROL **********
#
# SET:
#      0: No UA-100 present, for test purposes on other machines
#      1: UA-100 present and working
# NOTE: Could (and will) be automatically set to 0 if no UA-100 is found.
#       The UA-100 discovery routine is based on WHAT? - ****
#

REAL_UA_MODE = 1
logger.info('Setting REAL_UA_MODE to %s', REAL_UA_MODE )

logger.info('Importing the required modules')
import sys
import functools

import numpy as np

try:
    import mido
    import rtmidi
except ImportError:
    logger.warning('*** Warning *** mido and/or rtmidi not found - Switching to testing mode (REAL_UA_MODE = 0) ***')
    REAL_UA_MODE = 0
import PyQt4.uic
from PyQt4 import QtGui
# from PyQt4 import QtCore
# from types import MethodType
import signal
import time


from res.parameters import *

np.set_printoptions(formatter={'int': hex})

# Defining constants (taken from UA-100 documentation)
# and copying some useful documentation excerts

logger.info('Reading some MANY constants...')


# More documentation (*stolen* from michel minn's web page http://michaelminn.com/linux/mmusbaudio/)

# A listing of the UA-100 SYSEX messages (derived from Roland's documentation) is given below:
#
# Data Transmission
#
# 	F0: Start SysEx
# 	41: Manufacturer (Roland)
# 	10: Device ID
# 	00: Model ID 1
# 	11: Model ID 2
# 	12: Command (Transmit data)
# 	aa: Address
# 	aa
#     aa:
#     aa:
# 	dd: Data
# 	dd:
#     ck: checksum = 128 - ((sum of address & data bytes) & 0x3f);
# 	f7: end of SysEx
#
#     Examples: F0 41 10 00 11 12   00 40 02 00   01 00  3D F7
#               (select Stereo-EQ as Mic2 insertion effect)
#
#               f0 41 10 00 11 12   00 40 50 03   64     09 f7
#               (master level of 64)
#
# In URB buffer, the message is split into 3 byte chunks with
# a 24h is placed before every chunk except for a  25h before the
# final chunk.
#
#     24 f0 41 10    24 00 11 12   24 00 40 02   24 00 01 00   25 f7
#
# Note that for messages with multiple data bytes (length > 1),
# the first data byte (usually the significant one) comes first.
#
#
# ------------------------------------------------------------------------
# 00 40 00 00  01      PC Mode (VT Effect Mode) - sent by UA-100?
# 00 40 00 00  03      PC Mode (Compact Effect Mode)
# 00 40 00 00  04      PC Mode (Full Effect Mode)
# 00 40 00 00  05      VT Mode
# 00 40 00 00  06      Vocal Mode
# 00 40 00 00  07      Guitar Mode
# 00 40 00 00  08      GAME Mode
# 00 40 00 00  09      BYPASS Mode
#
# 00 40 00 01  0x      Copyright (0 off, 1 on)
#
#     n = 1 (line, mic1, mic1+2), 2 (mic2), 3 (wave1), 4 (wave2), 5 (sys effect 1), 6 (sys effect 2)
#
# 00 40 0n 00  xx 00   Effect type (listed below)
# 00 40 0n 03  xx      Effect parameter 1
# 00 40 0n 04  xx      Effect parameter 2
# 00 40 0n 05  xx      Effect parameter 3
# 00 40 0n 06  xx      Effect parameter 4
# 00 40 0n 07  xx      Effect parameter 5
# 00 40 0n 08  xx      Effect parameter 6
# 00 40 0n 09  xx      Effect parameter 7
# 00 40 0n 0A  xx      Effect parameter 8
# 00 40 0n 0B  xx      Effect parameter 9
# 00 40 0n 0C  xx      Effect parameter 10
# 00 40 0n 0D  xx      Effect parameter 11
# 00 40 0n 0E  xx      Effect parameter 12
# 00 40 0n 0F  xx      Effect parameter 13
# 00 40 0n 10  xx      Effect parameter 14
# 00 40 0n 11  xx      Effect parameter 15
# 00 40 0n 12  xx      Effect parameter 16
# 00 40 0n 13  xx      Effect parameter 17
# 00 40 0n 14  xx      Effect parameter 18
# 00 40 0n 15  xx      Effect parameter 19
# 00 40 0n 16  xx      Effect parameter 20
# 00 40 0n 17  xx      Effect parameter 21
# 00 40 0n 18  xx      Effect parameter 22
# 00 40 0n 19  xx      Effect parameter 23
# 00 40 0n 1A  xx      Effect parameter 24
# 00 40 0n 1B  xx      Effect parameter 25
# 00 40 0n 1C  xx      Effect parameter 26
# 00 40 0n 1D  xx      Effect parameter 27
# 00 40 0n 1E  xx      Effect parameter 28
# 00 40 0n 1F  xx      Effect parameter 29
# 00 40 0n 20  xx      Effect parameter 30
# 00 40 0n 21  xx      Effect parameter 31
# 00 40 0n 22  xx      Effect parameter 32
# 00 40 0n 23  xx      Effect parameter 33
# 00 40 0n 24  xx      Effect parameter 34
# 00 40 0n 25  xx      Effect parameter 35
# 00 40 0n 26  xx      Effect parameter 36
# 00 40 0n 27  xx      Effect parameter 37
# 00 40 0n 28  xx      Effect parameter 38
# 00 40 0n 29  xx      Effect parameter 39
# 00 40 0n 2A  xx      Effect parameter 40
#
# 00 40 10 00  00      Mic input mode
# 00 40 10 00  01      Line input mode
# 00 40 10 00  02      MIC1+MIC2 Mode (not in VT mode)
#
# 00 40 10 01  xx      Input pan 1 (0 - 40 - 7f)
# 00 40 10 02  xx      Input pan 2 (0 - 40 - 7f)
# 00 40 10 03  0x      Monitor (0 off, 1 on)
#
#     n = 1 (line, mic1, mic1+2), 2 (mic2), 3 (wave1), 4 (wave2), 5 (sys effect 1), 6 (sys effect 2)
#
# 00 40 1n 00  xx      Effect 1 send level (full/compact effect mode)
# 00 40 1n 02  xx      Effect 2 send level (full/compact effect mode)
# 00 40 1n 04  xx      Submaster send level (not in VT mode)
# 00 40 1n 05  xx      Fader level (not in VT mode)
# 00 40 1n 06  0x      Mute (0 off, 1 on)
# 00 40 1n 07  0x      Solo (0 off, 1 on)
#
# 00 40 40 00  01      VT effect mode
# 00 40 40 00  03      Compact effect mode (1 insertion + 2 system effects)
# 00 40 40 00  04      Full effect mode (1 effect)
# 00 40 40 01  0x      Line/Mic1/Mic1+2 insertion effect on/off (0 off, 1 on)
# 00 40 40 02  0x      Mic2 insertion effect on/off (0 off, 1 on)
# 00 40 40 03  0x      Wave1 insertion effect on/off (0 off, 1 on)
# 00 40 40 04  0x      Wave2 insertion effect on/off (0 off, 1 on)
# 00 40 40 05  0x      System effect 1 on/off (0 off, 1 on)
# 00 40 40 06  0x      System effect 2 on/off (0 off, 1 on)
#
# 00 40 40 07  xx      Effect 1 master return
# 00 40 40 08  xx      Effect 1 submaster return
# 00 40 40 09  xx      Effect 2 master return
# 00 40 40 0A  xx      Effect 2 submaster return
#
# 00 40 40 0B  0x      Vocal Transform 1 receive channel (0 - F)
# 00 40 40 0C  0x      Vocal Transform 1 note enabled (0 off, 1 on)
# 00 40 40 0D  0x      Vocal Transform 1 bend enabled (0 off, 1 on)
# 00 40 40 0E  0x      Vocal Transform 2 receive channel (0 - F)
# 00 40 40 0F  0x      Vocal Transform 2 note enabled (0 off, 1 on)
# 00 40 40 10  0x      Vocal Transform 2 bend enabled (0 off, 1 on)
#
# 00 40 50 00  0x      Record source (Mixer: 0 line/mic, 1 mic2, 2 wave1, 3 wave2,
# 				    4-7 ch 1-4, 8 submaster, 9 master)
#                                    (VT: 0 line/mic, 1 mic3, 2 wave1, 3 wave2, 4 VT-out, 5 master)
# 00 40 50 01  0x      Output (see record source)
# 00 40 50 02  xx      Recording level
# 00 40 50 03  xx      Master level
#
#
#       n  = 0 (Voice Transformer), 1 (Vocal), 2 (Guitar), 3 (Game) (NOT FOR PC MODE)
#
# 00 40 6n 00  xx      Preset effect parameter 1 (0 - 39)
# 00 40 6n 01  xx      Preset effect parameter 2 (0 - 39)
# 00 40 6n 02  xx      Preset effect parameter 3 (0 - 39)
# 00 40 6n 03  xx      Preset effect parameter 4 (0 - 39)
#
# 00 40 6n 04  xx      Preset effect default Value 1 (0 - 127)
# 00 40 6n 05  xx      Preset effect default Value 2 (0 - 127)
# 00 40 6n 06  xx      Preset effect default Value 3 (0 - 127)
# 00 40 6n 07  xx      Preset effect default Value 4 (0 - 127)
# 00 40 6n 08  xx      Preset effect default Value 5 (0 - 127)
# 00 40 6n 09  xx      Preset effect default Value 6 (0 - 127)
# 00 40 6n 0A  xx      Preset effect default Value 7 (0 - 127)
# 00 40 6n 0B  xx      Preset effect default Value 8 (0 - 127)
# 00 40 6n 0C  xx      Preset effect default Value 9 (0 - 127)
# 00 40 6n 0D  xx      Preset effect default Value 10 (0 - 127)
# 00 40 6n 0E  xx      Preset effect default Value 11 (0 - 127)
# 00 40 6n 0F  xx      Preset effect default Value 12 (0 - 127)
#
# 00 40 6n 10  xx      Preset effect default Value 13 (0 - 127)
# 00 40 6n 11  xx      Preset effect default Value 14 (0 - 127)
# 00 40 6n 12  xx      Preset effect default Value 15 (0 - 127)
# 00 40 6n 13  xx      Preset effect default Value 16 (0 - 127)
# 00 40 6n 14  xx      Preset effect default Value 17 (0 - 127)
# 00 40 6n 15  xx      Preset effect default Value 18 (0 - 127)
# 00 40 6n 16  xx      Preset effect default Value 19 (0 - 127)
# 00 40 6n 17  xx      Preset effect default Value 20 (0 - 127)
# 00 40 6n 18  xx      Preset effect default Value 21 (0 - 127)
# 00 40 6n 19  xx      Preset effect default Value 22 (0 - 127)
# 00 40 6n 1A  xx      Preset effect default Value 23 (0 - 127)
# 00 40 6n 1B  xx      Preset effect default Value 24 (0 - 127)
# 00 40 6n 1C  xx      Preset effect default Value 25 (0 - 127)
# 00 40 6n 1D  xx      Preset effect default Value 26 (0 - 127)
# 00 40 6n 1E  xx      Preset effect default Value 27 (0 - 127)
# 00 40 6n 1F  xx      Preset effect default Value 28 (0 - 127)
# 00 40 6n 20  xx      Preset effect default Value 29 (0 - 127)
# 00 40 6n 21  xx      Preset effect default Value 30 (0 - 127)
# 00 40 6n 22  xx      Preset effect default Value 31 (0 - 127)
# 00 40 6n 23  xx      Preset effect default Value 32 (0 - 127)
# 00 40 6n 24  xx      Preset effect default Value 33 (0 - 127)
# 00 40 6n 25  xx      Preset effect default Value 34 (0 - 127)
# 00 40 6n 26  xx      Preset effect default Value 35 (0 - 127)
# 00 40 6n 27  xx      Preset effect default Value 36 (0 - 127)
# 00 40 6n 28  xx      Preset effect default Value 37 (0 - 127)
# 00 40 6n 29  xx      Preset effect default Value 38 (0 - 127)
# 00 40 6n 2A  xx      Preset effect default Value 39 (0 - 127)
# 00 40 6n 2B  xx      Preset effect default Value 40 (0 - 127)
#
# 00 40 60 7F  00      Preset effect parameter write
#
#
# ---------------------------------------------------------
#
# System Effect 1
#
# 	0021: Delay
# 	0022: Chorus
#
# System Effect 2
#
# 	0031: Delay
# 	0032: Reverb
#
# Full Effects
# 	0011: High Quality Reverb
# 	0012: Mic Simulator
# 	0013: Vocoder
# 	0014: Vocal Multi
# 	0016: Game with 3D Reverb
# 	0300: Rotary Multi (same parameters as insertion #47)
# 	0400: Guitar Multi 1 (same parameters as insertion #48)
# 	0401: Guitar Multi 2 (same parameters as insertion #49)
# 	0402: Guitar Multi 3 (same parameters as insertion #50)
# 	0403: Clean Guitar Multi 1 (same parameters as insertion #51)
# 	0404: Clean Guitar Multi 2 (same parameters as insertion #52)
# 	0405: Bass Multi (same parameters as insertion #53)
# 	0406: Electric Piano Multi (same parameters as insertion #54)
# 	0500: Keyboard Multi ( (same parameters as insertion #55)
#
# Insertion Effects
# 	0000: (00) Noise Suppressor
# 	0100: (01) Stereo Equalizer
# 	0101: (02) Spectrum
# 	0102: (03) Enhancer
# 	0103: (04) Humanizer
# 	0110: (05) Overdrive
# 	0111: (06) Distortion
# 	0120: (07) Phaser
# 	0121: (08) Auto Wah
# 	0122: (09) Rotary
# 	0123: (10) Stereo Flanger
# 	0124: (11) Step Flanger
# 	0125: (12) Tremolo
# 	0126: (13) Auto Pan
# 	0130: (14) Compressor
# 	0131: (15) Limiter
# 	0140: (16) Hexa Chorus
# 	0141: (17) Tremolo Chorus
# 	0142: (18) Stereo Chorus
# 	0143: (19) Space D
# 	0144: (20) 3D Chorus
# 	0150: (21) Stereo Delay
# 	0151: (22) Modulation Delay
# 	0152: (23) 3 Tap Delay
# 	0153: (24) 4 Tap Delay
# 	0154: (25) Time Control Delay
# 	0155: (26) Reverb
# 	0156: (27) Gate Reverb
# 	0157: (28) 3D Delay
# 	0160: (29) 2-voice Pitch Shifter
# 	0161: (30) Feedback Pitch Shifter
# 	0170: (31) 3D Auto
# 	0171: (32) 3D Manual
# 	0172: (33) Lo-Fi 1
# 	0173: (34) Lo-Fi 2
# 	0200: (35) Overdrive/Chorus
# 	0201: (36) Overdrive/Flanger
# 	0202: (37) Overdrive/Delay
# 	0203: (38) Distortion/Chorus
# 	0204: (39) Distortion/Flanger
# 	0205: (40) Distortion/Delay
# 	0206: (41) Enhancer/Chorus
# 	0207: (42) Enhancer/Flanger
# 	0208: (43) Enhancer/Delay
# 	0209: (44) Chorus/Delay
# 	020a: (45) Flanger/Delay
# 	020b: (46) Chorus/Flanger
# 	0300: (47) Rotary Multi
# 	0400: (48) Guitar Multi1
# 	0401: (49) Guitar Multi2
# 	0402: (50) Guitar Multi3
# 	0403: (51) Clean Guitar Multi1
# 	0404: (52) Clean Guitar Multi2
# 	0405: (53) Bass Multi
# 	0406: (54) E.Piano Multi
# 	0500: (55) Keyboard Multi
# 	1100: (56) Chorus/Delay
# 	1101: (57) Flanger/Delay
# 	1102: (58) Chorus/Flanger
# 	1103: (59) Overdrive/Distortion1,2
# 	1104: (60) Overdrive/Distortion/Rotary
# 	1105: (61) Overdrive/Distortion/Phaser
# 	1106: (62) Overdrive/Distortion/Auto-wah
# 	1107: (63) Phaser/Rotary
# 	1108: (64) Phaser/Auto-wah


logger.info('Done!')


class MidiDevsDialog(QtGui.QDialog):
    '''
    First of all, we ask for the right device to use. In fact, we know which one... and thus, we can easily guess.
    '''

    def __init__(self, parent=None):
        super(MidiDevsDialog, self).__init__(parent)

        self.ui = PyQt4.uic.loadUi('ui/device_sel.ui', self)

        logger.debug('midiDevs= %s', midiDevs)
        for i in range(0, len(midiDevs)):
            self.outputDevicesList.addItem(str(midiDevs[i]), i)

        # update the device information when selecting the devices in the combobox
        self.outputDevicesList.currentIndexChanged.connect(self.updateDeviceLabels)

        # call the setMidiDevice custom slot to tell everyone which one is the selected device (output)
        self.outputDevicesList.currentIndexChanged.connect(self.setMidiDevice)
        self.outputDevicesList.setCurrentIndex(-1)
        # send true if OK is clicked
        self.dialogOK.clicked.connect(self.accept)

        # send false if Quit is clicked (and close application)
        self.dialogQuit.clicked.connect(self.reject)

        # set the current index to the guessed right outpud midi device for the UA100 controller
        if (REAL_UA_MODE):
            self.outputDevicesList.setCurrentIndex(DEFAULT_UA100CONTROL)
            pass

    def updateDeviceLabels(self, index):
        '''
        I should be an easy task to update label according to a combo box...
        '''
        # self.midiApiText.setText(str(midiDevs[index][0]))
        # self.deviceNameText.setText(str(midiDevs[index][1]))
        # if (midiDevs[index][2] == 1 and midiDevs[index][3] == 0):
        #     self.deviceIOText.setText('INPUT')
        # elif (midiDevs[index][2] == 0 and midiDevs[index][3] == 1):
        #     self.deviceIOText.setText('OUTPUT')
        # else:
        #     self.deviceIOText.setText('N/A')
        # 
        if (index == DEFAULT_UA100CONTROL):
            self.reccomendedLabel.setText('RECCOMENDED!\r\nYou don\'t really want to change it!')
            self.reccomendedLabel.setStyleSheet('color: red; font-style: bold')
        else:
            self.reccomendedLabel.setText('')

    def setMidiDevice(self, index):
        '''
        This slot should set the midi device selected in the combo box of the starting dialog
        '''
        global UA100CONTROL

        UA100CONTROL = index
        logger.debug('Index = %s', index)
        if not (index == -1):
            logger.debug('UA100CONTROL = %s', midiDevs[UA100CONTROL])
        else:
            logger.debug('UA100CONTROL is not yet set!')


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # load the ui
        self.ui = PyQt4.uic.loadUi('ui/main.ui', self)

        # inizialize the dicts containing the definitions for the 3 effect dialog types
        self.fullEffects = {}
        self.compactEffectsSys = {}
        self.compactEffectsIns = {}

        # setup menus
        self.actionReset_Mixer.triggered.connect(self.resetMixer)
        self.actionQuit.triggered.connect(QtGui.qApp.quit)

        # *************** MIC1 *********************

        self.Mic1.setProperty("channel", CC_MIC1_CH)

        # Setting Up the Mic1 Fader
        self.Mic1Fader.valueChanged.connect(self.Mic1Lcd.display)
        self.Mic1Fader.valueChanged.connect(functools.partial(self.valueChange, CC_MIC1_CH, CC_MAIN_FADER_PAR))
        self.Mic1Fader.setProperty("parameter", CC_MAIN_FADER_PAR)

        # Setting Up the Mic1 Pan Dial
        self.Mic1Pan.valueChanged.connect(self.Mic1PanLcd.display)
        self.Mic1Pan.valueChanged.connect(functools.partial(self.valueChange, CC_MIC1_CH, CC_PAN_PAR))
        self.Mic1Pan.setProperty("parameter", CC_PAN_PAR)
        # center...
        self.Mic1Pan.setProperty("value", CC_PAN_MIDDLE)

        # I also need Mic1Pan2, a "copy" of Mic2 for the Mic1+Mic2 mode:
        self.Mic1Pan2.valueChanged.connect(self.Mic1PanLcd2.display)
        self.Mic1Pan2.valueChanged.connect(functools.partial(self.valueChange, CC_MIC2_CH, CC_PAN_PAR))
        self.Mic1Pan2.setProperty("parameter", CC_PAN_PAR)
        self.Mic1Pan2.setProperty("value", CC_PAN_MIDDLE)

        # Setting up Ins1&2
        self.Mic1Ins1.valueChanged.connect(functools.partial(self.valueChange, CC_MIC1_CH, CC_SEND1_PAR))
        self.Mic1Ins2.valueChanged.connect(functools.partial(self.valueChange, CC_MIC1_CH, CC_SEND2_PAR))

        # Setting Up the Mic1 Solo Button ** THERE CAN ONLY BE ONE "SOLO" CHECKED, THUS... **
        self.Mic1Solo.toggled.connect(self.uniqueSolos)

        self.Mic1Mute.toggled.connect(functools.partial(self.valueChange, CC_MIC1_CH, CC_MUTE_PAR))

        # Setting Up the SubFader
        self.Mic1SubFader.valueChanged.connect(self.Mic1SubLcd.display)
        self.Mic1SubFader.valueChanged.connect(functools.partial(self.valueChange, CC_MIC1_CH, CC_SUB_FADER_PAR))

        # hiding the subs...
        self.Mic1SubFader.hide()
        self.Mic1SubLcd.hide()

        # *************** MIC2 *********************

        self.Mic2.setProperty("channel", CC_MIC2_CH)

        # Setting Up the Mic2 Fader
        self.Mic2Fader.valueChanged.connect(self.Mic2Lcd.display)
        self.Mic2Fader.valueChanged.connect(functools.partial(self.valueChange, CC_MIC2_CH, CC_MAIN_FADER_PAR))
        self.Mic2Fader.setProperty("parameter", CC_MAIN_FADER_PAR)

        # Setting Up the Mic2 Pan Dial
        self.Mic2Pan.valueChanged.connect(self.Mic2PanLcd.display)
        self.Mic2Pan.valueChanged.connect(functools.partial(self.valueChange, CC_MIC2_CH, CC_PAN_PAR))
        self.Mic2Pan.setProperty("parameter", CC_PAN_PAR)
        # center...
        self.Mic2Pan.setProperty("value", CC_PAN_MIDDLE)

        # I also need Mic1Pan2, a "copy" of Mic2 for the Mic1+Mic2 mode:
        self.Mic1Pan2.valueChanged.connect(self.Mic1PanLcd2.display)
        self.Mic1Pan2.valueChanged.connect(functools.partial(self.valueChange, CC_MIC2_CH, CC_PAN_PAR))
        self.Mic1Pan2.setProperty("parameter", CC_PAN_PAR)

        # Setting up Ins1&2
        self.Mic2Ins1.valueChanged.connect(functools.partial(self.valueChange, CC_MIC2_CH, CC_SEND1_PAR))
        self.Mic2Ins2.valueChanged.connect(functools.partial(self.valueChange, CC_MIC2_CH, CC_SEND2_PAR))

        # Setting Up the Mic2 Solo Button ** THEY CAN BE ONLY ONE SOLO CHECKED, THUS... **
        self.Mic2Solo.toggled.connect(self.uniqueSolos)

        self.Mic2Mute.toggled.connect(functools.partial(self.valueChange, CC_MIC2_CH, CC_MUTE_PAR))

        # hiding the subs...
        self.Mic2SubFader.hide()
        self.Mic2SubLcd.hide()

        # Setting Up the SubFader
        self.Mic2SubFader.valueChanged.connect(self.Mic2SubLcd.display)
        self.Mic2SubFader.valueChanged.connect(functools.partial(self.valueChange, CC_MIC2_CH, CC_SUB_FADER_PAR))

        # *************** WAVE1 *********************

        self.Wave1.setProperty("channel", CC_WAVE1_CH)

        # Setting up the Wave1 Fader
        self.Wave1Fader.valueChanged.connect(self.Wave1Lcd.display)
        self.Wave1Fader.valueChanged.connect(functools.partial(self.valueChange, CC_WAVE1_CH, CC_MAIN_FADER_PAR))
        self.Wave1Fader.setProperty("parameter", CC_MAIN_FADER_PAR)

        # Setting up Ins1&2
        self.Wave1Ins1.valueChanged.connect(functools.partial(self.valueChange, CC_WAVE1_CH, CC_SEND1_PAR))
        self.Wave1Ins2.valueChanged.connect(functools.partial(self.valueChange, CC_WAVE1_CH, CC_SEND2_PAR))

        # Setting Up the Wave1 Solo Button ** THEY CAN BE ONLY ONE SOLO CHECKED, THUS... **
        self.Wave1Solo.toggled.connect(self.uniqueSolos)
        self.Wave1Mute.toggled.connect(functools.partial(self.valueChange, CC_WAVE1_CH, CC_MUTE_PAR))

        # Setting Up the SubFader
        self.Wave1SubFader.valueChanged.connect(self.Wave1SubLcd.display)
        self.Wave1SubFader.valueChanged.connect(functools.partial(self.valueChange, CC_WAVE1_CH, CC_SUB_FADER_PAR))

        # hiding the subs...
        self.Wave1SubFader.hide()
        self.Wave1SubLcd.hide()

        # *************** WAVE2 *********************

        self.Wave2.setProperty("channel", CC_WAVE2_CH)

        # Setting up the Wave1 Fader
        self.Wave2Fader.valueChanged.connect(self.Wave2Lcd.display)
        self.Wave2Fader.valueChanged.connect(functools.partial(self.valueChange, CC_WAVE2_CH, CC_MAIN_FADER_PAR))
        self.Wave2Fader.setProperty("parameter", CC_MAIN_FADER_PAR)

        # Setting up Ins1&2
        self.Wave2Ins1.valueChanged.connect(functools.partial(self.valueChange, CC_WAVE2_CH, CC_SEND1_PAR))
        self.Wave2Ins2.valueChanged.connect(functools.partial(self.valueChange, CC_WAVE2_CH, CC_SEND2_PAR))

        # Setting Up the Wave2 Solo Button ** THEY CAN BE ONLY ONE SOLO CHECKED, THUS... **
        self.Wave2Solo.toggled.connect(self.uniqueSolos)

        self.Wave2Mute.toggled.connect(functools.partial(self.valueChange, CC_WAVE2_CH, CC_MUTE_PAR))

        # Setting Up the SubFader
        self.Wave2SubFader.valueChanged.connect(self.Wave2SubLcd.display)
        self.Wave2SubFader.valueChanged.connect(functools.partial(self.valueChange, CC_WAVE2_CH, CC_SUB_FADER_PAR))

        # hiding the subs...
        self.Wave2SubFader.hide()
        self.Wave2SubLcd.hide()

        # *************** MASTERLINE *********************

        self.MasterLineFader.setProperty("channel", CC_LINE_MASTER_CH)

        # Setting Up the MasterLine Fader
        self.MasterLineFader.valueChanged.connect(self.MasterLineLcd.display)
        self.MasterLineFader.valueChanged.connect(
            functools.partial(self.valueChange, CC_LINE_MASTER_CH, CC_MAIN_FADER_PAR))
        self.MasterLineFader.setProperty("parameter", CC_MAIN_FADER_PAR)

        # *************** WAVE (REC) **********************

        # Setting up the Wave (Rec) Fader
        self.WaveRecFader.valueChanged.connect(self.WaveRecLcd.display)
        self.WaveRecFader.valueChanged.connect(functools.partial(self.valueChange, CC_WAVEREC_CH, CC_MAIN_FADER_PAR))

        # *************** SYSEFF **************************

        # Return
        self.SysEffRet1.valueChanged.connect(functools.partial(self.valueChange, CC_SYSRET_CH, CC_SEND1_PAR))
        self.SysEffRet2.valueChanged.connect(functools.partial(self.valueChange, CC_SYSRET_CH, CC_SEND2_PAR))
        # Sub
        self.SysEffSub1.valueChanged.connect(functools.partial(self.valueChange, CC_SYSSUB_CH, CC_SEND1_PAR))
        self.SysEffSub2.valueChanged.connect(functools.partial(self.valueChange, CC_SYSSUB_CH, CC_SEND2_PAR))

        # SUB BUTTON

        self.SubButton.toggled.connect(self.showHideSub)

        # hiding more...
        self.SysEffSub1.hide()
        self.SysEffSub2.hide()
        self.SysEffSubLabel.hide()

        # Setting Up Mixer Output Sources for Master
        self.OutputMasterSourceSelect.currentIndexChanged.connect(
            functools.partial(self.valueChange, CC_LINE_MASTER_CH, CC_SELECTOR_PAR))
        if (MIXER_OUTPUT_MODE):
            for key in MASTER_SELECT_MIXERMODE.keys():
                self.OutputMasterSourceSelect.addItem(MASTER_SELECT_MIXERMODE[key])
            self.OutputMasterSourceSelect.setCurrentIndex(0x09)

        # Setting Up Mixer Output Sources for Wave(Rec)
        self.OutputWaveRecSourceSelect.currentIndexChanged.connect(
            functools.partial(self.valueChange, CC_WAVEREC_CH, CC_SELECTOR_PAR))
        if (MIXER_OUTPUT_MODE):
            for key in WAVE_SELECT_MIXERMODE.keys():
                self.OutputWaveRecSourceSelect.addItem(WAVE_SELECT_MIXERMODE[key])
            self.OutputWaveRecSourceSelect.setCurrentIndex(0x09)

        if (MIXER_OUTPUT_MODE):
            for key in MIXER_EFFECT_MODE_PAR.keys():
                self.uiEffectModeSelector.addItem(MIXER_EFFECT_MODE_PAR[key], key)
            self.uiEffectModeSelector.setCurrentIndex(-1)
        self.uiEffectModeSelector.currentIndexChanged.connect(self.setEffectMode)
        self.EffMic1Button.setProperty('HEX', [0x01])
        self.EffMic1Button.clicked.connect(self.effectSelection)
        self.EffMic2Button.setProperty('HEX', [0x02])
        self.EffMic2Button.clicked.connect(self.effectSelection)
        self.EffWave1Button.setProperty('HEX', [0x03])
        self.EffWave1Button.clicked.connect(self.effectSelection)
        self.EffWave2Button.setProperty('HEX', [0x04])
        self.EffWave2Button.clicked.connect(self.effectSelection)
        self.EffSys1Button.setProperty('HEX', [0x05])
        self.EffSys1Button.clicked.connect(self.effectSelection)
        self.EffSys2Button.setProperty('HEX', [0x06])
        self.EffSys2Button.clicked.connect(self.effectSelection)

        if (REAL_UA_MODE):
            self.__setInitMixerLevels__()
            pass

        self.uiInputModeButton.setProperty('state', 0x00)
        self.Mic1Pan2.hide()
        self.Mic1PanLcd2.hide()
        self.uiInputModeButton.clicked.connect(self.setInputMode)

        # Setting up the"Easy Settings" Box.
        #
        # by now, just my "Sax Mode" button will work.

        # Setting up "Sax Mode"
        #
        # Actually, as I use Audacity to listen and record my "performances" on the Saxophone, this button will
        # just switch MAIN output source to "Wave1" (the audacity output) and the Wave (REC) output to "Mic1/..."

        self.SaxModeButton.clicked.connect(self.saxMode)

    def saxMode(self):
        '''
        This should just switch MAIN output source to "Wave1" (the audacity output) and the Wave (REC) output to "Mic1/..."
        '''
        self.OutputMasterSourceSelect.setCurrentIndex(0x02)
        self.OutputWaveRecSourceSelect.setCurrentIndex(0x00)
        pass

    def setInputMode(self):
        '''
        
        The MIC1-GUITAR/LINE/MIC1+MIC2 toggler
        
        need a tree way button...
        MIC/LINE 21 (15H)       0: Mic Mode, 1: Line Mode, 2: MIC1+MIC2 Mod
        
        '''

        if self.sender().property('state') == 0x00:
            # Going to line mode...
            self.sender().setProperty('state', 0x01)
            self.Mic1.setTitle('Line')
            self.uiInputModeLabel.setText('Line')
            self.Mic2.hide()
            self.Mic1Pan2.hide()
            self.Mic1PanLcd2.hide()
        elif self.sender().property('state') == 0x01:
            # going to Mic1 + Mic 2 Mode
            self.sender().setProperty('state', 0x02)
            self.Mic1.setTitle('Mic1/GTR+Mic2')
            self.uiInputModeLabel.setText('Mic1\n+Mic2')
            self.Mic2.setEnabled(False)
            self.Mic2.hide()
            self.Mic1Pan2.show()
            self.Mic1PanLcd2.show()
            # let's expand a bit...
            self.Mic1.setProperty
        elif self.sender().property('state') == 0x02:
            # Back to
            self.sender().setProperty('state', 0x00)
            self.Mic1.setTitle('Mic1/Guitar')
            self.uiInputModeLabel.setText('Mic/GTR')
            self.Mic2.setEnabled(True)
            self.Mic1Pan2.hide()
            self.Mic1PanLcd2.hide()
            self.Mic2.show()

        if (REAL_UA_MODE):
            p = mido.Parser()
            p.feed([CC_MIC1_CH, CC_MICLINESELECTOR_PAR, self.sender().property('state').toPyObject()])
            shortMsg = p.get_message()
            logger.debug('Message to be sent %s', shortMsg)
            pmout.send(shortMsg)

        logger.debug('%s %s %s', CC_MIC1_CH, CC_MICLINESELECTOR_PAR, self.sender().property('state').toPyObject())

    def setEffectMode(self, value):
        '''
        ???
        '''

        global MixerEffectMode
        valueToList = [sorted(MIXER_EFFECT_MODE_PAR.keys())[value]]
        send_DT1(MIXER_EFFECT_CONTROL + MIXER_EFFECT_MODE + valueToList)
        MixerEffectMode = sorted(MIXER_EFFECT_MODE_PAR.keys())[value]

    def effectSelection(self):
        global MixerEffectMode
        if (MixerEffectMode == 0x04):
            if (self.fullEffects):
                self.fullEffects.close()
                self.fullEffects = FullEffectsDialog(self)
            else:
                self.fullEffects = FullEffectsDialog(self)
            self.fullEffects.show()
        if (MixerEffectMode == 0x03):
            # We can have only one effect for the mic1, mic2, wave1 and wave2
            # and both of sys1 and sys2
            if (self.sender().property('HEX') in ([0x05], [0x06])):
                if not (self.sender() in self.compactEffectsSys):
                    self.compactEffectsSys[self.sender()] = CompactEffectsSysDialog(self)
                self.compactEffectsSys[self.sender()].show()
            elif (self.sender().property('HEX') in ([0x01], [0x02], [0x03], [0x04])):
                # if not (self.sender() in self.compactEffectsIns):
                #    self.compactEffectsIns[self.sender()] = CompactEffectsInsDialog(self)
                # self.compactEffectsIns[self.sender()].show()
                if (self.compactEffectsIns):
                    self.compactEffectsIns.uiToggleEffect.setChecked(0)
                    self.compactEffectsIns.close()
                    self.compactEffectsIns = CompactEffectsInsDialog(self)
                    # self.compactEffectsInsert.uiToggleEffect.setChecked(1)
                else:
                    self.compactEffectsIns = CompactEffectsInsDialog(self)
                self.compactEffectsIns.show()

    def showHideSub(self, checked):
        '''
        Hide/Show Sub fader control when button clicked.
        '''
        if (checked):
            self.Mic1SubFader.show()
            self.Mic1SubLcd.show()
            self.Mic2SubFader.show()
            self.Mic2SubLcd.show()
            self.Wave1SubFader.show()
            self.Wave1SubLcd.show()
            self.Wave2SubFader.show()
            self.Wave2SubLcd.show()
            self.SysEffSub1.show()
            self.SysEffSub2.show()
            self.SysEffSubLabel.show()
        else:
            self.Mic1SubFader.hide()
            self.Mic1SubLcd.hide()
            self.Mic2SubFader.hide()
            self.Mic2SubLcd.hide()
            self.Wave1SubFader.hide()
            self.Wave1SubLcd.hide()
            self.Wave2SubFader.hide()
            self.Wave2SubLcd.hide()
            self.SysEffSub1.hide()
            self.SysEffSub2.hide()
            self.SysEffSubLabel.hide()

    def valueChange(self, a, b, val):
        '''
        custom slot to connect to the changes in the interface with WriteShort to send the control change messages
        '''
        logger.debug('Value change: %s %s %s', a, b, val)

        if (REAL_UA_MODE):
            p = mido.Parser()
            p.feed([a, b, val])
            shortMsg = p.get_message()
            logger.debug('Message to be sent %s', shortMsg)
            pmout.send(shortMsg)

    def uniqueSolos(self, checked):
        '''
        unchecks all other solo buttons if the present is checked.
        besides, it actually soloes/unsoloes the channel
        '''

        soloers = ['Mic1', 'Mic2', 'Wave1', 'Wave2']
        soloers.remove(str(self.sender().parent().objectName()))
        if (checked):
            logger.debug('soloers: %s', soloers)
            logger.debug('unchecking and desoloing ')
            logger.debig('soloing %s', str(self.sender().parent().objectName()))

            if (REAL_UA_MODE):
                p = mido.Parser()
                p.feed([self.sender().parent().property('channel').toPyObject(), CC_SOLO_PAR, 1])
                shortMsg = p.get_message()
                logger.info('Message to be sent %s', shortMsg)
                pmout.send(shortMsg)

            for soloer in soloers:
                soloingObj = self.findChild(QtGui.QGroupBox, soloer)

                if (REAL_UA_MODE):
                    p = mido.Parser()
                    p.feed([soloingObj.property('channel').toPyObject(), CC_SOLO_PAR, 0])
                    shortMsg = p.get_message()
                    logger.info('Message to be sent %s', shortMsg)
                    pmout.send(shortMsg)

                soloingButtonStr = soloer + 'Solo'
                nomuteButtonStr = soloer + 'Mute'
                soloingButton = soloingObj.findChild(QtGui.QPushButton, soloingButtonStr)
                nomuteButton = soloingObj.findChild(QtGui.QPushButton, nomuteButtonStr)
                soloingButton.setChecked(False)
                nomuteButton.hide()
                # review those fucking debug messages. They are just fucking messed up!
                logging.debug('desoloing: %s', soloingObj.objectName())
        else:
            for soloer in soloers:
                soloingObj = self.findChild(QtGui.QGroupBox, soloer)
                remuteButtonStr = soloer + 'Mute'
                remuteButton = soloingObj.findChild(QtGui.QPushButton, remuteButtonStr)
                remuteButton.show()

            if (REAL_UA_MODE):
                p = mido.Parser()
                p.feed([self.sender().parent().property('channel').toPyObject(), CC_SOLO_PAR, 0])
                shortMsg = p.get_message()
                logger.info('Message to be sent %S', shortMsg)
                pmout.send(shortMsg)

    def resetMixer(self):
        '''
        Reset all mixer values to average ones.
        ***************************************
        A better idea could be to retrieve the current values (with sysex messages) and use them...
        maybe in the future
        ***************************************
        '''
        self.MasterLineFader.setProperty("value", CC_0127_DEFAULT)
        self.Wave1Fader.setProperty("value", CC_0127_DEFAULT)
        # self.Wave1SubFader.setProperty("value", CC_0127_DEFAULT)
        self.Wave2Fader.setProperty("value", CC_0127_DEFAULT)
        # self.Wave2SubFader.setProperty("value", CC_0127_DEFAULT)
        self.Mic1Fader.setProperty("value", CC_0127_DEFAULT)
        self.Mic1Pan.setProperty("value", CC_PAN_MIDDLE)
        # self.Mic1SubFader.setProperty("value", CC_0127_DEFAULT)
        self.Mic2Fader.setProperty("value", CC_0127_DEFAULT)
        self.Mic2Pan.setProperty("value", CC_PAN_MIDDLE)
        # self.Mic2SubFader.setProperty("value", CC_0127_DEFAULT)
        self.WaveRecFader.setProperty("value", CC_0127_DEFAULT)

        self.Mic1Pan2.setProperty("value", CC_PAN_MIDDLE)

    def __setInitMixerLevels__(self):
        '''
        It works. It send SYSEX and reads answers. But there must me a better way to read and write.
        Actually there is, but I'm lazy.
        '''

        send_RQ1(MIXER_OUTPUT_CONTROL + MIXER_OUTPUT_MASTERLEVEL + MIXER_OUTPUT_MASTERLEVEL_SIZE)
        time.sleep(SLEEP_TIME)

        masterLevel = sysexRead(question = 'masterLevel')
        #logger.info('masterlevel= %s', masterLevel)
        self.MasterLineFader.setProperty("value", masterLevel)

        send_RQ1(MIXER_OUTPUT_CONTROL + MIXER_OUTPUT_WAVEREC + MIXER_OUTPUT_WAVEREC_SIZE)
        time.sleep(SLEEP_TIME)
        waverecLevel = sysexRead(question = "waverecLevel")
        self.WaveRecFader.setProperty("value", waverecLevel)

        send_RQ1(MIC1_FADER + MIC1_FADER_SIZE)
        time.sleep(SLEEP_TIME)
        mic1Level = sysexRead(question = "mic1Level")
        self.Mic1Fader.setProperty("value", mic1Level)

        send_RQ1(MIC2_FADER + MIC2_FADER_SIZE)
        time.sleep(SLEEP_TIME)
        mic2Level = sysexRead(question = "mic2Level")
        self.Mic2Fader.setProperty("value", mic2Level)

        send_RQ1(WAVE1_FADER + WAVE1_FADER_SIZE)
        time.sleep(SLEEP_TIME)
        wave1Level = sysexRead(question = "wave1Level")
        self.Wave1Fader.setProperty("value", wave1Level)

        send_RQ1(WAVE2_FADER + WAVE2_FADER_SIZE)
        time.sleep(SLEEP_TIME)
        wave2Level = sysexRead(question = "wave2Level")
        self.Wave2Fader.setProperty("value", wave2Level)


class CompactEffectsInsDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(CompactEffectsInsDialog, self).__init__(parent)
        # here is where I store the channel choosen fo the effect (mic1, mic2, wave1, wave2, sys1, sys2)
        self.SenderHex = parent.sender().property('HEX').toPyObject()
        # load the ui...
        self.ui = PyQt4.uic.loadUi('ui/compacteffectsinsdialog.ui', self)

        # populate the effect groups

        for key in COMPACT_INS_EFX_GROUP.keys():
            self.uiEffectGroupsList.addItem(COMPACT_INS_EFX_GROUP[key][0])

        # connect the group list to the effect type list in order to populate it
        self.uiEffectGroupsList.currentIndexChanged.connect(self.populateEffectType)

        # populate the effect type list with the first one (0)
        self.populateEffectType(0)

        # connect the set effect button with the relative function
        self.uiToggleEffect.toggled.connect(self.setEffect)

    def populateEffectType(self, index):
        """
        populate the list of effect types


        """
        # first, clear the previous list
        self.uiEffectTypeList.clear()

        # remember in which group we are
        self.InsEffectGroup = index

        # get the effect type names and put them in the drop down list
        for effectType in COMPACT_INS_EFX_GROUP[index][1]:
            self.uiEffectTypeList.addItem(COMPACT_INS_EFX_TYPE[effectType][0])

        # connect the effect type drop down widget with the parameters in order to populate the effect options
        self.uiEffectTypeList.currentIndexChanged.connect(self.populateEffect)

        # set the start effect type to 0
        self.populateEffect(0)

    def populateEffect(self, index):
        """
        populate the effect parameter.
        BE CAREFUL! The offset shit is tricky. I must explain better, I did not understand it myself after a year.

        :param index is relative to the effect group: we must add the offset to get to the right point.

        """
        # clear the parameters
        self.uiEffectParameters.clear()

        # tell the UA-100 we are setting exactly those effect parameters
        send_DT1([0x00, 0x40] + self.SenderHex + [0x00] + COMPACT_INS_EFX_TYPE[index][1])

        # I need to add an offset because of the grouping for the compact insertion effects.
        #
        # Please note:
        #
        # COMPACT_INS_EFX_GROUP contains the GROUPS or TYPE
        #
        # The offset is actually the first value of the range list in the definition
        #
        # COMPACT_INS_EFX_TYPE misleading name containing the single effects
        #
        # COMPACT_INS_EFX_PARAMETERS[xxx] countains the parameters of the single effects
        #

        # read the offset of the specified group to reach the right effects
        offset = COMPACT_INS_EFX_GROUP[self.InsEffectGroup][1][0]

        logger.debug('Indice: %s, Offset: %s', index, offset)

        # populate the effect parameters

        for param in COMPACT_INS_EFX_PARAMETERS[index + offset]:
            logger.debug('filling: %s', param)
            item = CustomTreeItem(self.uiEffectParameters, param)

    def sendEffect(self, value):
        '''
        We send the values set to the UA-100. The effects are only active when also the switch is checked.
        '''

        # first of all convert the passed value to list in order to send the SYSEX message
        valueToList = [value]
        logger.info('LSB/MSB for parameter: %s', self.sender().property('HEX').toPyObject())

        # if in real mode, actually send the message
        if REAL_UA_MODE == 1:
            send_DT1([0x00, 0x40] + self.SenderHex + self.sender().property('HEX').toPyObject() + valueToList)

    def setEffect(self, checked):
        '''
        A small but invaluable function:
        
        IT SWITCHES THE WHOLE THIG ON!
        '''

        logger.debug('Sender Hex: %s',self.SenderHex)
        if (checked):
            checkedList = [0x01]
        else:
            checkedList = [0x00]
        send_DT1([0x00, 0x40, 0x40] + self.SenderHex + checkedList)


class CompactEffectsSysDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(CompactEffectsSysDialog, self).__init__(parent)
        # here is where I store the channel choosen fo the effect (mic1, mic2, wave1, wave2, sys1, sys2)
        self.SenderHex = parent.sender().property('HEX').toPyObject()
        # load the ui...
        self.ui = PyQt4.uic.loadUi('ui/compacteffectssysdialog.ui', self)
        if self.SenderHex == [0x05]:
            self.setWindowTitle('System 1 - ' + self.windowTitle())
            self.uiEffectTypeList.addItem(COMPACT_SYS1_EFX_TYPE[1][0])
            self.uiEffectTypeList.addItem(COMPACT_SYS1_EFX_TYPE[2][0])
        elif self.SenderHex == [0x06]:
            self.setWindowTitle('System 2 - ' + self.windowTitle())
            self.uiEffectTypeList.addItem(COMPACT_SYS2_EFX_TYPE[1][0])
            self.uiEffectTypeList.addItem(COMPACT_SYS2_EFX_TYPE[2][0])

        # connect the combobox with the slot which populates the QTreeWidget
        self.uiEffectTypeList.currentIndexChanged.connect(self.populateEffect)

        self.populateEffect(0)

        self.uiToggleEffect.toggled.connect(self.setEffect)

    def populateEffect(self, index):

        # first af all, sent the effect type to the UA-100
        # This is the LSB/MSB of the effect type (i.e. High Quality Reverb, Mic Simulator) aka the FULL_EFX_TYPE[n][1] (hex value)
        self.uiEffectParameters.clear()
        if (self.SenderHex == [0x05]):
            logger.debug('Populate parameter DT1: %s', [0x00, 0x40] + self.SenderHex + [0x00] + COMPACT_SYS1_EFX_TYPE[index + 1][1])
            send_DT1([0x00, 0x40] + self.SenderHex + [0x00] + COMPACT_SYS1_EFX_TYPE[index + 1][1])
            for par in COMPACT_SYS1_EFX_PARAMETERS[index + 1]:
                item = CustomTreeItem(self.uiEffectParameters, par)
        elif (self.SenderHex == [0x06]):
            logger.debug('Populate parameter DT1: %s',[0x00, 0x40] + self.SenderHex + [0x00] + COMPACT_SYS2_EFX_TYPE[index + 1][1])
            send_DT1([0x00, 0x40] + self.SenderHex + [0x00] + COMPACT_SYS2_EFX_TYPE[index + 1][1])
            for par in COMPACT_SYS2_EFX_PARAMETERS[index + 1]:
                item = CustomTreeItem(self.uiEffectParameters, par)

    def setEffect(self, checked):
        '''
        A small but invaluable function:
        
        IT SWITCHES THE WHOLE THIG ON!
        '''

        logger.debug('Sender Hex: %s', self.SenderHex)
        if (checked):
            checkedList = [0x01]
        else:
            checkedList = [0x00]
        send_DT1([0x00, 0x40, 0x40] + self.SenderHex + checkedList)

    def sendEffect(self, value):
        '''
        We send the values set to the UA-100. The effects are only active when also the switch is checked.
        '''

        # first of all convert the passed value to list in order to send the SYSEX message
        valueToList = [value]
        logger.debug('LSB/MSB for parameter: %s', self.sender().property('HEX').toPyObject())

        # if in real mode, actually send the message
        send_DT1([0x00, 0x40] + self.SenderHex + self.sender().property('HEX').toPyObject() + valueToList)


class FullEffectsDialog(QtGui.QDialog):
    '''
    The full effect dialog.
    For every single effect selected, I should check if there are already instances for the effect. If not, generate it, if yes, use the old ones.
    BUT after I clead the QTreeWidget the instances of the QTreeWidgetItems get deleted. There should be a better way.
    To achieve this, sadly, we need to classify the items...
    '''

    def __init__(self, parent=None):
        super(FullEffectsDialog, self).__init__(parent)

        # here is where I store the channel choosen fo the effect (mic1, mic2, wave1, wave2, sys1, sys2)
        self.SenderHex = parent.sender().property('HEX').toPyObject()
        # QLineEditStr = 'uiEffectName' + self.sender().text()
        # self.EffectNameTextBox = self.parent().findChild(QtGui.QLineEdit, QLineEditStr)
        # load the ui...
        self.ui = PyQt4.uic.loadUi('ui/fulleffectsdialog.ui', self)

        # look for the FULL_EFX_TYPEs and populate the combo box (drop down menu)
        for key in FULL_EFX_TYPE.keys():
            self.EffectTypeList.addItem(FULL_EFX_TYPE[key][0])

        # connect the combobox with the slot which populates the QTreeWidget
        self.EffectTypeList.currentIndexChanged.connect(self.populateEffect)

        self.populateEffect(0)

        self.uiToggleEffect.toggled.connect(self.setEffect)

    def setEffect(self, checked):
        '''
        A small but invaluable function:
        
        IT SWITCHES THE WHOLE THIG ON!
        '''

        logger.debug('Sender Hex: %s', self.SenderHex)
        if (checked):
            checkedList = [0x01]
            # self.EffectNameTextBox.setText(FULL_EFX_TYPE[self.actualEffectIndex][0])
        else:
            checkedList = [0x00]
            # self.EffectNameTextBox.clear()
        send_DT1([0x00, 0x40, 0x40] + self.SenderHex + checkedList)

    def populateEffect(self, index):

        # first af all, send the effect type to the UA-100
        # This is the LSB/MSB of the effect type (i.e. High Quality Reverb, Mic Simulator) aka the FULL_EFX_TYPE[n][1] (hex value)
        send_DT1([0x00, 0x40] + self.SenderHex + [0x00] + FULL_EFX_TYPE[index + 1][1])
        self.actualEffectIndex = index + 1

        self.uiEffectParameters.clear()

        # "anonimously" polulate the QTreeWidget ...
        for par in FULL_EFX_PARAMETERS[index + 1]:
            item = CustomTreeItem(self.uiEffectParameters, par)

    def sendEffect(self, value):
        '''
        We send the values set to the UA-100. The effects are only active when also the switch is checked.
        '''

        # first of all convert the passed value to list in order to send the SYSEX message
        valueToList = [value]
        logger.debug('LSB/MSB for parameter: %s', self.sender().property('HEX').toPyObject())

        # if in real mode, actually send the message
        send_DT1([0x00, 0x40] + self.SenderHex + self.sender().property('HEX').toPyObject() + valueToList)


class CustomTreeItem(QtGui.QTreeWidgetItem):
    '''
    Just a dirty way to populate the QTreeWidget with custom items containing each a QSpinBox.
    
    ******************************************************************************************
    ************************************** TODO **********************************************
    set limits, mean value, default value and possibly also a better way to show the values...
    ******************************************************************************************
    
    '''

    def __init__(self, parent, par):
        '''
        parent (QTreeWidget) : Item's QTreeWidget parent.
        name   (str)         : Item's name. just an example.
        '''

        ## Init super class ( QtGui.QTreeWidgetItem )
        super(CustomTreeItem, self).__init__(parent)
        self.par = par
        self.setText(0, par[0])
        self.spinBox = QtGui.QSpinBox(parent)
        self.spinBox.setProperty('HEX', par[3])

        self.spinBox.setValue(-1)
        self.spinBox.setRange(min(par[2].keys()), max(par[2].keys()))

        self.spinBox.setWrapping(1)
        parent.setItemWidget(self, 1, self.spinBox)
        self.setText(3, par[1])

        self.spinBox.valueChanged.connect(self.setActualValue)
        # set the spinBox to some value, in order to let the next setValue trigger the signals
        self.spinBox.setValue(-1)
        self.spinBox.valueChanged.connect(parent.parent().sendEffect)
        self.spinBox.setValue(par[4])

    def setActualValue(self, value):
        self.setText(2, self.par[2][value])


def actualMidiDevices():
    '''
    This should enumerate the devices to (later on) give then the possibility to choose one or guess the right one
    Returns a dictionary with tuples like 
    
    midiDevs = { 0: (tuple), 1: (tuple), ... }
    
    where the tuple is in the format:
    
    ('ALSA', 'UA-100 MIDI 2', 0, 1, 0)
    
    '''

    if (REAL_UA_MODE):
        IODevs = mido.get_ioport_names()
        numIODevs = len(IODevs)

        if (numIODevs == 0):
            logger.warning('***************  No midi device found - and we should be in REAL UA mode! Exiting. Bye!')
            sys.exit()

        logger.info('We have %s output devices: %s', numIODevs,  IODevs)
    else:
        numIODevs = 1
        IODevs = {u'Dummy midi device 0:0'}

    # Initialize the device dictionary
    # midiDevs = { 0: (tuple), 1: (tuple), ... }
    midiDevs = {}
    for dev in range(0, numIODevs):
        midiDevs[dev] = IODevs[dev]

    return midiDevs


def rightMidiDevice(midiDevs):
    '''
    Guess the right device for sending Control Change and SysEx messages.
    
    I suppose it is HEAVY dependant on rtMidi and ALSA:
    if *they* change something in the structure of the device info, we are lost!
    
    It scans the midiDevs (dictionary!) looking for something like 'UA-100 Control' with the output flag set to 1.
    '''
    for i in range(0, len(midiDevs)):
        if ('UA-100 Control' in midiDevs[i]):
            logger.info('Found something! The controller is device %s aka %s', i, midiDevs[i][1])
            return int(i)


def sysexRead(question = "unknown"):
    global pmin

    answerMsg = pmin.receive()
    answerBytes = answerMsg.bytes()
    value = answerBytes[11]
    logger.debug('SysEx answer for question %s received: %s, aka %s. Vaule is: %s', question, answerMsg, answerBytes, value)
    # need to parse answer again... 

    return value


def send_RQ1(data):
    '''
    Here we are about to send a Request Data 1.
    Never forget to checksum!
    
    ** Note
    The first part of the message is fixed. What can change is the data (of course, it's function agument!)
    AND the checksum, which, on his side, depends on the data.
    '''
    global pmout, pmin
    checksum_result = checksum(data)
    message = RQ1_STATUS \
              + UA_SYSEX_ID \
              + RQ1_COMMAND \
              + data \
              + checksum_result \
              + EOX
    logger.info("Message RQ1: %s", message)

    if (REAL_UA_MODE):
        p = mido.Parser()
        p.feed(message)
        sysEx_msg = p.get_message()
        logger.info('Message to be sent: %s', sysEx_msg)
        pmout.send(sysEx_msg)


def send_DT1(data):
    global pmout, pmin
    checksum_result = checksum(data)
    message = DT1_STATUS \
              + UA_SYSEX_ID \
              + DT1_COMMAND \
              + data \
              + checksum_result \
              + EOX
    logger.info('DT1 Message: %s', np.array(message))

    if (REAL_UA_MODE):
        p = mido.Parser()
        p.feed(message)
        sysEx_msg = p.get_message()
        logger.info('Message to be sent: %s', sysEx_msg)
        pmout.send(sysEx_msg)


def checksum(toChecksum):
    '''
    That's how the UA-100 does the checksum:
    Take the data part of SYSEXES and do the maths.
    '''
    checksum_value = (128 - (sum(toChecksum) % 128))
    checksum_list = [checksum_value]
    return list(checksum_list)


if (__name__ == '__main__'):

    # brutal way to catch the CTRL+C signal if run in the console...
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    # **************************** MIDI PART: could it go somewhere else? **********************************************

    # setting the backend to rtmidi and alsa - Actually it's not wise to do it so, but it's ok for now.
    mido.set_backend('mido.backends.rtmidi/LINUX_ALSA')
    # *************************************************
    # TODO: change it to be more general

    # get the list of the Midi Devices according to rtMidi
    midiDevs = actualMidiDevices()

    logger.info('MIDI DEVICES FOUND: %s; they are: %s', len(midiDevs), midiDevs)

    # guess the right midi device
    if (REAL_UA_MODE):
        DEFAULT_UA100CONTROL = rightMidiDevice(midiDevs)
    else:
        DEFAULT_UA100CONTROL = 1

    logger.debug('DEFAULT_UA100CONTROL = %s', midiDevs[DEFAULT_UA100CONTROL])

    # *******************************************************************************************************************

    app = None
    if (not app):
        app = QtGui.QApplication([])

    dialog = MidiDevsDialog()
    dialog.show()

    if not dialog.exec_():
        # We quit if the the selection dialog quits
        logger.info('Quitting. Bye!')
        sys.exit()

    if (REAL_UA_MODE):
        logger.debug('UA100CONTROL = %s', midiDevs[UA100CONTROL])

    logger.debug('Opening device %s for input/ouput', midiDevs[UA100CONTROL])

    if (REAL_UA_MODE):
        # Open device for output

        logger.info('Trying the Output...')

        pmout = mido.open_output(midiDevs[UA100CONTROL])

        logger.info('...Done! Just opened %s for output.', midiDevs[UA100CONTROL])

        # Open "the next" device for input

        logger.info('Trying the Input...')

        pmin = mido.open_input(midiDevs[UA100CONTROL])

        logger.info('...Done! Just opened %s  for input', midiDevs[UA100CONTROL])

    window = MainWindow()
    window.show()

    if (app):
        app.exec_()
