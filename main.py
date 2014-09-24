# ********************************
# ***** DEBUG MODE CONTROL *******
# SET:
#      1: debug messages on stdout ON
#      0: debug messages on stdout OFF

DEBUG_MODE = 1

# ********************************
# ***** UA MODE CONTROL **********
#
# SET:
#      0: No UA-100 present, for test purposes on other machines
#      1: UA-100 present and working
# NOTE: Could (and will) be automatically set to 0 if no UA-100 is found.
#       The UA-100 discovery routine is based on ALSA - **** 
#       ******* TO DO *******
#       Let the discovery be usb id based.

REAL_UA_MODE = 1

# ********************************

import numpy as np
import sys
import os
import functools
try:
    import pyportmidi as pm
except ImportError:
    print('*** Warning *** pyPortmidi not found - Swithing to testing mode (REAL_UA_MODE = 0) ***')
    REAL_UA_MODE = 0
import PyQt4.uic
from PyQt4 import QtGui, QtCore
from types import MethodType
import signal
import time
import res.tools as tools

if (DEBUG_MODE):
    np.set_printoptions(formatter={'int':hex})

# Defining costants (taken from UA-100 documentation)
# and copying some useful documentation excerts

if (DEBUG_MODE):
    print('Reading some constants...')

# just for convenience in code writing and editing
# in DEFINING CONSTANTS
if (True):
    
    # **************** this will and should be replaced with the real values obtained with sysex messages...
    CC_0127_DEFAULT = 64 # I think 'in media stat virtus'
    
    # ***************************************************************
    # *** 1. RECEIVE DATA
    # ***************************************************************
    # *************************
    # ** Channel Voice Messages
    # *************************
    #
    #         Status         |       2nd byte         |     3rd byte
    #          9nH           |          kkH           |       vvH
    #
    #
    # n = MIDI channel number: 0H-FH (ch.1-ch.16)
    # kk = note number : 00H-7FH (0-127)
    # NOTE: Used for pitch changes when using VT effect
    #
    # **********************************
    # Channel Voice Change STATUS Values
    # **********************************
    CV_MIC1_CH = 0x90
    CV_MIC2_CH = 0x91
    CV_WAVE1_CH = 0x92
    CV_WAVE2_CH = 0x93
    CV_SYSRET_CH = 0x94
    CV_SYSSUB_CH = 0x95
    CV_WAVEREC_CH = 0x9E
    CV_LINE_MASTER_CH = 0x9F
    #
    # ************************* 
    # ** Pitch Bend Change
    # *************************
    #
    #         Status         |       2nd byte         |     3rd byte
    #          EnH           |         llH            |       mmH
    #
    #
    # n = MIDI channel number: 0H-FH (ch.1-ch.16)
    # mm, ll = Pitch Bend value: 00 00H-40 00H-7F 7FH (-8192-0- +8191)
    # NOTE: Used for pitch changes when using VT effect
    #
    # *******************************
    # Pitch Bend Change STATUS Values
    # *******************************
    PB_MIC1_CH = 0xE0
    PB_MIC2_CH = 0xE1
    PB_WAVE1_CH = 0xE2
    PB_WAVE2_CH = 0xE3
    PB_SYSRET_CH = 0xE4
    PB_SYSSUB_CH = 0xe5
    PB_WAVEREC_CH = 0xEE
    PB_LINE_MASTER_CH = 0xEF
    #
    # *************************
    # ** Control Change
    # *************************
    #
    #         Status         |       2nd byte         |     3rd byte
    #          BnH                       mmH                   llH
    #
    # n = MIDI channel number: 0H-FH (ch. 1 to ch. 16:Refer to the correspondence chart)
    # mm = Mixer parameter number:Refer to the correspondence chart
    # ll = Mixer parameter value: 00H - 7FH (0 - 127)
    # ****************************
    # Control Change STATUS Values
    # ****************************
    CC_MIC1_CH = 0xB0
    CC_MIC2_CH = 0xB1
    CC_WAVE1_CH = 0xB2
    CC_WAVE2_CH = 0xB3
    CC_SYSRET_CH = 0xB4
    CC_SYSSUB_CH = 0xB5
    CC_WAVEREC_CH = 0xBE
    CC_LINE_MASTER_CH = 0xBF
    #
    # *********************************************************
    # * Correspondences Between MIDI Channels and Mixer Signals
    # *********************************************************
    #
    #      MIDI channel      |           Signal
    #           1Ch.         |  LINE (Line Mode), MIC1/GUITAR (Mic Mode), MIC1+MIC2 (MIC1+MIC2 Mode)
    #           2Ch.         |  MIC2 (Mic mode only)
    #           3Ch.         |  WAVE1
    #           4Ch.         |  WAVE2
    #           5Ch.         |  SysRET(system effect return Main bus)
    #           6Ch.         |  SysSUB(system effect return Sub bus)
    #           15Ch.        |  WAVE (Rec)
    #           16Ch.        |  LINE (Master)
    #
    # **********************************************************
    # * Mixer parameters and setting ranges
    # **********************************************************
    #
    # Parameter              |           mm           |             ll (setting range)
    # MIC/LINE Selector      |        21 (15H)        |     0: Mic Mode, 1: Line Mode, 2: MIC1+MIC2 Mode
    # Pan                    |        10 (0AH)        |     0 (left) - 64 (center) - 127 (right)
    # Send 1                 |        16 (10H)        |     0 - 127: Full/Compact Effect mode only
    # Send 2                 |        17 (11H)        |     0 - 127: Full/Compact Effect mode only
    # Mute                   |        18 (12H)        |     0 (OFF), 1 (ON: Mute)
    # Solo                   |        19 (13H)        |     0 (OFF), 1 (ON: Solo)
    # Sub Fader              |        20 (14H)        |     0 - 127
    # Main Fader             |         7 (07H)        |     0 - 127
    # Selector               |        22 (16H)        |     <Full/Compact Effect mode> 
    #                                                        0: MIC1 (Mic Mode), LINE (Line Mode), MIC1+MIC2 (MIC1+MIC2 Mode),
    #                                                        1: MIC2 (Mic Mode only), 
    #                                                        2: WAVE1,
    #                                                        3: WAVE2,
    #                                                        4 to 7: CH1 to 4,
    #                                                        8: SUB,
    #                                                        9: MAIN 
    #                                                       <VT Effect mode>
    #                                                        0: MIC1 (Mic Mode), LINE (Line Mode),
    #                                                        1: MIC2 (Mic Mode only),
    #                                                        2: WAVE1,
    #                                                        3: WAVE2,
    #                                                        4: VT_OUT,
    #                                                        5: MAIN
    # Effect Switch          |        23 (17H)        |      0 (OFF), 1 (ON: Apply effect)
    
    CC_MICLINESELECTOR_PAR = 21 # 0x15
    # CC_MICLINESELECTOR_RANGE = { 'Mic Mode': 0, 'Line Mode': 1, 'MIC1+MIC2 Mode': 2}
    CC_PAN_PAR = 10 # 0x0A - 0 - 64 - 127 (LEFT - CENTER - RIGHT)
    CC_SEND1_PAR = 16 # 0x10
    CC_SEND2_PAR = 17 # 0x11
    CC_MUTE_PAR = 18 # 0x12
    CC_SOLO_PAR = 19 # 0x13
    CC_SUB_FADER_PAR = 20 # 0x14
    CC_MAIN_FADER_PAR = 7 # 0x70
    CC_SELECTOR_PAR = 22 # 0x16
    CC_EFFECTSWITHC_PAR = 23 # 0x23
    
    # ******************************************************
    # * Correspondences Between Mixer Signals and Parameters
    # ******************************************************
    #
    #                   |  MIC1/LINE/ | MIC2 | WAVE1 | WAVE2 | SysRET |  SysSUB | WAVE  | LINE 
    #    Parameter      |  MIC1MIC2   | 2Ch. |  3Ch. |  4Ch. |   5Ch. |    6Ch. | 15Ch. | 16Ch.
    #                   |    1Ch.     |      |       |       |        |         |       |
    #                   |             |      |       |       |        |         |       |
    # MIC/LINE Selector |     O       |   -  |   -   |   -   |    -   |    -    |   -   |   -
    #    21 (15H)       |             |      |       |       |        |         |       |
    #                   |             |      |       |       |        |         |       |
    #       Pan         |     O       |   O  |   -   |   -   |    -   |    -    |   -   |   -
    #    10 (0AH)       |             |      |       |       |        |         |       |
    #                   |             |      |       |       |        |         |       |
    #     Send 1        |     O       |   O  |   O   |   O   |    O   |    O    |   -   |   -
    #    16 (10H)       |             |      |       |       |        |         |       |
    #                   |             |      |       |       |        |         |       |
    #     Send 2        |     O       |   O  |   O   |   O   |    O   |    O    |   -   |   -
    #    17 (11H)       |             |      |       |       |        |         |       |
    #                   |             |      |       |       |        |         |       |
    #      Mute         |     O       |   O  |   O   |   O   |    -   |    -    |   -   |   -
    #    18 (12H)       |             |      |       |       |        |         |       |
    #                   |             |      |       |       |        |         |       |
    #      Solo         |     O       |   O  |   O   |   O   |    -   |    -    |   -   |   -
    #    19 (13H)       |             |      |       |       |        |         |       |
    #                   |             |      |       |       |        |         |       |
    #    Sub Fader      |     O       |   O  |   O   |   O   |    -   |    -    |   -   |   -
    #    20 (14H)       |             |      |       |       |        |         |       |
    #                   |             |      |       |       |        |         |       |
    #    Main Fader     |     O       |   O  |   O   |   O   |    -   |    -    |   O   |   O
    #     7 (07H)       |             |      |       |       |        |         |       |
    #                   |             |      |       |       |        |         |       |
    #     Selector      |     -       |   -  |   -   |   -   |    -   |    -    |   O   |   O
    #    22 (16H)       |             |      |       |       |        |         |       |
    #                   |             |      |       |       |        |         |       |
    #   Effect Switch   |     O       |   O  |   O   |   O   |    O   |    O    |   -   |   -
    #    23 (17H)       |             |      |       |       |        |         |       |
    # **********************************************************************************************
    #
    # Omitting the RPN MSB/LSB and Data Entry part. TODO in a near future, at least for documentation purposes
    # 
    # MIDI EXCLUSIVE
    # ********** I SHALL PUT SOME CONSTANTS FOR THE SYSEXs AND PASTE THE DOCUMENTATION AS WELL **********
    # LET'S START
    #
    # let's set the sleep time between SYSEXex (in seconds)
    SLEEP_TIME = 0.05 
    
    # This should be common for all SYSEXes
    UA_SYSEX_ID= [0x41,0x10,0x00,0x11]
    
    # Request data 1 RQ1 (0x11)
    RQ1_STATUS = [0xF0]
    RQ1_COMMAND = [0x11]
    
    # Data set 1 (DT1)
    DT1_STATUS = [0xF0]
    DT1_COMMAND = [0x12]
    
    # Address map (one last 0xnn is the actual parameter)
    
    # Mixer Parameters
    
    
    # UA-100 Control
    
    UA100_CONTROL = [0x00, 0x40, 0x00]
    
    # MODE
    UA100_MODE = [0x00]
    UA100_MODE_SIZE = [0x00, 0x00, 0x00, 0x01]
    #UA100_MODE_DATARANGE = range(0x01,10)
        # 1: PC Mode(VT Effect Mode)
        # 3: PC Mode(Compact Effect Mode)
        # 4: PC Mode(Full Effect Mode)
        # 5: VT Mode
        # 6: Vocal Mode
        # 7: Guitar Mode
        # 8: GAME Mode
        # 9: BYPASS Mode
        # * Send only (sent when the Effect Type Selector is switched or when a requested by Data Request 1)
    
    # COPYRIGHT
    COPYRIGHT = [0x01]
    COPYRIGHT_SIZE = [0x00, 0x00, 0x00, 0x01]
    
    # Mixer Input Control
    MIXER_INPUT_CONTROL = [0x00, 0x40, 0x10]
    
    MIXER_INPUT_MODE = [0x00]
    MIXER_INPUT_MODE_SIZE = [0x00, 0x00, 0x00, 0x01]
    MIXER_INPUT_MODE_VALUES = {0x00: 'Mic Mode', 0x01: 'Line Mode', 0x02: 'MIC1 + MIC2 Mode'}
    
    MIXER_INPUT_PAN1 = [0x01]
    MIXER_INPUT_PAN1_SIZE = [0x00, 0x00, 0x00, 0x01]
    MIXER_INPUT_PAN2 = [0x02]
    MIXER_INPUT_PAN2_SIZE = [0x00, 0x00, 0x00, 0x01]
    MIXER_INPUT_MONITOR_SW = [0x03]
    MIXER_INPUT_MONITOR_SW_SIZE = [0x00, 0x00, 0x00, 0x01]
    
    #...
    MIC1_FADER = [0x00, 0x40, 0x11, 0x05]
    MIC1_FADER_SIZE = [0x00, 0x00, 0x00, 0x01]
    MIC2_FADER = [0x00, 0x40, 0x12, 0x05]
    MIC2_FADER_SIZE = [0x00, 0x00, 0x00, 0x01]
    WAVE1_FADER = [0x00, 0x40, 0x13, 0x05]
    WAVE1_FADER_SIZE = [0x00, 0x00, 0x00, 0x01]
    # WAVE1_FADER_RANGErange(0x00, 0x80)
    WAVE2_FADER = [0x00, 0x40, 0x14, 0x05]
    WAVE2_FADER_SIZE = [0x00, 0x00, 0x00, 0x01]
    #...
    
    EFFECT_PARAMETERS = [0x00, 0x40, 0x01]
    
    MIXER_EFFECT_CONTROL = [0x00, 0x40, 0x40]
    
    MIXER_EFFECT_MODE = [0x00]
    MIXER_EFFECT_MODE_SIZE = [0x00, 0x00, 0x00, 0x01]
    MIXER_EFFECT_MODE_PAR={#0x01: 'VT Effect Mode',\
                           0x03: 'Compact Effect Mode',\
                           0x04: 'Full Effect Mode'}
    
    
    
    # Mixer Output Control
    MIXER_OUTPUT_CONTROL = [0x00, 0x40, 0x50]
    #
    MASTER_SELECT_MIXERMODE = {0x00: 'LINE/MIC1/MIC1+MIC2',\
                               0x01: 'MIC2',\
                               0x02: 'WAVE1',\
                               0x03: 'WAVE2',\
                               0x04: 'CH1',\
                               0x05: 'CH2',\
                               0x06: 'CH3',\
                               0x07: 'CH4',\
                               0x08: 'SUB',\
                               0x09: 'MAIN',\
                               0x0A: 'WAVE(REC)OUT'}
    MASTER_SELECT_VTMIXERMODE = {0x00: 'LINE/MIC1',\
                                 0x01: 'MIC2',\
                                 0x02: 'WAVE1',\
                                 0x03: 'WAVE2',\
                                 0x04: 'VT_OUT',\
                                 0x05: 'MAIN',\
                                 0x06: 'WAVE(REC)OUT'}
    WAVE_SELECT_MIXERMODE = {0x00: 'LINE/MIC1/MIC1+MIC2',\
                               0x01: 'MIC2',\
                               0x02: 'WAVE1',\
                               0x03: 'WAVE2',\
                               0x04: 'CH1',\
                               0x05: 'CH2',\
                               0x06: 'CH3',\
                               0x07: 'CH4',\
                               0x08: 'SUB',\
                               0x09: 'MAIN'}
    WAVE_SELECT_VTMIXERMODE = {0x00: 'LINE/MIC1',\
                                 0x01: 'MIC2',\
                                 0x02: 'WAVE1',\
                                 0x03: 'WAVE2',\
                                 0x04: 'VT_OUT',\
                                 0x05: 'MAIN'}
    
    # Mixer Output Mode:
    # 0: VT MIXER MODE
    # 1: MIXER MODE
    MIXER_OUTPUT_MODE = 1
    
    #...
    MIXER_OUTPUT_MASTERLEVEL = [0x03]
    MIXER_OUTPUT_MASTERLEVEL_SIZE = [0x00, 0x00, 0x00, 0x01]
    #MIXER_OUTPUT_MASTERLEVEL_RANGE = range(0x00, 0x80)
    MIXER_OUTPUT_WAVEREC = [0x02]
    MIXER_OUTPUT_WAVEREC_SIZE = [0x00, 0x00, 0x00, 0x01]
    #...
    
    
    PRESET_EFFECT_CONTROL = [0x00, 0x40, 0x60]
    
    
    # PARAMETER CONVERSION TABLES
    # PRE DELAY TIME [ms] (1)
    # It is not a regular parameters as it has different steps. Must be built in steps...
    #PARAM_CONV_1 = tools.mergeRanges(range(0x00,0x33),tools.ulist(0,5,0.1,'ms'))
    #PARAM_CONV_1_B = tools.mergeRanges(range(0x33,0x3D),tools.ulist(5.5,10,0.5))
    #PARAM_CONV_1_C = tools.mergeRanges(range(0x3D,0x65),tools.ulist(11,50,1))
    #PARAM_CONV_1_D = tools.mergeRanges(range(0x65,0x7E),tools.ulist(52,100,2))
    #PARAM_CONV_1_E = {0x7E: '100', 0x7F: '100'}
    #PARAM_CONV_1.update(PARAM_CONV_1_B)
    #PARAM_CONV_1.update(PARAM_CONV_1_C)
    #PARAM_CONV_1.update(PARAM_CONV_1_D)
    #PARAM_CONV_1.update(PARAM_CONV_1_E)
    # to save CPU and time, I put THEM ALL already build...
    PARAM_TYPE_1 = ({0: '0ms', 1: '0.1ms', 2: '0.2ms', 3: '0.3ms', 4: '0.4ms', 5: '0.5ms',
                     6: '0.6ms', 7: '0.7ms', 8: '0.8ms', 9: '0.9ms', 10: '1.0ms', 11: '1.1ms',
                     12: '1.2ms', 13: '1.3ms', 14: '1.4ms', 15: '1.5ms', 16: '1.6ms', 17: '1.7ms',
                     18: '1.8ms', 19: '1.9ms', 20: '2.0ms', 21: '2.1ms', 22: '2.2ms', 23: '2.3ms',
                     24: '2.4ms', 25: '2.5ms', 26: '2.6ms', 27: '2.7ms', 28: '2.8ms', 29: '2.9ms',
                     30: '3.0ms', 31: '3.1ms', 32: '3.2ms', 33: '3.3ms', 34: '3.4ms', 35: '3.5ms',
                     36: '3.6ms', 37: '3.7ms', 38: '3.8ms', 39: '3.9ms', 40: '4.0ms', 41: '4.1ms',
                     42: '4.2ms', 43: '4.3ms', 44: '4.4ms', 45: '4.5ms', 46: '4.6ms', 47: '4.7ms',
                     48: '4.8ms', 49: '4.9ms', 50: '5.0ms', 51: '5.5', 52: '6.0', 53: '6.5', 54: '7.0',
                     55: '7.5', 56: '8.0', 57: '8.5', 58: '9.0', 59: '9.5', 60: '10.0', 61: '11', 62: '12',
                     63: '13', 64: '14', 65: '15', 66: '16', 67: '17', 68: '18', 69: '19', 70: '20', 71: '21',
                     72: '22', 73: '23', 74: '24', 75: '25', 76: '26', 77: '27', 78: '28', 79: '29', 80: '30',
                     81: '31', 82: '32', 83: '33', 84: '34', 85: '35', 86: '36', 87: '37', 88: '38', 89: '39',
                     90: '40', 91: '41', 92: '42', 93: '43', 94: '44', 95: '45', 96: '46', 97: '47', 98: '48',
                     99: '49', 100: '50', 101: '52', 102: '54', 103: '56', 104: '58', 105: '60', 106: '62',
                     107: '64', 108: '66', 109: '68', 110: '70', 111: '72', 112: '74', 113: '76', 114: '78',
                     115: '80', 116: '82', 117: '84', 118: '86', 119: '88', 120: '90', 121: '92', 122: '94',
                     123: '96', 124: '98', 125: '100', 126: '100', 127: '100'})
    PARAM_TYPE_4 = ({0: '0ms', 1: '0.1ms', 2: '0.2ms', 3: '0.3ms', 4: '0.4ms', 5: '0.5ms', 6: '0.6ms',
                     7: '0.7ms', 8: '0.8ms', 9: '0.9ms', 10: '1.0ms', 11: '1.1ms', 12: '1.2ms',
                     13: '1.3ms', 14: '1.4ms', 15: '1.5ms', 16: '1.6ms', 17: '1.7ms', 18: '1.8ms',
                     19: '1.9ms', 20: '2.0ms', 21: '2.1ms', 22: '2.2ms', 23: '2.3ms', 24: '2.4ms',
                     25: '2.5ms', 26: '2.6ms', 27: '2.7ms', 28: '2.8ms', 29: '2.9ms', 30: '3.0ms',
                     31: '3.1ms', 32: '3.2ms', 33: '3.3ms', 34: '3.4ms', 35: '3.5ms', 36: '3.6ms',
                     37: '3.7ms', 38: '3.8ms', 39: '3.9ms', 40: '4.0ms', 41: '4.1ms', 42: '4.2ms',
                     43: '4.3ms', 44: '4.4ms', 45: '4.5ms', 46: '4.6ms', 47: '4.7ms', 48: '4.8ms',
                     49: '4.9ms', 50: '5.0ms', 51: '5.5ms', 52: '6.0ms', 53: '6.5ms', 54: '7.0ms',
                     55: '7.5ms', 56: '8.0ms', 57: '8.5ms', 58: '9.0ms', 59: '9.5ms', 60: '10.0ms',
                     61: '11ms', 62: '12ms', 63: '13ms', 64: '14ms', 65: '15ms', 66: '16ms', 67: '17ms',
                     68: '18ms', 69: '19ms', 70: '20ms', 71: '21ms', 72: '22ms', 73: '23ms', 74: '24ms',
                     75: '25ms', 76: '26ms', 77: '27ms', 78: '28ms', 79: '29ms', 80: '30ms', 81: '31ms',
                     82: '32ms', 83: '33ms', 84: '34ms', 85: '35ms', 86: '36ms', 87: '37ms', 88: '38ms',
                     89: '39ms', 90: '40ms', 91: '50ms', 92: '60ms', 93: '70ms', 94: '80ms', 95: '90ms',
                     96: '100ms', 97: '110ms', 98: '120ms', 99: '130ms', 100: '140ms', 101: '150ms',
                     102: '160ms', 103: '170ms', 104: '180ms', 105: '190ms', 106: '200ms', 107: '210ms',
                     108: '220ms', 109: '230ms', 110: '240ms', 111: '250ms', 112: '260ms', 113: '270ms',
                     114: '280ms', 115: '290ms', 116: '300ms', 117: '320ms', 118: '340ms', 119: '360ms',
                     120: '380ms', 121: '400ms', 122: '420ms', 123: '440ms', 124: '460ms', 125: '480ms',
                     126: '500ms', 127: '500ms'}
        )
    
    PARAM_TYPE_4_SHORT = ({0: '0ms', 1: '0.1ms', 2: '0.2ms', 3: '0.3ms', 4: '0.4ms', 5: '0.5ms', 6: '0.6ms',
                     7: '0.7ms', 8: '0.8ms', 9: '0.9ms', 10: '1.0ms', 11: '1.1ms', 12: '1.2ms',
                     13: '1.3ms', 14: '1.4ms', 15: '1.5ms', 16: '1.6ms', 17: '1.7ms', 18: '1.8ms',
                     19: '1.9ms', 20: '2.0ms', 21: '2.1ms', 22: '2.2ms', 23: '2.3ms', 24: '2.4ms',
                     25: '2.5ms', 26: '2.6ms', 27: '2.7ms', 28: '2.8ms', 29: '2.9ms', 30: '3.0ms',
                     31: '3.1ms', 32: '3.2ms', 33: '3.3ms', 34: '3.4ms', 35: '3.5ms', 36: '3.6ms',
                     37: '3.7ms', 38: '3.8ms', 39: '3.9ms', 40: '4.0ms', 41: '4.1ms', 42: '4.2ms',
                     43: '4.3ms', 44: '4.4ms', 45: '4.5ms', 46: '4.6ms', 47: '4.7ms', 48: '4.8ms',
                     49: '4.9ms', 50: '5.0ms', 51: '5.5ms', 52: '6.0ms', 53: '6.5ms', 54: '7.0ms',
                     55: '7.5ms', 56: '8.0ms', 57: '8.5ms', 58: '9.0ms', 59: '9.5ms', 60: '10.0ms',
                     61: '11ms', 62: '12ms', 63: '13ms', 64: '14ms', 65: '15ms', 66: '16ms', 67: '17ms',
                     68: '18ms', 69: '19ms', 70: '20ms', 71: '21ms', 72: '22ms', 73: '23ms', 74: '24ms',
                     75: '25ms', 76: '26ms', 77: '27ms', 78: '28ms', 79: '29ms', 80: '30ms', 81: '31ms',
                     82: '32ms', 83: '33ms', 84: '34ms', 85: '35ms', 86: '36ms', 87: '37ms', 88: '38ms',
                     89: '39ms', 90: '40ms', 91: '50ms', 92: '60ms', 93: '70ms', 94: '80ms', 95: '90ms',
                     96: '100ms', 97: '110ms', 98: '120ms', 99: '130ms', 100: '140ms', 101: '150ms',
                     102: '160ms', 103: '170ms', 104: '180ms', 105: '190ms', 106: '200ms', 107: '210ms',
                     108: '220ms', 109: '230ms', 110: '240ms', 111: '250ms', 112: '260ms', 113: '270ms',
                     114: '280ms', 115: '290ms', 116: '300ms', 117: '320ms', 118: '340ms', 119: '360ms'}
        )

    #PARAM_TYPE_5 = tools.mergeRanges(range(0x00,0x80),tools.ulist(0,635,5,'ms'))
    PARAM_TYPE_5 = ({0: '0ms', 1: '5ms', 2: '10ms', 3: '15ms', 4: '20ms', 5: '25ms', 6: '30ms', 7: '35ms',
                    8: '40ms', 9: '45ms', 10: '50ms', 11: '55ms', 12: '60ms', 13: '65ms', 14: '70ms',
                    15: '75ms', 16: '80ms', 17: '85ms', 18: '90ms', 19: '95ms', 20: '100ms', 21: '105ms',
                    22: '110ms', 23: '115ms', 24: '120ms', 25: '125ms', 26: '130ms', 27: '135ms', 28: '140ms',
                    29: '145ms', 30: '150ms', 31: '155ms', 32: '160ms', 33: '165ms', 34: '170ms', 35: '175ms',
                    36: '180ms', 37: '185ms', 38: '190ms', 39: '195ms', 40: '200ms', 41: '205ms', 42: '210ms',
                    43: '215ms', 44: '220ms', 45: '225ms', 46: '230ms', 47: '235ms', 48: '240ms', 49: '245ms',
                    50: '250ms', 51: '255ms', 52: '260ms', 53: '265ms', 54: '270ms', 55: '275ms', 56: '280ms',
                    57: '285ms', 58: '290ms', 59: '295ms', 60: '300ms', 61: '305ms', 62: '310ms', 63: '315ms',
                    64: '320ms', 65: '325ms', 66: '330ms', 67: '335ms', 68: '340ms', 69: '345ms', 70: '350ms',
                    71: '355ms', 72: '360ms', 73: '365ms', 74: '370ms', 75: '375ms', 76: '380ms', 77: '385ms',
                    78: '390ms', 79: '395ms', 80: '400ms', 81: '405ms', 82: '410ms', 83: '415ms', 84: '420ms',
                    85: '425ms', 86: '430ms', 87: '435ms', 88: '440ms', 89: '445ms', 90: '450ms', 91: '455ms',
                    92: '460ms', 93: '465ms', 94: '470ms', 95: '475ms', 96: '480ms', 97: '485ms', 98: '490ms',
                    99: '495ms', 100: '500ms', 101: '505ms', 102: '510ms', 103: '515ms', 104: '520ms', 105: '525ms',
                    106: '530ms', 107: '535ms', 108: '540ms', 109: '545ms', 110: '550ms', 111: '555ms', 112: '560ms',
                    113: '565ms', 114: '570ms', 115: '575ms', 116: '580ms', 117: '585ms', 118: '590ms', 119: '595ms',
                    120: '600ms', 121: '605ms', 122: '610ms', 123: '615ms', 124: '620ms', 125: '625ms', 126: '630ms', 127: '635ms'})
    
    PARAM_TYPE_8 = ({0: '315Hz', 1: '315Hz', 2: '315Hz', 3: '315Hz', 4: '315Hz', 5: '315Hz', 6: '315Hz', 7: '315Hz', 8: '400Hz',
                     9: '400Hz', 10: '400Hz', 11: '400Hz', 12: '400Hz', 13: '400Hz', 14: '400Hz', 15: '400Hz', 16: '500Hz',
                     17: '500Hz', 18: '500Hz', 19: '500Hz', 20: '500Hz', 21: '500Hz', 22: '500Hz', 23: '500Hz', 24: '630Hz',
                     25: '630Hz', 26: '630Hz', 27: '630Hz', 28: '630Hz', 29: '630Hz', 30: '630Hz', 31: '630Hz', 32: '800Hz',
                     33: '800Hz', 34: '800Hz', 35: '800Hz', 36: '800Hz', 37: '800Hz', 38: '800Hz', 39: '800Hz', 40: '1000Hz',
                     41: '1000Hz', 42: '1000Hz', 43: '1000Hz', 44: '1000Hz', 45: '1000Hz', 46: '1000Hz', 47: '1000Hz',
                     48: '1250Hz', 49: '1250Hz', 50: '1250Hz', 51: '1250Hz', 52: '1250Hz', 53: '1250Hz', 54: '1250Hz',
                     55: '1250Hz', 56: '1600Hz', 57: '1600Hz', 58: '1600Hz', 59: '1600Hz', 60: '1600Hz', 61: '1600Hz',
                     62: '1600Hz', 63: '1600Hz', 64: '2000Hz', 65: '2000Hz', 66: '2000Hz', 67: '2000Hz', 68: '2000Hz',
                     69: '2000Hz', 70: '2000Hz', 71: '2000Hz', 72: '2500Hz', 73: '2500Hz', 74: '2500Hz', 75: '2500Hz',
                     76: '2500Hz', 77: '2500Hz', 78: '2500Hz', 79: '2500Hz', 80: '3150Hz', 81: '3150Hz', 82: '3150Hz',
                     83: '3150Hz', 84: '3150Hz', 85: '3150Hz', 86: '3150Hz', 87: '3150Hz', 88: '4000Hz', 89: '4000Hz',
                     90: '4000Hz', 91: '4000Hz', 92: '4000Hz', 93: '4000Hz', 94: '4000Hz', 95: '4000Hz', 96: '5000Hz',
                     97: '5000Hz', 98: '5000Hz', 99: '5000Hz', 100: '5000Hz', 101: '5000Hz', 102: '5000Hz', 103: '5000Hz',
                     104: '6300Hz', 105: '6300Hz', 106: '6300Hz', 107: '6300Hz', 108: '6300Hz', 109: '6300Hz',
                     110: '6300Hz', 111: '6300Hz', 112: '8000Hz', 113: '8000Hz', 114: '8000Hz', 115: '8000Hz',
                     116: '8000Hz', 117: '8000Hz', 118: '8000Hz', 119: '8000Hz', 120: 'Bypass', 121: 'Bypass',
                     122: 'Bypass', 123: 'Bypass', 124: 'Bypass', 125: 'Bypass', 126: 'Bypass', 127: 'Bypass'}
        )

    # PARAM_TYPE_16 - the table in manual reports 7 (page 76-77)
    #PARAM_TYPE_16 = tools.mergeRanges(range(0x00,0x64),tools.ulist(0.1,10,0.1,'s'))
    #PARAM_TYPE_16_B = tools.mergeRanges(range(0x64,0x80),tools.ulist(11,38,1,'s'))
    #PARAM_TYPE_16.update(PARAM_TYPE_16_B)
    PARAM_TYPE_16 = ({0: '0.1s', 1: '0.2s', 2: '0.3s', 3: '0.4s', 4: '0.5s', 5: '0.6s', 6: '0.7s', 7: '0.8s',
                      8: '0.9s', 9: '1.0s', 10: '1.1s', 11: '1.2s', 12: '1.3s', 13: '1.4s', 14: '1.5s',
                      15: '1.6s', 16: '1.7s', 17: '1.8s', 18: '1.9s', 19: '2.0s', 20: '2.1s', 21: '2.2s',
                      22: '2.3s', 23: '2.4s', 24: '2.5s', 25: '2.6s', 26: '2.7s', 27: '2.8s', 28: '2.9s',
                      29: '3.0s', 30: '3.1s', 31: '3.2s', 32: '3.3s', 33: '3.4s', 34: '3.5s', 35: '3.6s',
                      36: '3.7s', 37: '3.8s', 38: '3.9s', 39: '4.0s', 40: '4.1s', 41: '4.2s', 42: '4.3s',
                      43: '4.4s', 44: '4.5s', 45: '4.6s', 46: '4.7s', 47: '4.8s', 48: '4.9s', 49: '5.0s',
                      50: '5.1s', 51: '5.2s', 52: '5.3s', 53: '5.4s', 54: '5.5s', 55: '5.6s', 56: '5.7s',
                      57: '5.8s', 58: '5.9s', 59: '6.0s', 60: '6.1s', 61: '6.2s', 62: '6.3s', 63: '6.4s',
                      64: '6.5s', 65: '6.6s', 66: '6.7s', 67: '6.8s', 68: '6.9s', 69: '7.0s', 70: '7.1s',
                      71: '7.2s', 72: '7.3s', 73: '7.4s', 74: '7.5s', 75: '7.6s', 76: '7.7s', 77: '7.8s',
                      78: '7.9s', 79: '8.0s', 80: '8.1s', 81: '8.2s', 82: '8.3s', 83: '8.4s', 84: '8.5s',
                      85: '8.6s', 86: '8.7s', 87: '8.8s', 88: '8.9s', 89: '9.0s', 90: '9.1s', 91: '9.2s',
                      92: '9.3s', 93: '9.4s', 94: '9.5s', 95: '9.6s', 96: '9.7s', 97: '9.8s', 98: '9.9s',
                      99: '10.0s', 100: '11s', 101: '12s', 102: '13s', 103: '14s', 104: '15s', 105: '16s',
                      106: '17s', 107: '18s', 108: '19s', 109: '20s', 110: '21s', 111: '22s', 112: '23s',
                      113: '24s', 114: '25s', 115: '26s', 116: '27s', 117: '28s', 118: '29s', 119: '30s',
                      120: '31s', 121: '32s', 122: '33s', 123: '34s', 124: '35s', 125: '36s', 126: '37s', 127: '38s'})
    
    
    # Those are funny. Non capire O~O
    #BALANCE_VALUES=(['D0<E','D1<E','D3<E','D4<E','D6<E','D7<E','D9<E','D11<E','D12<E','D14<E','D<E',
    #                 'D15<E','D17<E','D19<E','D20<E','D22<E','D23<E','D25<E','D26<E','D28<E','D30<E',
    #                 'D31<E','D33<E','D34<E','D36<E','D38<E','D39<E','D41<E','D42<E','D44<E','D46<E',
    #                 'D47<E','D49<E','D50<E','D52<E','D53<E','D55<E','D57<E','D58<E','D60<E','D61<E',
    #                 'D63<E','D65<E','D66<E','D68<E','D69<E','D71<E','D73<E','D74<E','D76<E','D77<E',
    #                 'D79<E','D80<E','D82<E','D84<E','D85<E','D87<E','D88<E','D90<E','D92<E','D93<E',
    #                 'D<E','D95<E','D96<E','D98<E','D=E','D>98E','D>96E','D>95E','D>93E','D>92E',
    #                 'D>90E','D>88E','D>87E','D>85E','D>84E','D>82E','D>80E','D>79E','D>77E','D>76E',
    #                 'D>74E','D>73E','D>71E','D>69E','D>68E','D>66E','D>65E','D>63E','D>61E','D>60E',
    #                 'D>58E','D>57E','D>55E','D>53E','D>52E','D>50E','D>49E','D>47E','D>46E','D>44E',
    #                 'D>42E','D>41E','D>39E','D>38E','D>36E','D>34E','D>33E','D>31E','D>30E','D>28E',
    #                 'D>26E','D>25E','D>23E','D>22E','D>20E','D>19E','D>17E','D>15E','D>14E','D>12E',
    #                 'D>11E','D>9E','D>7E','D>6E','D>4E','D>3E','D>1E','D>0E'])
    BALANCE_VALUES = ({0: 'D>0E', 1: 'D>0E', 2: 'D>1E', 3: 'D>3E', 4: 'D>4E', 5: 'D>6E', 6: 'D>7E',
                       7: 'D>9E', 8: 'D>11E', 9: 'D>12E', 10: 'D>14E', 11: 'D>15E', 12: 'D>17E',
                       13: 'D>19E', 14: 'D>20E', 15: 'D>22E', 16: 'D>23E', 17: 'D>25E', 18: 'D>26E',
                       19: 'D>28E', 20: 'D>30E', 21: 'D>31E', 22: 'D>33E', 23: 'D>34E', 24: 'D>36E',
                       25: 'D>38E', 26: 'D>39E', 27: 'D>41E', 28: 'D>42E', 29: 'D>44E', 30: 'D>46E',
                       31: 'D>47E', 32: 'D>49E', 33: 'D>50E', 34: 'D>52E', 35: 'D>53E', 36: 'D>55E',
                       37: 'D>57E', 38: 'D>58E', 39: 'D>60E', 40: 'D>61E', 41: 'D>63E', 42: 'D>65E',
                       43: 'D>66E', 44: 'D>68E', 45: 'D>69E', 46: 'D>71E', 47: 'D>73E', 48: 'D>74E',
                       49: 'D>76E', 50: 'D>77E', 51: 'D>79E', 52: 'D>80E', 53: 'D>82E', 54: 'D>84E',
                       55: 'D>85E', 56: 'D>87E', 57: 'D>88E', 58: 'D>90E', 59: 'D>92E', 60: 'D>93E',
                       61: 'D>95E', 62: 'D>96E', 63: 'D>98E', 64: 'D=E', 65: 'D98<E', 66: 'D96<E',
                       67: 'D95<E', 68: 'D93<E', 69: 'D92<E', 70: 'D90<E', 71: 'D88<E', 72: 'D87<E',
                       73: 'D85<E', 74: 'D84<E', 75: 'D82<E', 76: 'D80<E', 77: 'D79<E', 78: 'D77<E',
                       79: 'D76<E', 80: 'D74<E', 81: 'D73<E', 82: 'D71<E', 83: 'D69<E', 84: 'D68<E',
                       85: 'D66<E', 86: 'D65<E', 87: 'D63<E', 88: 'D61<E', 89: 'D60<E', 90: 'D58<E',
                       91: 'D57<E', 92: 'D55<E', 93: 'D53<E', 94: 'D52<E', 95: 'D50<E', 96: 'D49<E',
                       97: 'D47<E', 98: 'D46<E', 99: 'D44<E', 100: 'D42<E', 101: 'D41<E', 102: 'D39<E',
                       103: 'D38<E', 104: 'D36<E', 105: 'D34<E', 106: 'D33<E', 107: 'D31<E',
                       108: 'D30<E', 109: 'D28<E', 110: 'D26<E', 111: 'D25<E', 112: 'D23<E',
                       113: 'D22<E', 114: 'D20<E', 115: 'D19<E', 116: 'D17<E', 117: 'D15<E',
                       118: 'D14<E', 119: 'D12<E', 120: 'D11<E', 121: 'D9<E', 122: 'D7<E',
                       123: 'D6<E', 124: 'D4<E', 125: 'D3<E', 126: 'D1<E', 127: 'D0<E'})


    
    # Let's initialise the dictionaries with the parameters.
    FULL_EFX_TYPE = {}
    FULL_EFX_PARAMETERS={}
    
    
    # FULL EFFECT MODE
    FULL_EFX_TYPE[1] = ('High Quality Reverb',[0x00,0x11])
    # FULL_EFX_PARAMETERS[]: How to build them (brainstorming) [in ITALIAN, sorry]
    # Mi servono anche i range in forma umana oltre a quelli esadecimali per il SYSEX, in modo che lo spinbox mostri il valore umano e passi
    # il valore esadecimale.
    # al momento, se FULL_EFX_PARAMETERS[x] = par, abbiamo:
    # par[0]: nome del parametro (es. 'Reverb Time');
    # par[1]: range indicativo in forma 'umana' - lo metto in colonna 3 del QtreeWidgetItem
    # par[2]: range esadecimale completo dei valori che puo' assumere il parametro -> quello che passo al SYSEX
    # **** ora ho fatto diventare par[2] a sua volta un dizionario in cui la chiave e' il valoroa esadecimale da passare mentre l'argomento e' il valore 'umano'
    # **** **** ad esempio: {0: '0ms', 1: '1ms'}
    # par[3]: LSB/MSB del parametro -> da passare al SYSEX
    # par[4]: metto il valore di default
    #
    # posso
    # 1. aggiungere quindi una colonna in cui inserisco una tupla dei valori 'umani'.
    # 2. modificare par[2] facendolo diventare un dizionario nella forma {valore_hex: valore umano}
    
    # BACKUP del parametro "vecchio"
    #FULL_EFX_PARAMETERS[1] = ( ('Type','Room1/2/Plate1/2/Hall1/2',range(0x00,0x06), [0x03]),\
    #    ('Pre Dly','0ms - 80ms - 635ms', range(0x00,0x80), [0x04]),\
    #    ('Reverb Time','0.1s - 2s - 38s',range(0x00,0x80), [0x05]),\
    #    ('HF Damp','-10 - -4 -0', range(0x00,0x0B), [0x06]),\
    #    ('ER Pre Dly', '0 - 40ms - 635 ms', range(0x00,0x80), [0x07]),\
    #    ('ER Mix','0 - 15 - 127', range(0x00,0x80), [0x08]),\
    #    ('Diffusion','0 - 9 - 10',range(0x00,0x0B),[0x09]),\
    #    ('Tone Low','-12dB - 0dB - +12dB',range(0x34,0x4D),[0x0A]),\
    #    ('Tone High','-12dB - 0dB - +12dB',range(0x34,0x4D),[0x0B]),\
    #    ('Balance','D > 0E - D0 < E', range(0x00,0x80), [0x0C])
    #)
    
    # parametro di lavoro
    # l'implementazione attuale ha in par[2] un dizionario con associati i valori hex a quelli umani...
    FULL_EFX_PARAMETERS[1] = ( ('Type','Room1/2/Plate1/2/Hall1/2',tools.mergeRanges(range(0x00,0x06),['Room1','Room2','Plate1','Plate2','Hall1','Hall2']), [0x03],0x03),\
        ('Pre Dly','0ms - 80ms - 635ms', PARAM_TYPE_5, [0x04], 0x10),\
        ('Reverb Time','0.1s - 2s - 38s',PARAM_TYPE_16, [0x05],0x13),\
        ('HF Damp','-10 - -4 -0', tools.mergeRanges(range(0x00,0x0B),tools.ulist(-10,0,1)), [0x06], 0x06),\
        ('ER Pre Dly', '0 - 40ms - 635 ms', PARAM_TYPE_5, [0x07], 0x08),\
        ('ER Mix','0 - 15 - 127', tools.mergeRanges(range(0x00,0x80),tools.ulist(0,127,1)), [0x08],0x0f),\
        ('Diffusion','0 - 9 - 10', tools.mergeRanges(range(0x00,0x0B),tools.ulist(0,10,1)),[0x09],0x09),\
        ('Tone Low','-12dB - 0dB - +12dB',tools.mergeRanges(range(0x34,0x4D), tools.ulist(-12,+12,1,'dB')),[0x0A], 0x40),\
        ('Tone High','-12dB - 0dB - +12dB',tools.mergeRanges(range(0x34,0x4D), tools.ulist(-12,+12,1,'dB')),[0x0B],0x40),\
        ('Balance','D > 0E - D0 < E', BALANCE_VALUES, [0x0C],0x7f)
    )

    #FULL_EFX_TYPE[2] = ('Mic Simulator',[0x00,0x12])
    #FULL_EFX_PARAMETERS[2] = ()
    #FULL_EFX_TYPE[3] = ('Vocoder',[0x00,0x13])
    #FULL_EFX_TYPE[4] = ('Vocal Multi',[0x00,0x14])
    #FULL_EFX_TYPE[5] = ('Game',[0x00,0x16])
    #FULL_EFX_TYPE[6] = ('Rotary Multi',[0x03,0x00])
    #FULL_EFX_TYPE[7] = ('GTR Multi',[0x04,0x00])
    
    
    # COMPACT EFFECTS MODE
    # Let's define the SYS first. They are actually a bit easier.
    
    # REMEMBER: SYS1 only has DELAY and CHORUS
    #           SYS2 only has DELAY and REVERB
    # THIS MEANS: we must differentiate the two of them somehow. Fuck.
    
    COMPACT_SYS1_EFX_TYPE = ({1: ('Delay',[0x00, 0x21]),
                             2: ('Chorus', [0x00, 0x22])})
    COMPACT_SYS2_EFX_TYPE = ({1: ('Delay', [0x00, 0x31]),
                              2: ('Reverb', [0x00, 0x32])})
    
    
    
    COMPACT_SYS1_EFX_PARAMETERS={}
    
    COMPACT_SYS1_EFX_PARAMETERS[1] = (
        ('Dly Tm LtoL', '0.0ms - 110ms - 360ms',PARAM_TYPE_4_SHORT, [0x03], 97),
        ('Dly Tm LtoR', '0.0ms - 13.0ms - 360ms',PARAM_TYPE_4_SHORT, [0x04], 63),
        ('Dly Tm RtoR', '0.0ms - 100ms - 360ms',PARAM_TYPE_4_SHORT, [0x05], 96),
        ('Dly Tm RtoL', '0.0ms - 8.0ms - 360ms',PARAM_TYPE_4_SHORT, [0x06], 56),
        ('Feedback Level', '-48% - -34% - +48%', tools.mergeRanges(range(0x28,0x59),tools.ulist(-48,+48,2,'%')), [0x07],0x36),
        ('Cross Fd Level', '-48% - -34% - +48%', tools.mergeRanges(range(0x28,0x59),tools.ulist(-48,+48,2,'%')), [0x08],0x4A),
        ('HF Damp','315Hz - 8kHz/Bypass',PARAM_TYPE_8,[0x09],120),
        ('Cross HF Damp','315Hz - 6.3kHz - 8kHz/Bypass',PARAM_TYPE_8,[0x0A],104),
        ('Cross Balance','0-98-127',tools.mergeRanges(range(0x00,0x80),tools.ulist(0,127,1)), [0x0B], 0x62),
        ('Balance','D > 0E - D0 < E',BALANCE_VALUES,[0x0C],0x7F)
    )
    
    COMPACT_SYS1_EFX_PARAMETERS[2] = (
        ('Type','Mode1 -2 -4',tools.mergeRanges(range(0x00,0x04),['Mode1','Mode2','Mode3','Mode4']),[0x03], 0x01),
        ('Pre Filter','Off/LPF/HPF', tools.mergeRanges(range(0x00,0x03),['Off','LPF','HPF']),[0x04], 0x02),
        #('Cutoff'),
        ('Pre Dly','0ms - 100ms', PARAM_TYPE_1, [0x06], 80),
        #('Rate'),
        ('Depth', '0-116-127',tools.mergeRanges(range(0x00,0x80),tools.ulist(0,127,1)),[0x08], 0x74),
        ('Balance','D > 0E - D0 < E',BALANCE_VALUES,[0x09],0x7F)
    )
    COMPACT_SYS2_EFX_PARAMETERS={}
    
    COMPACT_SYS2_EFX_PARAMETERS[1] = (
        ('Dly Tm LtoL', '0.0ms - 110ms - 360ms',PARAM_TYPE_4_SHORT, [0x03], 97),
        ('Dly Tm LtoR', '0.0ms - 13.0ms - 360ms',PARAM_TYPE_4_SHORT, [0x04], 63),
        ('Dly Tm RtoR', '0.0ms - 100ms - 360ms',PARAM_TYPE_4_SHORT, [0x05], 96),
        ('Dly Tm RtoL', '0.0ms - 8.0ms - 360ms',PARAM_TYPE_4_SHORT, [0x06], 56),
        ('Feedback Level', '-48% - -34% - +48%', tools.mergeRanges(range(0x28,0x59),tools.ulist(-48,+48,2,'%')), [0x07],0x36),
        ('Cross Fd Level', '-48% - -34% - +48%', tools.mergeRanges(range(0x28,0x59),tools.ulist(-48,+48,2,'%')), [0x08],0x4A),
        ('HF Damp','315Hz - 8kHz/Bypass',PARAM_TYPE_8,[0x09],120),
        ('Cross HF Damp','315Hz - 6.3kHz - 8kHz/Bypass',PARAM_TYPE_8,[0x0A],104),
        ('Cross Balance','0-98-127',tools.mergeRanges(range(0x00,0x80),tools.ulist(0,127,1)), [0x0B], 0x62),
        ('Balance','D > 0E - D0 < E',BALANCE_VALUES,[0x0C],0x7F)
    )
    
    COMPACT_SYS2_EFX_PARAMETERS[2] = (
        ('Type','Room1/2/Plate1/2/Hall1/2',tools.mergeRanges(range(0x00,0x06),['Room1','Room2','Plate1','Plate2','Hall1','Hall2']), [0x03],0x05),
        ('Pre Dly','0ms - 100ms', PARAM_TYPE_1, [0x04], 0x7F),
        ('Reverb Time','0 - 23 - 127',tools.mergeRanges(range(0x00,0x80),tools.ulist(0,127,1)), [0x05],0x17),
        #('HF Damp'),
        #('Low Gain'),
        #('High Gain'),
        ('Balance','D > 0E - D0 < E',BALANCE_VALUES,[0x09],0x7F)
    )
    
    # Now we must define the COMPACT INSERTION EFFECT.
    # Remember: they are grouped, as in the documentation
    
    COMPACT_INS_EFX_TYPE={}
    COMPACT_INS_EFX_PARAMETERS={}
    
    # End of exclusive (EOX)
    EOX = [0xF7]
    
    
    

if (DEBUG_MODE):
    print('Done!')

class MidiDevsDialog(QtGui.QDialog):
    
    def __init__(self, parent = None):
        super(MidiDevsDialog,self).__init__(parent)
        
        self.ui = PyQt4.uic.loadUi('ui/device_sel.ui', self)
        
        if (DEBUG_MODE):
            print('DEFAULT_UA100CONTROL= ',DEFAULT_UA100CONTROL)
            print('midiDevs=', midiDevs)
        for i in range(0,len(midiDevs)):
            self.outputDevicesList.addItem(str(midiDevs[i]), i)
        
        # update the device information when selecting the devices in the combobox
        self.outputDevicesList.currentIndexChanged.connect(self.updateDeviceLabels)
        
        # call the setMidiDevice custom slot to tell everyone whitch one is the selected device (output)
        self.outputDevicesList.currentIndexChanged.connect(self.setMidiDevice)
        
        # send true if OK is clicked
        self.dialogOK.clicked.connect(self.accept)
        
        # send false if Quit is clicked (and close application)
        self.dialogQuit.clicked.connect(self.reject)
        
        # set the current index to the guessed right outpud midi device for the UA100 controller
        if (REAL_UA_MODE):
            self.outputDevicesList.setCurrentIndex(DEFAULT_UA100CONTROL)
    
    def updateDeviceLabels(self, index):
        '''
        I should be an easy task to update label according to a combo box...
        '''
        self.midiApiText.setText(str(midiDevs[index][0]))
        self.deviceNameText.setText(str(midiDevs[index][1]))
        if (midiDevs[index][2] == 1 and midiDevs[index][3] == 0):
            self.deviceIOText.setText('INPUT')
        elif (midiDevs[index][2] == 0 and midiDevs[index][3] == 1):
            self.deviceIOText.setText('OUTPUT')
        else:
            self.deviceIOText.setText('N/A')
        
        if (index == DEFAULT_UA100CONTROL):
            self.reccomendedLabel.setText('RECCOMENDED!\r\nYou don\'t really want to change it!')
            self.reccomendedLabel.setStyleSheet('color: red; font-style: bold')
        else:
            self.reccomendedLabel.setText('')
        
        if (DEBUG_MODE == 1):
            print(midiDevs[index][2], midiDevs[index][3])
            
    def setMidiDevice(self, index):
        '''
        This slot should set the midi device selected in the combo box of the starting dialog
        '''
        global UA100CONTROL
        
        UA100CONTROL=index
        if (DEBUG_MODE ==1):
            print('Index = ', index)
            print('UA100CONTROL = ',UA100CONTROL)



class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        
        # load the ui
        self.ui = PyQt4.uic.loadUi('ui/main.ui', self)
        
        self.fullEffects = {}
        self.compactEffectsSys = {}
        
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
        
        # Setting up Ins1&2
        self.Mic2Ins1.valueChanged.connect(functools.partial(self.valueChange, CC_MIC2_CH, CC_SEND1_PAR))
        self.Mic2Ins2.valueChanged.connect(functools.partial(self.valueChange, CC_MIC2_CH, CC_SEND2_PAR))
        
        # Setting Up the Mic2 Solo Button ** THEY CAN BE ONLY ONE SOLO CHECKED, THUS... **
        #self.mic2Solo.toggled.connect(functools.partial(self.uniqueSolos, self, window, self.mic2Solo, 2))
        #self.mic2Solo.toggled.connect(functools.partial(self.uniqueSolos, self.mic1Solo, self.wave1Solo, self.wave2Solo))
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
        #self.Wave1Fader.setProperty("value", CC_0127_DEFAULT)
        self.Wave1Fader.setProperty("parameter", CC_MAIN_FADER_PAR)
        
        # Setting up Ins1&2
        self.Wave1Ins1.valueChanged.connect(functools.partial(self.valueChange, CC_WAVE1_CH, CC_SEND1_PAR))
        self.Wave1Ins2.valueChanged.connect(functools.partial(self.valueChange, CC_WAVE1_CH, CC_SEND2_PAR))
        
        # Setting Up the Wave1 Solo Button ** THEY CAN BE ONLY ONE SOLO CHECKED, THUS... **
        #self.wave1Solo.toggled.connect(functools.partial(self.uniqueSolos, self, window, self.wave1Solo, 3))
        #self.wave1Solo.toggled.connect(functools.partial(self.uniqueSolos, self.mic1Solo, self.wave2Solo, self.mic2Solo))
        self.Wave1Solo.toggled.connect(self.uniqueSolos)
        self.Wave1Mute.toggled.connect(functools.partial(self.valueChange, CC_WAVE1_CH, CC_MUTE_PAR))
        
        # Setting Up the SubFader
        self.Wave1SubFader.valueChanged.connect(self.Wave1SubLcd.display)
        self.Wave1SubFader.valueChanged.connect(functools.partial(self.valueChange,CC_WAVE1_CH, CC_SUB_FADER_PAR))
        
        # hiding the subs...
        self.Wave1SubFader.hide()
        self.Wave1SubLcd.hide()
        
            # *************** WAVE2 *********************
    
        self.Wave2.setProperty("channel", CC_WAVE2_CH)
        
        # Setting up the Wave1 Fader
        self.Wave2Fader.valueChanged.connect(self.Wave2Lcd.display)
        self.Wave2Fader.valueChanged.connect(functools.partial(self.valueChange, CC_WAVE2_CH, CC_MAIN_FADER_PAR))
        #self.Wave2Fader.setProperty("value", CC_0127_DEFAULT)
        self.Wave2Fader.setProperty("parameter", CC_MAIN_FADER_PAR)    
        
        # Setting up Ins1&2
        self.Wave2Ins1.valueChanged.connect(functools.partial(self.valueChange, CC_WAVE2_CH, CC_SEND1_PAR))
        self.Wave2Ins2.valueChanged.connect(functools.partial(self.valueChange, CC_WAVE2_CH, CC_SEND2_PAR))
        
        # Setting Up the Wave2 Solo Button ** THEY CAN BE ONLY ONE SOLO CHECKED, THUS... **
        #self.wave2Solo.toggled.connect(functools.partial(uniqueSolos, self, window, self.wave1Solo, 4))
        #self.wave2Solo.toggled.connect(functools.partial(uniqueSolos, self.mic1Solo, self.wave1Solo, self.mic2Solo))
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
        self.MasterLineFader.valueChanged.connect(functools.partial(self.valueChange, CC_LINE_MASTER_CH, CC_MAIN_FADER_PAR))
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
        self.OutputMasterSourceSelect.currentIndexChanged.connect(functools.partial(self.valueChange, CC_LINE_MASTER_CH, CC_SELECTOR_PAR))
        if (MIXER_OUTPUT_MODE):
            for key in MASTER_SELECT_MIXERMODE.keys():
                self.OutputMasterSourceSelect.addItem(MASTER_SELECT_MIXERMODE[key])
            self.OutputMasterSourceSelect.setCurrentIndex(0x09)
            
        # Setting Up Mixer Output Sources for Wave(Rec)
        self.OutputWaveRecSourceSelect.currentIndexChanged.connect(functools.partial(self.valueChange, CC_WAVEREC_CH, CC_SELECTOR_PAR))
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
        
        
        #self.EffWave2Button.clicked.connect(setEff2)
        #self.EffMic2Button.clicked.connect(effOn)
        
        if (REAL_UA_MODE):
            self.__setInitMixerLevels__()
        
        self.uiInputModeButton.setProperty('state',0x00)
        self.uiInputModeButton.clicked.connect(self.setInputMode)
    
    def setInputMode(self):
        '''
        
        The MIC1-GUITAR/LINE/MIC1+MIC2 toggler
        
        need a tree way button...
        
        '''
        
        if self.sender().property('state') == 0x00:
            self.sender().setProperty('state',0x01)
            self.Mic1.setTitle('Line')
            self.uiInputModeLabel.setText('Line')
            self.Mic2.hide()
        elif self.sender().property('state') == 0x01:
            self.sender().setProperty('state',0x02)
            self.Mic1.setTitle('Mic1/Guitar+Mic2')
            self.uiInputModeLabel.setText('Mic1\n+Mic2')
            self.Mic2.hide()
        elif self.sender().property('state') == 0x02:
            self.sender().setProperty('state',0x00)
            self.Mic1.setTitle('Mic1/Guitar')
            self.uiInputModeLabel.setText('Mic/\nGuitar')
            self.Mic2.show()
        if (REAL_UA_MODE):
            pmout.write_short(CC_MIC1_CH,CC_MICLINESELECTOR_PAR, self.sender().property('state').toPyObject() )
            
        if (DEBUG_MODE):
            print(CC_MIC1_CH,' ',CC_MICLINESELECTOR_PAR,' ',self.sender().property('state').toPyObject() )  
    
    def setEffectMode(self, value):
        global MixerEffectMode
        valueToList=[sorted(MIXER_EFFECT_MODE_PAR.keys())[value]]
        #if (DEBUG_MODE):
        #    print(valueToList)
        send_DT1(MIXER_EFFECT_CONTROL + MIXER_EFFECT_MODE + valueToList)
        MixerEffectMode=sorted(MIXER_EFFECT_MODE_PAR.keys())[value]
        
    
    def effectSelection(self):
        global MixerEffectMode
        #if (DEBUG_MODE):
        #    print(self.sender().objectName())
        if (MixerEffectMode == 0x04):
            #if not (self.sender() in self.fullEffects):
            #    self.fullEffects[self.sender()] = FullEffectsDialog(self)
            #self.fullEffects[self.sender()].show()
            if (self.fullEffects):
                self.fullEffects.uiToggleEffect.setChecked(0)
                self.fullEffects.close()
                self.fullEffects = FullEffectsDialog(self)
                self.fullEffects.uiToggleEffect.setChecked(1)
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
            else:
                pass
            
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

    def valueChange(self,a,b,val):
        '''
        custom slot to connect to the changes in the interface with write_short to send the control change messages
        '''
        
        if (REAL_UA_MODE):
            pmout.write_short(a,b,val)
            
        if (DEBUG_MODE == 1):
            print(hex(a),b,val)   
    
    def uniqueSolos(self, checked):
        '''
        unchecks all other solo buttons if the present is checked.
        besides, it actually soloes/unsoloes the channel
        '''
        
        soloers =['Mic1','Mic2','Wave1','Wave2']
        soloers.remove(str(self.sender().parent().objectName()))
        if (checked):
            if (DEBUG_MODE == 1):
                print(soloers)
                print('unchecking and desoloing ')
                print('soloing ',str(self.sender().parent().objectName()))
            if (REAL_UA_MODE):
                pmout.write_short(self.sender().parent().property('channel').toPyObject(),CC_SOLO_PAR,1)
            for soloer in soloers:
                soloingObj = self.findChild(QtGui.QGroupBox, soloer)
                if (REAL_UA_MODE):
                    pmout.write_short(soloingObj.property('channel').toPyObject(),CC_SOLO_PAR,0)
                soloingButtonStr = soloer+'Solo'
                nomuteButtonStr = soloer+'Mute'
                #print soloingButtonStr
                soloingButton = soloingObj.findChild(QtGui.QPushButton, soloingButtonStr)
                nomuteButton = soloingObj.findChild(QtGui.QPushButton, nomuteButtonStr)
                soloingButton.setChecked(False)
                nomuteButton.hide()
                if (DEBUG_MODE):
                    # review those fucking debug messages. They are just fucking messed up!
                    print('desoloing: ',soloingObj.objectName())
                    print(soloingObj.property('channel').toPyObject())
        else:
            for soloer in soloers:
                soloingObj = self.findChild(QtGui.QGroupBox, soloer)
                remuteButtonStr = soloer+'Mute'
                remuteButton = soloingObj.findChild(QtGui.QPushButton, remuteButtonStr)
                remuteButton.show()
            if (REAL_UA_MODE):
                pmout.write_short(self.sender().parent().property('channel').toPyObject(),CC_SOLO_PAR,0)
            else:
                print('pmout.write_short(',self.sender().parent().property('channel').toPyObject(),',',CC_SOLO_PAR,'0)')
    
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
        #self.Wave1SubFader.setProperty("value", CC_0127_DEFAULT)
        self.Wave2Fader.setProperty("value", CC_0127_DEFAULT)
        #self.Wave2SubFader.setProperty("value", CC_0127_DEFAULT)
        self.Mic1Fader.setProperty("value", CC_0127_DEFAULT)
        self.Mic1Pan.setProperty("value", CC_0127_DEFAULT)
        #self.Mic1SubFader.setProperty("value", CC_0127_DEFAULT)
        self.Mic2Fader.setProperty("value", CC_0127_DEFAULT)
        self.Mic2Pan.setProperty("value", CC_0127_DEFAULT)
        #self.Mic2SubFader.setProperty("value", CC_0127_DEFAULT)
        self.WaveRecFader.setProperty("value", CC_0127_DEFAULT)

    def __setInitMixerLevels__(self):
        '''
        It works. It send SYSEX and reads answers. But there must me a better way to read and write.
        Actually there is, but I'm lazy.
        '''
    
        send_RQ1(MIXER_OUTPUT_CONTROL + MIXER_OUTPUT_MASTERLEVEL + MIXER_OUTPUT_MASTERLEVEL_SIZE)
        time.sleep(SLEEP_TIME)
        answerList = sysexRead(4)
        masterLevel= answerList[2][0][2]
        self.MasterLineFader.setProperty("value", masterLevel)
        
        send_RQ1(MIXER_OUTPUT_CONTROL + MIXER_OUTPUT_WAVEREC + MIXER_OUTPUT_WAVEREC_SIZE)
        time.sleep(SLEEP_TIME)
        answerList = sysexRead(4)
        waverecLevel= answerList[2][0][2]
        self.WaveRecFader.setProperty("value", waverecLevel)
        
        send_RQ1(MIC1_FADER + MIC1_FADER_SIZE)
        time.sleep(SLEEP_TIME)
        answerList = sysexRead(4)
        mic1Level= answerList[2][0][2]
        self.Mic1Fader.setProperty("value", mic1Level)
        
        send_RQ1(MIC2_FADER + MIC2_FADER_SIZE)
        time.sleep(SLEEP_TIME)
        answerList = sysexRead(4)
        mic2Level= answerList[2][0][2]
        self.Mic2Fader.setProperty("value", mic2Level)
        
        send_RQ1(WAVE1_FADER + WAVE1_FADER_SIZE)
        time.sleep(SLEEP_TIME)
        answerList = sysexRead(4)
        wave1Level= answerList[2][0][2]
        self.Wave1Fader.setProperty("value", wave1Level)
        
        send_RQ1(WAVE2_FADER + WAVE2_FADER_SIZE)
        time.sleep(SLEEP_TIME)
        answerList = sysexRead(4)
        wave2Level= answerList[2][0][2]
        self.Wave2Fader.setProperty("value", wave2Level)
        
        
        # This should read the INPUT MODE and set the starting value accordingly. But I must think a way to do setInputMode better.
        #send_RQ1(MIXER_INPUT_CONTROL + MIXER_INPUT_MODE + MIXER_INPUT_MODE_SIZE)
        #time.sleep(SLEEP_TIME)
        #answerList = sysexRead(4)
        #mixerMode = answerList[2][0][2]
        #self.uiInputModeButton.setProperty('state',mixerMode)
        
        #if (DEBUG_MODE):
        #    print(answerList)

class CompactEffectsSysDialog(QtGui.QDialog):
    def __init__(self,parent = None):
        super(CompactEffectsSysDialog,self).__init__(parent)
        # here is where I store the channel choosen fo the effect (mic1, mic2, wave1, wave2, sys1, sys2)
        self.SenderHex = parent.sender().property('HEX').toPyObject()
        # load the ui...
        self.ui = PyQt4.uic.loadUi('ui/compacteffectssysdialog.ui', self)
        if self.SenderHex == [0x05]:
            self.setWindowTitle('System 1 - '+self.windowTitle())
            self.uiEffectTypeList.addItem(COMPACT_SYS1_EFX_TYPE[1][0])
            self.uiEffectTypeList.addItem(COMPACT_SYS1_EFX_TYPE[2][0])
        elif self.SenderHex == [0x06]:
            self.setWindowTitle('System 2 - '+self.windowTitle())
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
            if (DEBUG_MODE):
                print([0x00, 0x40] + self.SenderHex + [0x00] + COMPACT_SYS1_EFX_TYPE[index+1][1])
            send_DT1([0x00, 0x40] + self.SenderHex + [0x00] + COMPACT_SYS1_EFX_TYPE[index+1][1])
            for par in COMPACT_SYS1_EFX_PARAMETERS[index+1]:
                item = CustomTreeItem(self.uiEffectParameters, par, index)
        elif (self.SenderHex == [0x06]):
            if (DEBUG_MODE):
                print([0x00, 0x40] + self.SenderHex + [0x00] + COMPACT_SYS2_EFX_TYPE[index+1][1])
            send_DT1([0x00, 0x40] + self.SenderHex + [0x00] + COMPACT_SYS2_EFX_TYPE[index+1][1])
            for par in COMPACT_SYS2_EFX_PARAMETERS[index+1]:
                item = CustomTreeItem(self.uiEffectParameters, par, index)
        
        
    def setEffect(self, checked):
        '''
        A small but invaluable function:
        
        IT SWITCHES THE WHOLE THIG ON!
        '''
        
        if (DEBUG_MODE):
            print(self.SenderHex)
        if (checked):
            checkedList= [0x01]
        else:
            checkedList= [0x00]
        send_DT1([0x00, 0x40, 0x40] + self.SenderHex + checkedList)
    
    def sendEffect(self, value):
        '''
        We send the values set to the UA-100. The effects are only active when also the switch is checked.
        '''
        
        # first of all convert the passed value to list in order to send the SYSEX message
        valueToList = [value]
        if (DEBUG_MODE):
            print 'LSB/MSB for parameter:', self.sender().property('HEX').toPyObject()
        
        
        # if in real mode, actually send the message
        send_DT1([0x00, 0x40] + self.SenderHex + self.sender().property('HEX').toPyObject() + valueToList)
        
class FullEffectsDialog(QtGui.QDialog):
    '''
    The full effect dialog.
    For every single effect selected, I should check if there are already instances for the effect. If not, generate it, if yes, use the old ones.
    BUT after I clead the QTreeWidget the instances of the QTreeWidgetItems get deleted. There should be a better way.
    To achieve this, sadly, we need to classify the items...
    '''
    
    def __init__(self,parent = None):
        super(FullEffectsDialog,self).__init__(parent)
        
        # here is where I store the channel choosen fo the effect (mic1, mic2, wave1, wave2, sys1, sys2)
        self.SenderHex = parent.sender().property('HEX').toPyObject()
        
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
        
        if (DEBUG_MODE):
            print(self.SenderHex)
        if (checked):
            checkedList= [0x01]
        else:
            checkedList= [0x00]
        send_DT1([0x00, 0x40, 0x40] + self.SenderHex + checkedList)
    
    def populateEffect(self, index):
        
        # first af all, sent the effect type to the UA-100
        # This is the LSB/MSB of the effect type (i.e. High Quality Reverb, Mic Simulator) aka the FULL_EFX_TYPE[n][1] (hex value)
        if (DEBUG_MODE):
            print([0x00, 0x40] + self.SenderHex + [0x00] + FULL_EFX_TYPE[index+1][1])
        send_DT1([0x00, 0x40] + self.SenderHex + [0x00] + FULL_EFX_TYPE[index+1][1])
        
        
        self.uiEffectParameters.clear()
        # check if the list isn't yet there... but, as said, the instances are deleted... so what? and How?
        #if not (index in self.effectList):
        #    self.effectList[index]={}
        #    for par in FULL_EFX_PARAMETERS[index+1]:
        #        self.effectList[index][par[0]] = CustomTreeItem(self.uiEffectParameters, par)
        #else:
        #    print self.effectList[index]
        #    for item in self.effectList[index]:
        #        self.uiEffectParameters.addTopLevelItem(self.effectList[index][item])
        
        # "anonimously" polulate the QTreeWidget ...
        for par in FULL_EFX_PARAMETERS[index+1]:
            item = CustomTreeItem(self.uiEffectParameters, par, index)
    
    def sendEffect(self, value):
        '''
        We send the values set to the UA-100. The effects are only active when also the switch is checked.
        '''
        
        # first of all convert the passed value to list in order to send the SYSEX message
        valueToList = [value]
        if (DEBUG_MODE):
            print 'LSB/MSB for parameter:', self.sender().property('HEX').toPyObject()
        
        
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
    def __init__( self, parent, par, index ):
        '''
        parent (QTreeWidget) : Item's QTreeWidget parent.
        name   (str)         : Item's name. just an example.
        '''
 
        ## Init super class ( QtGui.QTreeWidgetItem )
        super( CustomTreeItem, self ).__init__( parent )
        self.par= par
        self.setText(0,par[0])
        self.spinBox = QtGui.QSpinBox(parent)
        self.spinBox.setProperty('HEX', par[3])
        #self.spinBox.setValue(5)
        
        # nell'implementazione con par[2] dizionario questa riga non va bene...
        #self.spinBox.setRange(min(par[2]), max(par[2]))
        # devo usare par[2].keys()
        self.spinBox.setRange(min(par[2].keys()),max(par[2].keys()))
        
        
        self.spinBox.setWrapping(1)
        parent.setItemWidget(self,1, self.spinBox)
        self.setText(3,par[1])
        self.spinBox.valueChanged.connect(parent.parent().sendEffect)
        self.spinBox.valueChanged.connect(self.setActualValue)
        self.spinBox.setValue(par[4])
    
    def setActualValue(self, value):
        self.setText(2,self.par[2][value])

def actualMidiDevices():
    '''
    This should enumerate the devices to (later on) give then the possibility to choose one or guess the right one
    Returns a dictionary with tuples like 
    
    midiDevs = { 0: (tuple), 1: (tuple), ... }
    
    where the tuple is in the format:
    
    ('ALSA', 'UA-100 MIDI 2', 0, 1, 0)
    
    '''
    # Count the MIDI devices connected
    if (REAL_UA_MODE):
        numDevs = pm.get_count()
    else:
        numDevs = 5 
    # Initialize the device dictionary
    # midiDevs = { 0: (tuple), 1: (tuple), ... }
    #
    midiDevs = {}
    for dev in range(0,numDevs):
        # the portmidi get_device_info() returns a tuple
        if (REAL_UA_MODE):
            midiDevs[dev]=pm.get_device_info(dev)
        else:
            # fake entries...
            midiDevs[dev]=('pippo','pluto',1,1,1)
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
                print('Trovato! Il controller e il device ',i, ', ovvero ',midiDevs[i][1])
            return int(i)

     
def sysexRead(buffer_size):
    global pmin
    
    if (REAL_UA_MODE):
        answer = pmin.read(buffer_size)
    else:
        answer = CC_0127_DEFAULT
    
    return answer
    
    
def send_RQ1(data):
    '''
    Here we are about to send a Request Data 1.
    Never forget to checksum!
    
    ** Note
    The first part of the message is fixed. What can change is the data (of course, it's function agument!)
    AND the checksum, which on his side, depends on the data.
    '''
    global pmout, pmin
    checksum_result = checksum(data)
    message = RQ1_STATUS \
              +UA_SYSEX_ID \
              + RQ1_COMMAND \
              + data \
              + checksum_result\
              + EOX
    if (REAL_UA_MODE):
        pmout.write_sys_ex(pm.time(),message)

def send_DT1(data):
    global pmout, pmin
    checksum_result = checksum(data)
    message = DT1_STATUS \
              +UA_SYSEX_ID \
              + DT1_COMMAND \
              + data \
              + checksum_result\
              + EOX
    if (DEBUG_MODE):
        #print(message)
        print(np.array(message))
    if (REAL_UA_MODE):
        pmout.write_sys_ex(pm.time(),message)

def checksum(toChecksum):
    '''
    That's how the UA-100 does the checksum:
    Take the data part of SYSEXES and do the maths.
    '''
    checksum_value = (128 - (sum(toChecksum) % 128))
    checksum_list = [checksum_value]
    return list(checksum_list)

if ( __name__ == '__main__' ):
    
    # brutal way to catch the CTRL+C signal if run in the console...
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    # **************************** MIDI PART: could it go somewhere else? **********************************************
    
    # initialize the portmidi interface
    
    if (REAL_UA_MODE):
        pm.init()
        
    
    # get the list of the Midi Devices according to portmidy
    midiDevs=actualMidiDevices()
    
    if (DEBUG_MODE == 1):
        print('MIDI DEVICES FOUND: ',len(midiDevs),'. They are: ', midiDevs)
        
    # guess the right midi device
    if (REAL_UA_MODE):
        DEFAULT_UA100CONTROL = rightMidiDevice(midiDevs)
    else:
        DEFAULT_UA100CONTROL = 1
    
    if (DEBUG_MODE == 1):
        print('DEFAULT_UA100CONTROL = ',DEFAULT_UA100CONTROL)
    
    # *******************************************************************************************************************
    
    app = None
    if ( not app ):
        app = QtGui.QApplication([])
        
    dialog = MidiDevsDialog()
    dialog.show()
    
    if not dialog.exec_():
        # We quit if the the selection dialog quits
        if (DEBUG_MODE == 1):
            print('Bye.')
        sys.exit()
    
    if (DEBUG_MODE) and (REAL_UA_MODE):
        print('DEFAULT_UA100CONTROL = ',DEFAULT_UA100CONTROL)
    
    if (DEBUG_MODE):
        print('Opening device: ',DEFAULT_UA100CONTROL,' for ouput and device: ', DEFAULT_UA100CONTROL+1, 'for input')
    
    if (REAL_UA_MODE):
        # Open device for output
        pmout = pm.midi.Output(UA100CONTROL)
        # Open "the next" device for input
        pmin = pm.midi.Input(UA100CONTROL+1)
    
    window = MainWindow()
    window.show()

    if ( app ):
        app.exec_()