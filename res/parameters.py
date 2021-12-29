#!/usr/bin/python ua100mix/res/parameters.py

# All the params imported into main.py
# NOTE: this file will be imported as "from ... import *"
# I read it's acceptable to do so for constants.

import res.tools

CC_0127_DEFAULT = 64
CC_PAN_MIDDLE = 64
# I think 'in media stat virtus'


#
# The following comes from the UA-100 manual
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

CC_MICLINESELECTOR_PAR = 21  # 0x15
# CC_MICLINESELECTOR_RANGE = { 'Mic Mode': 0, 'Line Mode': 1, 'MIC1+MIC2 Mode': 2}
CC_PAN_PAR = 10  # 0x0A - 0 - 64 - 127 (LEFT - CENTER - RIGHT)
CC_SEND1_PAR = 16  # 0x10
CC_SEND2_PAR = 17  # 0x11
CC_MUTE_PAR = 18  # 0x12
CC_SOLO_PAR = 19  # 0x13
CC_SUB_FADER_PAR = 20  # 0x14
CC_MAIN_FADER_PAR = 7  # 0x70
CC_SELECTOR_PAR = 22  # 0x16
CC_EFFECTSWITHC_PAR = 23  # 0x23

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
UA_SYSEX_ID = [0x41, 0x10, 0x00, 0x11]

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
# UA100_MODE_DATARANGE = range(0x01,10)
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

# ...
MIC1_FADER = [0x00, 0x40, 0x11, 0x05]
MIC1_FADER_SIZE = [0x00, 0x00, 0x00, 0x01]
MIC2_FADER = [0x00, 0x40, 0x12, 0x05]
MIC2_FADER_SIZE = [0x00, 0x00, 0x00, 0x01]
WAVE1_FADER = [0x00, 0x40, 0x13, 0x05]
WAVE1_FADER_SIZE = [0x00, 0x00, 0x00, 0x01]
# WAVE1_FADER_RANGErange(0x00, 0x80)
WAVE2_FADER = [0x00, 0x40, 0x14, 0x05]
WAVE2_FADER_SIZE = [0x00, 0x00, 0x00, 0x01]
# ...

EFFECT_PARAMETERS = [0x00, 0x40, 0x01]

MIXER_EFFECT_CONTROL = [0x00, 0x40, 0x40]

MIXER_EFFECT_MODE = [0x00]
MIXER_EFFECT_MODE_SIZE = [0x00, 0x00, 0x00, 0x01]
MIXER_EFFECT_MODE_PAR = ({
    # 0x01: 'VT Effect Mode',
    0x03: 'Compact Effect Mode',
    0x04: 'Full Effect Mode'}
)

# Mixer Output Control
MIXER_OUTPUT_CONTROL = [0x00, 0x40, 0x50]
#
MASTER_SELECT_MIXERMODE = ({0x00: 'LINE/MIC1/MIC1+MIC2',
                            0x01: 'MIC2',
                            0x02: 'WAVE1',
                            0x03: 'WAVE2',
                            0x04: 'CH1',
                            0x05: 'CH2',
                            0x06: 'CH3',
                            0x07: 'CH4',
                            0x08: 'SUB',
                            0x09: 'MAIN',
                            0x0A: 'WAVE(REC)OUT'})
MASTER_SELECT_VTMIXERMODE = ({0x00: 'LINE/MIC1',
                              0x01: 'MIC2',
                              0x02: 'WAVE1',
                              0x03: 'WAVE2',
                              0x04: 'VT_OUT',
                              0x05: 'MAIN',
                              0x06: 'WAVE(REC)OUT'})
WAVE_SELECT_MIXERMODE = ({0x00: 'LINE/MIC1/MIC1+MIC2',
                          0x01: 'MIC2',
                          0x02: 'WAVE1',
                          0x03: 'WAVE2',
                          0x04: 'CH1',
                          0x05: 'CH2',
                          0x06: 'CH3',
                          0x07: 'CH4',
                          0x08: 'SUB',
                          0x09: 'MAIN'})
WAVE_SELECT_VTMIXERMODE = ({0x00: 'LINE/MIC1',
                            0x01: 'MIC2',
                            0x02: 'WAVE1',
                            0x03: 'WAVE2',
                            0x04: 'VT_OUT',
                            0x05: 'MAIN'})

# Mixer Output Mode:
# 0: VT MIXER MODE
# 1: MIXER MODE
MIXER_OUTPUT_MODE = 1

# ...
MIXER_OUTPUT_MASTERLEVEL = [0x03]
MIXER_OUTPUT_MASTERLEVEL_SIZE = [0x00, 0x00, 0x00, 0x01]
# MIXER_OUTPUT_MASTERLEVEL_RANGE = range(0x00, 0x80)
MIXER_OUTPUT_WAVEREC = [0x02]
MIXER_OUTPUT_WAVEREC_SIZE = [0x00, 0x00, 0x00, 0x01]
# ...


PRESET_EFFECT_CONTROL = [0x00, 0x40, 0x60]

# PARAMETER CONVERSION TABLES

# Parameters 10 to 18 are numbered and named wrongly the manual: count starts back from 1 and the names are just copied.
# The right list can be found on page 66.

# *1 : Pre Delay Time
# *2 : Delay Time 1
# *3 : Delay Time 2
# *4 : Delay Time 3
# *5 : Delay Time 4
# *6 : Rate 1
# *7 : Rate 2
# *8 : HF Damp
# *9 : Cutoff Freq
# *10 : EQ Freq
# *11 : LPF
# *12 : Manual
# *13 : Azimuth
# *14 : Accl
# *15 : Bass Cut Freq
# *16 : Reverb Time
# *17 : Distance
# *18 : Boost Freq

# so Parameter 10 is actually the 1 on pages 76-77)

# PRE DELAY TIME [ms] (1)
# It is not a regular parameters as it has different steps. Must be built in steps...
# PARAM_CONV_1 = tools.mergeRanges(range(0x00,0x33),tools.ulist(0,5,0.1,'ms'))
# PARAM_CONV_1_B = tools.mergeRanges(range(0x33,0x3D),tools.ulist(5.5,10,0.5))
# PARAM_CONV_1_C = tools.mergeRanges(range(0x3D,0x65),tools.ulist(11,50,1))
# PARAM_CONV_1_D = tools.mergeRanges(range(0x65,0x7E),tools.ulist(52,100,2))
# PARAM_CONV_1_E = {0x7E: '100', 0x7F: '100'}
# PARAM_CONV_1.update(PARAM_CONV_1_B)
# PARAM_CONV_1.update(PARAM_CONV_1_C)
# PARAM_CONV_1.update(PARAM_CONV_1_D)
# PARAM_CONV_1.update(PARAM_CONV_1_E)
# to save CPU and time, I put THEM ALL already built...
# Pre Delay Time (ms)
PARAM_TYPE_1 = ({0: '0ms', 1: '0.1ms', 2: '0.2ms', 3: '0.3ms', 4: '0.4ms', 5: '0.5ms',
                 6: '0.6ms', 7: '0.7ms', 8: '0.8ms', 9: '0.9ms', 10: '1.0ms', 11: '1.1ms',
                 12: '1.2ms', 13: '1.3ms', 14: '1.4ms', 15: '1.5ms', 16: '1.6ms', 17: '1.7ms',
                 18: '1.8ms', 19: '1.9ms', 20: '2.0ms', 21: '2.1ms', 22: '2.2ms', 23: '2.3ms',
                 24: '2.4ms', 25: '2.5ms', 26: '2.6ms', 27: '2.7ms', 28: '2.8ms', 29: '2.9ms',
                 30: '3.0ms', 31: '3.1ms', 32: '3.2ms', 33: '3.3ms', 34: '3.4ms', 35: '3.5ms',
                 36: '3.6ms', 37: '3.7ms', 38: '3.8ms', 39: '3.9ms', 40: '4.0ms', 41: '4.1ms',
                 42: '4.2ms', 43: '4.3ms', 44: '4.4ms', 45: '4.5ms', 46: '4.6ms', 47: '4.7ms',
                 48: '4.8ms', 49: '4.9ms', 50: '5.0ms', 51: '5.5ms', 52: '6.0ms', 53: '6.5ms', 54: '7.0ms',
                 55: '7.5ms', 56: '8.0ms', 57: '8.5ms', 58: '9.0ms', 59: '9.5ms', 60: '10.0ms', 61: '11msms',
                 62: '12msms',
                 63: '13msms', 64: '14ms', 65: '15ms', 66: '16ms', 67: '17ms', 68: '18ms', 69: '19ms', 70: '20ms',
                 71: '21ms',
                 72: '22ms', 73: '23ms', 74: '24ms', 75: '25ms', 76: '26ms', 77: '27ms', 78: '28ms', 79: '29ms',
                 80: '30ms',
                 81: '31ms', 82: '32ms', 83: '33ms', 84: '34ms', 85: '35ms', 86: '36ms', 87: '37ms', 88: '38ms',
                 89: '39ms',
                 90: '40ms', 91: '41ms', 92: '42ms', 93: '43ms', 94: '44ms', 95: '45ms', 96: '46ms', 97: '47ms',
                 98: '48ms',
                 99: '49ms', 100: '50ms', 101: '52ms', 102: '54ms', 103: '56ms', 104: '58ms', 105: '60ms',
                 106: '62ms',
                 107: '64ms', 108: '66ms', 109: '68ms', 110: '70ms', 111: '72ms', 112: '74ms', 113: '76ms',
                 114: '78ms',
                 115: '80ms', 116: '82ms', 117: '84ms', 118: '86ms', 119: '88ms', 120: '90ms', 121: '92ms',
                 122: '94ms',
                 123: '96ms', 124: '98ms', 125: '100ms', 126: '100ms', 127: '100ms'})

# Delay Time 2 (ms)
PARAM_TYPE_2 = ({0: '200ms', 1: '205ms', 2: '210ms', 3: '215ms', 4: '220ms', 5: '225ms',
                6: '230ms', 7: '235ms', 8: '240ms', 9: '245ms', 10: '250ms', 11: '255ms',
                12: '260ms', 13: '265ms', 14: '270ms', 15: '275ms', 16: '280ms', 17: '285ms',
                18: '290ms', 19: '295ms', 20: '300ms', 21: '305ms', 22: '310ms', 23: '315ms',
                24: '320ms', 25: '325ms', 26: '330ms', 27: '335ms', 28: '340ms', 29: '345ms',
                30: '350ms', 31: '355ms', 32: '360ms', 33: '365ms', 34: '370ms', 35: '375ms',
                36: '380ms', 37: '385ms', 38: '390ms', 39: '395ms', 40: '400ms', 41: '405ms',
                42: '410ms', 43: '415ms', 44: '420ms', 45: '425ms', 46: '430ms', 47: '435ms',
                48: '440ms', 49: '445ms', 50: '450ms', 51: '455ms', 52: '460ms', 53: '465ms',
                54: '470ms', 55: '475ms', 56: '480ms', 57: '485ms', 58: '490ms', 59: '495ms',
                60: '500ms', 61: '505ms', 62: '510ms', 63: '515ms', 64: '520ms', 65: '525ms',
                66: '530ms', 67: '535ms', 68: '540ms', 69: '545ms', 70: '550ms', 71: '560ms',
                72: '570ms', 73: '580ms', 74: '590ms', 75: '600ms', 76: '610ms', 77: '620ms',
                78: '630ms', 79: '640ms', 80: '650ms', 81: '660ms', 82: '670ms', 83: '680ms',
                84: '690ms', 85: '700ms', 86: '710ms', 87: '720ms', 88: '730ms', 89: '740ms',
                90: '750ms', 91: '760ms', 92: '770ms', 93: '780ms', 94: '790ms', 95: '800ms',
                96: '810ms', 97: '820ms', 98: '830ms', 99: '840ms', 100: '850ms', 101: '860ms',
                102: '870ms', 103: '880ms', 104: '890ms', 105: '900ms', 106: '910ms',
                107: '920ms', 108: '930ms', 109: '940ms', 110: '950ms', 111: '960ms',
                112: '970ms', 113: '980ms', 114: '990ms', 115: '1000ms'})

# Delay Time 2 (ms)
PARAM_TYPE_3 = ({0: '200ms', 1: '205ms', 2: '210ms', 3: '215ms', 4: '220ms', 5: '225ms',
                 6: '230ms', 7: '235ms', 8: '240ms', 9: '245ms', 10: '250ms', 11: '255ms',
                 12: '260ms', 13: '265ms', 14: '270ms', 15: '275ms', 16: '280ms', 17: '285ms',
                 18: '290ms', 19: '295ms', 20: '300ms', 21: '305ms', 22: '310ms', 23: '315ms',
                 24: '320ms', 25: '325ms', 26: '330ms', 27: '335ms', 28: '340ms', 29: '345ms',
                 30: '350ms', 31: '355ms', 32: '360ms', 33: '365ms', 34: '370ms', 35: '375ms',
                 36: '380ms', 37: '385ms', 38: '390ms', 39: '395ms', 40: '400ms', 41: '405ms',
                 42: '410ms', 43: '415ms', 44: '420ms', 45: '425ms', 46: '430ms', 47: '435ms',
                 48: '440ms', 49: '445ms', 50: '450ms', 51: '455ms', 52: '460ms', 53: '465ms',
                 54: '470ms', 55: '475ms', 56: '480ms', 57: '485ms', 58: '490ms', 59: '495ms',
                 60: '500ms', 61: '505ms', 62: '510ms', 63: '515ms', 64: '520ms', 65: '525ms',
                 66: '530ms', 67: '535ms', 68: '540ms', 69: '545ms', 70: '550ms', 71: '555ms',
                 72: '560ms', 73: '565ms', 74: '570ms', 75: '575ms', 76: '580ms', 77: '585ms',
                 78: '590ms', 79: '595ms', 80: '600ms', 81: '610ms', 82: '620ms', 83: '630ms',
                 84: '640ms', 85: '650ms', 86: '660ms', 87: '670ms', 88: '680ms', 89: '690ms',
                 90: '700ms', 91: '710ms', 92: '720ms', 93: '730ms', 94: '740ms', 95: '750ms',
                 96: '760ms', 97: '770ms', 98: '780ms', 99: '790ms', 100: '800ms', 101: '810ms',
                 102: '820ms', 103: '830ms', 104: '840ms', 105: '850ms', 106: '860ms',
                 107: '870ms', 108: '880ms', 109: '890ms', 110: '900ms', 111: '910ms',
                 112: '920ms', 113: '930ms', 114: '940ms', 115: '950ms', 116: '960ms',
                 117: '970ms', 118: '980ms', 119: '990ms', 120: '1000ms', 121: '1000',
                 122: '1000', 123: '1000', 124: '1000', 125: '1000', 126: '1000', 127: '1000'})



# Delay Time 3 (ms)
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
# Some effects require a shorter version of *Delay Time 3*
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

# PARAM_TYPE_5 = tools.mergeRanges(range(0x00,0x80),tools.ulist(0,635,5,'ms'))
# Delay Time 4
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
                 120: '600ms', 121: '605ms', 122: '610ms', 123: '615ms', 124: '620ms', 125: '625ms', 126: '630ms',
                 127: '635ms'})

# Some effects require a shorter version of Delay Time 4
PARAM_TYPE_5_SHORT = ({1: '5ms', 2: '10ms', 3: '15ms', 4: '20ms', 5: '25ms', 6: '30ms', 7: '35ms',
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
                 99: '495ms', 100: '500ms'})

# Rate1 (Hz)
PARAM_TYPE_6 = ({0: '0.05Hz', 1: '0.1Hz', 2: '0.15Hz', 3: '0.2Hz', 4: '0.25Hz', 5: '0.3Hz', 6: '0.35Hz',
                 7: '0.4Hz', 8: '0.45Hz', 9: '0.5Hz', 10: '0.55Hz', 11: '0.6Hz', 12: '0.65Hz', 13: '0.7Hz',
                 14: '0.75Hz', 15: '0.8Hz', 16: '0.85Hz', 17: '0.9Hz', 18: '0.95Hz', 19: '1.0Hz', 20: '1.05Hz',
                 21: '1.1Hz', 22: '1.15Hz', 23: '1.2Hz', 24: '1.25Hz', 25: '1.3Hz', 26: '1.35Hz', 27: '1.4Hz',
                 28: '1.45Hz', 29: '1.5Hz', 30: '1.55Hz', 31: '1.6Hz', 32: '1.65Hz', 33: '1.7Hz', 34: '1.75Hz',
                 35: '1.8Hz', 36: '1.85Hz', 37: '1.9Hz', 38: '1.95Hz', 39: '2.0Hz', 40: '2.05Hz', 41: '2.1Hz',
                 42: '2.15Hz', 43: '2.2Hz', 44: '2.25Hz', 45: '2.3Hz', 46: '2.35Hz', 47: '2.4Hz', 48: '2.45Hz',
                 49: '2.5Hz', 50: '2.55Hz', 51: '2.6Hz', 52: '2.65Hz', 53: '2.7Hz', 54: '2.75Hz', 55: '2.8Hz',
                 56: '2.85Hz', 57: '2.9Hz', 58: '2.95Hz', 59: '3.0Hz', 60: '3.05Hz', 61: '3.1Hz', 62: '3.15Hz',
                 63: '3.2Hz', 64: '3.25Hz', 65: '3.3Hz', 66: '3.35Hz', 67: '3.4Hz', 68: '3.45Hz', 69: '3.5Hz',
                 70: '3.55Hz', 71: '3.6Hz', 72: '3.65Hz', 73: '3.7Hz', 74: '3.75Hz', 75: '3.8Hz', 76: '3.85Hz',
                 77: '3.9Hz', 78: '3.95Hz', 79: '4.0Hz', 80: '4.05Hz', 81: '4.1Hz', 82: '4.15Hz', 83: '4.2Hz',
                 84: '4.25Hz', 85: '4.3Hz', 86: '4.35Hz', 87: '4.4Hz', 88: '4.45Hz', 89: '4.5Hz', 90: '4.55Hz',
                 91: '4.6Hz', 92: '4.65Hz', 93: '4.7Hz', 94: '4.75Hz', 95: '4.8Hz', 96: '4.85Hz', 97: '4.9Hz',
                 98: '4.95Hz', 99: '5.0Hz', 100: '5.1Hz', 101: '5.2Hz', 102: '5.3Hz', 103: '5.4Hz', 104: '5.5Hz',
                 105: '5.6Hz', 106: '5.7Hz', 107: '5.8Hz', 108: '5.9Hz', 109: '6.0Hz', 110: '6.1Hz',
                 111: '6.2Hz', 112: '6.3Hz', 113: '6.4Hz', 114: '6.5Hz', 115: '6.6Hz', 116: '6.7Hz',
                 117: '6.8Hz', 118: '6.9Hz', 119: '7.0Hz', 120: '7.5Hz', 121: '8.0Hz', 122: '8.5Hz',
                 123: '9.0Hz', 124: '9.5Hz', 125: '10.0Hz', 126: '10Hz', 127: '10Hz'}
                )

# Rate2 (Hz)
PARAM_TYPE_7 =  ({0: '0.05Hz', 1: '0.1Hz', 2: '0.15Hz', 3: '0.2Hz', 4: '0.25Hz', 5: '0.3Hz',
                  6: '0.35Hz', 7: '0.4Hz', 8: '0.45Hz', 9: '0.5Hz', 10: '0.55Hz', 11: '0.6Hz',
                  12: '0.65Hz', 13: '0.7Hz', 14: '0.75Hz', 15: '0.8Hz', 16: '0.85Hz', 17: '0.9Hz',
                  18: '0.95Hz', 19: '1.0Hz', 20: '1.05Hz', 21: '1.1Hz', 22: '1.15Hz', 23: '1.2Hz',
                  24: '1.25Hz', 25: '1.3Hz', 26: '1.35Hz', 27: '1.4Hz', 28: '1.45Hz', 29: '1.5Hz',
                  30: '1.55Hz', 31: '1.6Hz', 32: '1.65Hz', 33: '1.7Hz', 34: '1.75Hz', 35: '1.8Hz',
                  36: '1.85Hz', 37: '1.9Hz', 38: '1.95Hz', 39: '2.0Hz', 40: '2.05Hz', 41: '2.1Hz',
                  42: '2.15Hz', 43: '2.2Hz', 44: '2.25Hz', 45: '2.3Hz', 46: '2.35Hz', 47: '2.4Hz',
                  48: '2.45Hz', 49: '2.5Hz', 50: '2.55Hz', 51: '2.6Hz', 52: '2.65Hz', 53: '2.7Hz',
                  54: '2.75Hz', 55: '2.8Hz', 56: '2.85Hz', 57: '2.9Hz', 58: '2.95Hz', 59: '3.0Hz',
                  60: '3.05Hz', 61: '3.1Hz', 62: '3.15Hz', 63: '3.2Hz', 64: '3.25Hz', 65: '3.3Hz',
                  66: '3.35Hz', 67: '3.4Hz', 68: '3.45Hz', 69: '3.5Hz', 70: '3.55Hz', 71: '3.6Hz',
                  72: '3.65Hz', 73: '3.7Hz', 74: '3.75Hz', 75: '3.8Hz', 76: '3.85Hz', 77: '3.9Hz',
                  78: '3.95Hz', 79: '4.0Hz', 80: '4.05Hz', 81: '4.1Hz', 82: '4.15Hz', 83: '4.2Hz',
                  84: '4.25Hz', 85: '4.3Hz', 86: '4.35Hz', 87: '4.4Hz', 88: '4.45Hz', 89: '4.5Hz',
                  90: '4.55Hz', 91: '4.6Hz', 92: '4.65Hz', 93: '4.7Hz', 94: '4.75Hz', 95: '4.8Hz',
                  96: '4.85Hz', 97: '4.9Hz', 98: '4.95Hz', 99: '5.0Hz', 100: '5.05Hz', 101: '5.1Hz',
                  102: '5.15Hz', 103: '5.2Hz', 104: '5.25Hz', 105: '5.3Hz', 106: '5.35Hz',
                  107: '5.4Hz', 108: '5.45Hz', 109: '5.5Hz', 110: '5.55Hz', 111: '5.6Hz',
                  112: '5.65Hz', 113: '5.7Hz', 114: '5.75Hz', 115: '5.8Hz', 116: '5.85Hz',
                  117: '5.9Hz', 118: '5.95Hz', 119: '6.0Hz', 120: '6.05Hz', 121: '6.1Hz',
                  122: '6.15Hz', 123: '6.2Hz', 124: '6.25Hz', 125: '6.3Hz', 126: '6.35Hz',
                  127: '6.4Hz'})


# HF Damp (HZ)
PARAM_TYPE_8 = (
    {0: '315Hz', 1: '315Hz', 2: '315Hz', 3: '315Hz', 4: '315Hz', 5: '315Hz', 6: '315Hz', 7: '315Hz', 8: '400Hz',
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

# Cutoff Freq (Hz)
PARAM_TYPE_9 = (
    {0: '250Hz', 1: '250Hz', 2: '250Hz', 3: '250Hz', 4: '250Hz', 5: '250Hz', 6: '250Hz',
     7: '250Hz', 8: '315Hz', 9: '315Hz', 10: '315Hz', 11: '315Hz', 12: '315Hz', 13: '315Hz',
     14: '315Hz', 15: '315Hz', 16: '400Hz', 17: '400Hz', 18: '400Hz', 19: '400Hz', 20: '400Hz',
     21: '400Hz', 22: '400Hz', 23: '400Hz', 24: '500Hz', 25: '500Hz', 26: '500Hz', 27: '500Hz',
     28: '500Hz', 29: '500Hz', 30: '500Hz', 31: '500Hz', 32: '630Hz', 33: '630Hz', 34: '630Hz',
     35: '630Hz', 36: '630Hz', 37: '630Hz', 38: '630Hz', 39: '630Hz', 40: '800Hz', 41: '800Hz',
     42: '800Hz', 43: '800Hz', 44: '800Hz', 45: '800Hz', 46: '800Hz', 47: '800Hz', 48: '1000Hz',
     49: '1000Hz', 50: '1000Hz', 51: '1000Hz', 52: '1000Hz', 53: '1000Hz', 54: '1000Hz',
     55: '1000Hz', 56: '1250Hz', 57: '1250Hz', 58: '1250Hz', 59: '1250Hz', 60: '1250Hz',
     61: '1250Hz', 62: '1250Hz', 63: '1250Hz', 64: '1600Hz', 65: '1600Hz', 66: '1600Hz',
     67: '1600Hz', 68: '1600Hz', 69: '1600Hz', 70: '1600Hz', 71: '1600Hz', 72: '2000Hz',
     73: '2000Hz', 74: '2000Hz', 75: '2000Hz', 76: '2000Hz', 77: '2000Hz', 78: '2000Hz',
     79: '2000Hz', 80: '2500Hz', 81: '2500Hz', 82: '2500Hz', 83: '2500Hz', 84: '2500Hz',
     85: '2500Hz', 86: '2500Hz', 87: '2500Hz', 88: '3150Hz', 89: '3150Hz', 90: '3150Hz',
     91: '3150Hz', 92: '3150Hz', 93: '3150Hz', 94: '3150Hz', 95: '3150Hz', 96: '4000Hz',
     97: '4000Hz', 98: '4000Hz', 99: '4000Hz', 100: '4000Hz', 101: '4000Hz', 102: '4000Hz',
     103: '4000Hz', 104: '5000Hz', 105: '5000Hz', 106: '5000Hz', 107: '5000Hz', 108: '5000Hz',
     109: '5000Hz', 110: '5000Hz', 111: '5000Hz', 112: '6300Hz', 113: '6300Hz', 114: '6300Hz',
     115: '6300Hz', 116: '6300Hz', 117: '6300Hz', 118: '6300Hz', 119: '6300Hz', 120: '8000Hz',
     121: '8000Hz', 122: '8000Hz', 123: '8000Hz', 124: '8000Hz', 125: '8000Hz', 126: '8000Hz',
     127: '8000Hz'})

# SEMIPAR_10=[]
# for hz in [200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300]:
#   for pippo in range(1,9):
#      SEMIPAR_10.append(str(hz)+'Hz')
#
# PAR_10= tools.mergeRanges(range(0x00,0x80),SEMIPAR_10)

# EQ Freq
PARAM_TYPE_10 = (
    {0: '200Hz', 1: '200Hz', 2: '200Hz', 3: '200Hz', 4: '200Hz', 5: '200Hz', 6: '200Hz', 7: '200Hz',
     8: '250Hz', 9: '250Hz', 10: '250Hz', 11: '250Hz', 12: '250Hz', 13: '250Hz', 14: '250Hz', 15: '250Hz',
     16: '315Hz', 17: '315Hz', 18: '315Hz', 19: '315Hz', 20: '315Hz', 21: '315Hz', 22: '315Hz', 23: '315Hz',
     24: '400Hz', 25: '400Hz', 26: '400Hz', 27: '400Hz', 28: '400Hz', 29: '400Hz', 30: '400Hz', 31: '400Hz',
     32: '500Hz', 33: '500Hz', 34: '500Hz', 35: '500Hz', 36: '500Hz', 37: '500Hz', 38: '500Hz', 39: '500Hz',
     40: '630Hz', 41: '630Hz', 42: '630Hz', 43: '630Hz', 44: '630Hz', 45: '630Hz', 46: '630Hz', 47: '630Hz',
     48: '800Hz', 49: '800Hz', 50: '800Hz', 51: '800Hz', 52: '800Hz', 53: '800Hz', 54: '800Hz', 55: '800Hz',
     56: '1000Hz', 57: '1000Hz', 58: '1000Hz', 59: '1000Hz', 60: '1000Hz', 61: '1000Hz', 62: '1000Hz',
     63: '1000Hz', 64: '1250Hz', 65: '1250Hz', 66: '1250Hz', 67: '1250Hz', 68: '1250Hz', 69: '1250Hz',
     70: '1250Hz', 71: '1250Hz', 72: '1600Hz', 73: '1600Hz', 74: '1600Hz', 75: '1600Hz', 76: '1600Hz',
     77: '1600Hz', 78: '1600Hz', 79: '1600Hz', 80: '2000Hz', 81: '2000Hz', 82: '2000Hz', 83: '2000Hz',
     84: '2000Hz', 85: '2000Hz', 86: '2000Hz', 87: '2000Hz', 88: '2500Hz', 89: '2500Hz', 90: '2500Hz',
     91: '2500Hz', 92: '2500Hz', 93: '2500Hz', 94: '2500Hz', 95: '2500Hz', 96: '3150Hz', 97: '3150Hz',
     98: '3150Hz', 99: '3150Hz', 100: '3150Hz', 101: '3150Hz', 102: '3150Hz', 103: '3150Hz', 104: '4000Hz',
     105: '4000Hz', 106: '4000Hz', 107: '4000Hz', 108: '4000Hz', 109: '4000Hz', 110: '4000Hz', 111: '4000Hz',
     112: '5000Hz', 113: '5000Hz', 114: '5000Hz', 115: '5000Hz', 116: '5000Hz', 117: '5000Hz', 118: '5000Hz',
     119: '5000Hz', 120: '6300Hz', 121: '6300Hz', 122: '6300Hz', 123: '6300Hz', 124: '6300Hz', 125: '6300Hz',
     126: '6300Hz', 127: '6300Hz'}
)

# LPF

# SEMIPAR_11=[]
# for hz in [250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,'Bypass']:
#     for pippo in range(1,9):
#         SEMIPAR_11.append(str(hz)+'{}'.format("Hz" if hz != "Bypass" else ""))
#
# PAR_10= tools.mergeRanges(range(0x00,0x80),SEMIPAR_11)

PARAM_TYPE_11 = ({0: '250Hz', 1: '250Hz', 2: '250Hz', 3: '250Hz', 4: '250Hz', 5: '250Hz',
                  6: '250Hz', 7: '250Hz', 8: '315Hz', 9: '315Hz', 10: '315Hz', 11: '315Hz',
                  12: '315Hz', 13: '315Hz', 14: '315Hz', 15: '315Hz', 16: '400Hz', 17: '400Hz',
                  18: '400Hz', 19: '400Hz', 20: '400Hz', 21: '400Hz', 22: '400Hz', 23: '400Hz',
                  24: '500Hz', 25: '500Hz', 26: '500Hz', 27: '500Hz', 28: '500Hz', 29: '500Hz',
                  30: '500Hz', 31: '500Hz', 32: '630Hz', 33: '630Hz', 34: '630Hz', 35: '630Hz',
                  36: '630Hz', 37: '630Hz', 38: '630Hz', 39: '630Hz', 40: '800Hz', 41: '800Hz',
                  42: '800Hz', 43: '800Hz', 44: '800Hz', 45: '800Hz', 46: '800Hz', 47: '800Hz',
                  48: '1000Hz', 49: '1000Hz', 50: '1000Hz', 51: '1000Hz', 52: '1000Hz',
                  53: '1000Hz', 54: '1000Hz', 55: '1000Hz', 56: '1250Hz', 57: '1250Hz',
                  58: '1250Hz', 59: '1250Hz', 60: '1250Hz', 61: '1250Hz', 62: '1250Hz',
                  63: '1250Hz', 64: '1600Hz', 65: '1600Hz', 66: '1600Hz', 67: '1600Hz',
                  68: '1600Hz', 69: '1600Hz', 70: '1600Hz', 71: '1600Hz', 72: '2000Hz',
                  73: '2000Hz', 74: '2000Hz', 75: '2000Hz', 76: '2000Hz', 77: '2000Hz',
                  78: '2000Hz', 79: '2000Hz', 80: '2500Hz', 81: '2500Hz', 82: '2500Hz',
                  83: '2500Hz', 84: '2500Hz', 85: '2500Hz', 86: '2500Hz', 87: '2500Hz',
                  88: '3150Hz', 89: '3150Hz', 90: '3150Hz', 91: '3150Hz', 92: '3150Hz',
                  93: '3150Hz', 94: '3150Hz', 95: '3150Hz', 96: '4000Hz', 97: '4000Hz',
                  98: '4000Hz', 99: '4000Hz', 100: '4000Hz', 101: '4000Hz', 102: '4000Hz',
                  103: '4000Hz', 104: '5000Hz', 105: '5000Hz', 106: '5000Hz', 107: '5000Hz',
                  108: '5000Hz', 109: '5000Hz', 110: '5000Hz', 111: '5000Hz', 112: '6300Hz',
                  113: '6300Hz', 114: '6300Hz', 115: '6300Hz', 116: '6300Hz', 117: '6300Hz',
                  118: '6300Hz', 119: '6300Hz', 120: 'Bypass', 121: 'Bypass', 122: 'Bypass',
                  123: 'Bypass', 124: 'Bypass', 125: 'Bypass', 126: 'Bypass', 127: 'Bypass'})

# Manual

# PARAM_TYPE_12
# p = tools.ulist(100,300,10,'Hz')
# s = tools.ulist(320,1000,20,'Hz')
# t = tools.ulist(1100,8000,100,'Hz')
# q = 2 * ['8000Hz']
#
# p.extend(s)
# p.extend(t)
# p.extend(q)
# z = tools.mergeRanges(range(0x00,0x80),p)

PARAM_TYPE_12 = ({0: '100Hz', 1: '110Hz', 2: '120Hz', 3: '130Hz', 4: '140Hz', 5: '150Hz', 6: '160Hz',
                  7: '170Hz', 8: '180Hz', 9: '190Hz', 10: '200Hz', 11: '210Hz', 12: '220Hz',
                  13: '230Hz', 14: '240Hz', 15: '250Hz', 16: '260Hz', 17: '270Hz', 18: '280Hz',
                  19: '290Hz', 20: '300Hz', 21: '320Hz', 22: '340Hz', 23: '360Hz', 24: '380Hz',
                  25: '400Hz', 26: '420Hz', 27: '440Hz', 28: '460Hz', 29: '480Hz', 30: '500Hz',
                  31: '520Hz', 32: '540Hz', 33: '560Hz', 34: '580Hz', 35: '600Hz', 36: '620Hz',
                  37: '640Hz', 38: '660Hz', 39: '680Hz', 40: '700Hz', 41: '720Hz', 42: '740Hz',
                  43: '760Hz', 44: '780Hz', 45: '800Hz', 46: '820Hz', 47: '840Hz', 48: '860Hz',
                  49: '880Hz', 50: '900Hz', 51: '920Hz', 52: '940Hz', 53: '960Hz', 54: '980Hz',
                  55: '1000Hz', 56: '1100Hz', 57: '1200Hz', 58: '1300Hz', 59: '1400Hz',
                  60: '1500Hz', 61: '1600Hz', 62: '1700Hz', 63: '1800Hz', 64: '1900Hz',
                  65: '2000Hz', 66: '2100Hz', 67: '2200Hz', 68: '2300Hz', 69: '2400Hz',
                  70: '2500Hz', 71: '2600Hz', 72: '2700Hz', 73: '2800Hz', 74: '2900Hz',
                  75: '3000Hz', 76: '3100Hz', 77: '3200Hz', 78: '3300Hz', 79: '3400Hz',
                  80: '3500Hz', 81: '3600Hz', 82: '3700Hz', 83: '3800Hz', 84: '3900Hz',
                  85: '4000Hz', 86: '4100Hz', 87: '4200Hz', 88: '4300Hz', 89: '4400Hz',
                  90: '4500Hz', 91: '4600Hz', 92: '4700Hz', 93: '4800Hz', 94: '4900Hz',
                  95: '5000Hz', 96: '5100Hz', 97: '5200Hz', 98: '5300Hz', 99: '5400Hz',
                  100: '5500Hz', 101: '5600Hz', 102: '5700Hz', 103: '5800Hz', 104: '5900Hz',
                  105: '6000Hz', 106: '6100Hz', 107: '6200Hz', 108: '6300Hz', 109: '6400Hz',
                  110: '6500Hz', 111: '6600Hz', 112: '6700Hz', 113: '6800Hz', 114: '6900Hz',
                  115: '7000Hz', 116: '7100Hz', 117: '7200Hz', 118: '7300Hz', 119: '7400Hz',
                  120: '7500Hz', 121: '7600Hz', 122: '7700Hz', 123: '7800Hz', 124: '7900Hz',
                  125: '8000Hz', 126: '8000Hz', 127: '8000Hz'})

# Azimuth

# PARAM_TYPE_13
# c = 6 * ['L180(=R180)']
# l = tools.rlist(168,1,-12,'L',4)
#
# m = 4 * ['0']
# r = tools.rlist(12,179,12,'R',4)
# f = 6 * ['R180(=L180)']
#
# c.extend(l)
# c.extend(m)
# c.extend(r)
# c.extend(f)
# base_range = range(0x00,0x80)
# PARAM_TYPE_13 = tools.mergeRanges(base_range, c)

PARAM_TYPE_13 = ({0: 'L180(=R180)', 1: 'L180(=R180)', 2: 'L180(=R180)', 3: 'L180(=R180)',
                  4: 'L180(=R180)', 5: 'L180(=R180)', 6: 'L168', 7: 'L168', 8: 'L168', 9: 'L168',
                  10: 'L156', 11: 'L156', 12: 'L156', 13: 'L156', 14: 'L144', 15: 'L144',
                  16: 'L144', 17: 'L144', 18: 'L132', 19: 'L132', 20: 'L132', 21: 'L132', 22: 'L120',
                  23: 'L120', 24: 'L120', 25: 'L120', 26: 'L108', 27: 'L108', 28: 'L108', 29: 'L108',
                  30: 'L96', 31: 'L96', 32: 'L96', 33: 'L96', 34: 'L84', 35: 'L84', 36: 'L84',
                  37: 'L84', 38: 'L72', 39: 'L72', 40: 'L72', 41: 'L72', 42: 'L60', 43: 'L60',
                  44: 'L60', 45: 'L60', 46: 'L48', 47: 'L48', 48: 'L48', 49: 'L48', 50: 'L36',
                  51: 'L36', 52: 'L36', 53: 'L36', 54: 'L24', 55: 'L24', 56: 'L24', 57: 'L24',
                  58: 'L12', 59: 'L12', 60: 'L12', 61: 'L12', 62: '0', 63: '0', 64: '0', 65: '0',
                  66: 'R12', 67: 'R12', 68: 'R12', 69: 'R12', 70: 'R24', 71: 'R24', 72: 'R24',
                  73: 'R24', 74: 'R36', 75: 'R36', 76: 'R36', 77: 'R36', 78: 'R48', 79: 'R48',
                  80: 'R48', 81: 'R48', 82: 'R60', 83: 'R60', 84: 'R60', 85: 'R60', 86: 'R72',
                  87: 'R72', 88: 'R72', 89: 'R72', 90: 'R84', 91: 'R84', 92: 'R84', 93: 'R84',
                  94: 'R96', 95: 'R96', 96: 'R96', 97: 'R96', 98: 'R108', 99: 'R108', 100: 'R108',
                  101: 'R108', 102: 'R120', 103: 'R120', 104: 'R120', 105: 'R120', 106: 'R132',
                  107: 'R132', 108: 'R132', 109: 'R132', 110: 'R144', 111: 'R144', 112: 'R144',
                  113: 'R144', 114: 'R156', 115: 'R156', 116: 'R156', 117: 'R156', 118: 'R168',
                  119: 'R168', 120: 'R168', 121: 'R168', 122: 'R180(=L180)', 123: 'R180(=L180)',
                  124: 'R180(=L180)', 125: 'R180(=L180)', 126: 'R180(=L180)', 127: 'R180(=L180)'}
)

# Accl

# PARAM_TYPE_14
# d = tools.rlist(0,15,1,factor = 8)
# p = tools.mergeRanges(base_range,d)

PARAM_TYPE_14 = ({0: '0', 1: '0', 2: '0', 3: '0', 4: '0', 5: '0', 6: '0', 7: '0', 8: '1', 9: '1',
                  10: '1', 11: '1', 12: '1', 13: '1', 14: '1', 15: '1', 16: '2', 17: '2', 18: '2',
                  19: '2', 20: '2', 21: '2', 22: '2', 23: '2', 24: '3', 25: '3', 26: '3', 27: '3',
                  28: '3', 29: '3', 30: '3', 31: '3', 32: '4', 33: '4', 34: '4', 35: '4', 36: '4',
                  37: '4', 38: '4', 39: '4', 40: '5', 41: '5', 42: '5', 43: '5', 44: '5', 45: '5',
                  46: '5', 47: '5', 48: '6', 49: '6', 50: '6', 51: '6', 52: '6', 53: '6', 54: '6',
                  55: '6', 56: '7', 57: '7', 58: '7', 59: '7', 60: '7', 61: '7', 62: '7', 63: '7',
                  64: '8', 65: '8', 66: '8', 67: '8', 68: '8', 69: '8', 70: '8', 71: '8', 72: '9',
                  73: '9', 74: '9', 75: '9', 76: '9', 77: '9', 78: '9', 79: '9', 80: '10', 81: '10',
                  82: '10', 83: '10', 84: '10', 85: '10', 86: '10', 87: '10', 88: '11', 89: '11',
                  90: '11', 91: '11', 92: '11', 93: '11', 94: '11', 95: '11', 96: '12', 97: '12',
                  98: '12', 99: '12', 100: '12', 101: '12', 102: '12', 103: '12', 104: '13',
                  105: '13', 106: '13', 107: '13', 108: '13', 109: '13', 110: '13', 111: '13',
                  112: '14', 113: '14', 114: '14', 115: '14', 116: '14', 117: '14', 118: '14',
                  119: '14', 120: '15', 121: '15', 122: '15', 123: '15', 124: '15', 125: '15',
                  126: '15', 127: '15'}
                 )

# *15 : Bass Cut Freq
PARAM_TYPE_15 = (
    {0: '20', 1: '20', 2: '20', 3: '20', 4: '20', 5: '20', 6: '20', 7: '20', 8: '25', 9: '25',
     10: '25', 11: '25', 12: '25', 13: '25', 14: '25', 15: '25', 16: '35', 17: '35', 18: '35',
     19: '35', 20: '35', 21: '35', 22: '35', 23: '35', 24: '50', 25: '50', 26: '50', 27: '50',
     28: '50', 29: '50', 30: '50', 31: '50', 32: '85', 33: '85', 34: '85', 35: '85', 36: '85',
     37: '85', 38: '85', 39: '85', 40: '115', 41: '115', 42: '115', 43: '115', 44: '115', 45: '115',
     46: '115', 47: '115', 48: '150', 49: '150', 50: '150', 51: '150', 52: '150', 53: '150',
     54: '150', 55: '150', 56: '200', 57: '200', 58: '200', 59: '200', 60: '200', 61: '200',
     62: '200', 63: '200', 64: '250', 65: '250', 66: '250', 67: '250', 68: '250', 69: '250',
     70: '250', 71: '250', 72: '350', 73: '350', 74: '350', 75: '350', 76: '350', 77: '350',
     78: '350', 79: '350', 80: '500', 81: '500', 82: '500', 83: '500', 84: '500', 85: '500',
     86: '500', 87: '500', 88: '650', 89: '650', 90: '650', 91: '650', 92: '650', 93: '650',
     94: '650', 95: '650', 96: '850', 97: '850', 98: '850', 99: '850', 100: '850', 101: '850',
     102: '850', 103: '850', 104: '1000', 105: '1000', 106: '1000', 107: '1000', 108: '1000',
     109: '1000', 110: '1000', 111: '1000', 112: '1500', 113: '1500', 114: '1500', 115: '1500',
     116: '1500', 117: '1500', 118: '1500', 119: '1500', 120: '2000', 121: '2000', 122: '2000',
     123: '2000', 124: '2000', 125: '2000', 126: '2000', 127: '2000'}
)

# Reverb Time

# PARAM_TYPE_16 = tools.mergeRanges(range(0x00,0x64),tools.ulist(0.1,10,0.1,'s'))
# PARAM_TYPE_16_B = tools.mergeRanges(range(0x64,0x80),tools.ulist(11,38,1,'s'))
# PARAM_TYPE_16.update(PARAM_TYPE_16_B)


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
                  120: '31s', 121: '32s', 122: '33s', 123: '34s', 124: '35s', 125: '36s', 126: '37s', 127: '38s'}
                 )

# Boost Freq

# PARAM_TYPE_17
# this is shortissimo - and it's not used anywhere!!
# d1 = tools.rlist(60,200,20)
# d2 = tools.rlist(300,400,100)
# d1.extend(d2)
# p = tools.mergeRanges(range(0x00,0x0A), d1)

PARAM_TYPE_17 = ({0: '60Hz', 1: '80Hz', 2: '100Hz', 3: '120Hz', 4: '140Hz',
                  5: '160Hz', 6: '180Hz', 7: '200Hz', 8: '300Hz', 9: '400Hz'})

# Those are funny. Non capire O~O
PARAM_BALANCE = ({0: 'D>0E', 1: 'D>0E', 2: 'D>1E', 3: 'D>3E', 4: 'D>4E', 5: 'D>6E', 6: 'D>7E',
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



PARAM_ON_OFF = {0: 'Off', 1: 'On'}
PARAM_UP_DOWN = {0: 'Down', 1: 'Up'}

# -12dB - +12dB
# PARAM_12DB = tools.mergeRanges(range(0x34,0x4D), tools.ulist(-12,+12,1,'dB'))
PARAM_12DB = ({52: '-12dB', 53: '-11dB', 54: '-10dB', 55: '-9dB', 56: '-8dB', 57: '-7dB', 58: '-6dB',
               59: '-5dB', 60: '-4dB', 61: '-3dB', 62: '-2dB', 63: '-1dB', 64: '0dB', 65: '1dB',
               66: '2dB', 67: '3dB', 68: '4dB', 69: '5dB', 70: '6dB', 71: '7dB', 72: '8dB', 73: '9dB',
               74: '10dB', 75: '11dB', 76: '12dB'}
              )

# 0 - 18 dB - well, actually is 0 - 22 (as for the documentation there is a range problem...)
# Low Boost Level....0dB - +8dB - 18dB....40 - 56....04 the two ranges are different...
# PARAM_0_18DB = tools.mergeRanges(range(0x40, 0x57), tools.ulist(0, +22, 1,'dB'))
PARAM_0_18DB = ({64: '0dB', 65: '1dB', 66: '2dB', 67: '3dB', 68: '4dB', 69: '5dB', 70: '6dB', 71: '7dB',
                 72: '8dB', 73: '9dB', 74: '10dB', 75: '11dB', 76: '12dB', 77: '13dB', 78: '14dB', 79: '15dB',
                 80: '16dB', 81: '17dB', 82: '18dB', 83: '19dB', 84: '20dB', 85: '21dB', 86: '22dB'}
                )

# 1 - 4
PARAM_1_4 = ({0: '1', 1: '2', 2: '3', 3: '4'})


# -24 - +12
# PARAM_2412 = tools.mergeRanges(range(0x28, 0x4D), tools.ulist(-24, +12, 1))
PARAM_2412 = ({40: '-24', 41: '-23', 42: '-22', 43: '-21', 44: '-20', 45: '-19', 46: '-18',
               47: '-17', 48: '-16', 49: '-15', 50: '-14', 51: '-13', 52: '-12', 53: '-11',
               54: '-10', 55: '-9', 56: '-8', 57: '-7', 58: '-6', 59: '-5', 60: '-4', 61: '-3',
               62: '-2', 63: '-1', 64: '0', 65: '1', 66: '2', 67: '3', 68: '4', 69: '5',
               70: '6', 71: '7', 72: '8', 73: '9', 74: '10', 75: '11', 76: '12'})


# 0-127
# PARAM_0127 = tools.mergeRanges(range(0x00, 0x80), tools.ulist(0, 127, 1))

PARAM_0127 = ({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8',
               9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16',
               17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24',
               25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32',
               33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40',
               41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48',
               49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56',
               57: '57', 58: '58', 59: '59', 60: '60', 61: '61', 62: '62', 63: '63', 64: '64',
               65: '65', 66: '66', 67: '67', 68: '68', 69: '69', 70: '70', 71: '71', 72: '72',
               73: '73', 74: '74', 75: '75', 76: '76', 77: '77', 78: '78', 79: '79', 80: '80',
               81: '81', 82: '82', 83: '83', 84: '84', 85: '85', 86: '86', 87: '87', 88: '88',
               89: '89', 90: '90', 91: '91', 92: '92', 93: '93', 94: '94', 95: '95', 96: '96',
               97: '97', 98: '98', 99: '99', 100: '100', 101: '101', 102: '102', 103: '103',
               104: '104', 105: '105', 106: '106', 107: '107', 108: '108', 109: '109', 110: '110',
               111: '111', 112: '112', 113: '113', 114: '114', 115: '115', 116: '116', 117: '117',
               118: '118', 119: '119', 120: '120', 121: '121', 122: '122', 123: '123', 124: '124',
               125: '125', 126: '126', 127: '127'})



# -98% - +98%
# PARAM_9898 = tools.mergeRanges(range(0x0F, 0x72), tools.ulist(-98, +98, 2, '%'))
PARAM_9898 = ({15: '-98%', 16: '-96%', 17: '-94%', 18: '-92%', 19: '-90%', 20: '-88%',
               21: '-86%', 22: '-84%', 23: '-82%', 24: '-80%', 25: '-78%', 26: '-76%',
               27: '-74%', 28: '-72%', 29: '-70%', 30: '-68%', 31: '-66%', 32: '-64%',
               33: '-62%', 34: '-60%', 35: '-58%', 36: '-56%', 37: '-54%', 38: '-52%',
               39: '-50%', 40: '-48%', 41: '-46%', 42: '-44%', 43: '-42%', 44: '-40%',
               45: '-38%', 46: '-36%', 47: '-34%', 48: '-32%', 49: '-30%', 50: '-28%',
               51: '-26%', 52: '-24%', 53: '-22%', 54: '-20%', 55: '-18%', 56: '-16%',
               57: '-14%', 58: '-12%', 59: '-10%', 60: '-8%', 61: '-6%', 62: '-4%',
               63: '-2%', 64: '0%', 65: '2%', 66: '4%', 67: '6%', 68: '8%', 69: '10%',
               70: '12%', 71: '14%', 72: '16%', 73: '18%', 74: '20%', 75: '22%', 76: '24%',
               77: '26%', 78: '28%', 79: '30%', 80: '32%', 81: '34%', 82: '36%', 83: '38%',
               84: '40%', 85: '42%', 86: '44%', 87: '46%', 88: '48%', 89: '50%', 90: '52%',
               91: '54%', 92: '56%', 93: '58%', 94: '60%', 95: '62%', 96: '64%', 97: '66%',
               98: '68%', 99: '70%', 100: '72%', 101: '74%', 102: '76%', 103: '78%',
               104: '80%', 105: '82%', 106: '84%', 107: '86%', 108: '88%', 109: '90%',
               110: '92%', 111: '94%', 112: '96%', 113: '98%'})

# -100 - +100
# PARAM_100100 = tools.mergeRanges(range(0x0E, 0x73), tools.ulist(-100, +100, 2))
PARAM_100100 = ({14: '-100', 15: '-98', 16: '-96', 17: '-94', 18: '-92', 19: '-90',
                 20: '-88', 21: '-86', 22: '-84', 23: '-82', 24: '-80', 25: '-78',
                 26: '-76', 27: '-74', 28: '-72', 29: '-70', 30: '-68', 31: '-66',
                 32: '-64', 33: '-62', 34: '-60', 35: '-58', 36: '-56', 37: '-54',
                 38: '-52', 39: '-50', 40: '-48', 41: '-46', 42: '-44', 43: '-42',
                 44: '-40', 45: '-38', 46: '-36', 47: '-34', 48: '-32', 49: '-30',
                 50: '-28', 51: '-26', 52: '-24', 53: '-22', 54: '-20', 55: '-18',
                 56: '-16', 57: '-14', 58: '-12', 59: '-10', 60: '-8', 61: '-6',
                 62: '-4', 63: '-2', 64: '0', 65: '2', 66: '4', 67: '6', 68: '8',
                 69: '10', 70: '12', 71: '14', 72: '16', 73: '18', 74: '20', 75: '22',
                 76: '24', 77: '26', 78: '28', 79: '30', 80: '32', 81: '34', 82: '36',
                 83: '38', 84: '40', 85: '42', 86: '44', 87: '46', 88: '48', 89: '50',
                 90: '52', 91: '54', 92: '56', 93: '58', 94: '60', 95: '62', 96: '64',
                 97: '66', 98: '68', 99: '70', 100: '72', 101: '74', 102: '76',
                 103: '78', 104: '80', 105: '82', 106: '84', 107: '86', 108: '88',
                 109: '90', 110: '92', 111: '94', 112: '96', 113: '98', 114: '100'})

# FIXME:
# This parameter has a problem I don't know how to solve:
# in the manual it is shown as L63 - 0 - R63, bay spanning 0x00 to 0x7D. The first range is 127 and the second 128.
# To cope with this situation, I put 2 zeroes in the middle instead of 1.
# No idea if it's a good idea!
#
PARAM_PAN63 = ({0: 'L63', 1: 'L62', 2: 'L61', 3: 'L60', 4: 'L59', 5: 'L58', 6: 'L57', 7: 'L56',
                8: 'L55', 9: 'L54', 10: 'L53', 11: 'L52', 12: 'L51', 13: 'L50', 14: 'L49',
                15: 'L48', 16: 'L47', 17: 'L46', 18: 'L45', 19: 'L44', 20: 'L43', 21: 'L42',
                22: 'L41', 23: 'L40', 24: 'L39', 25: 'L38', 26: 'L37', 27: 'L36', 28: 'L35',
                29: 'L34', 30: 'L33', 31: 'L32', 32: 'L31', 33: 'L30', 34: 'L29', 35: 'L28',
                36: 'L27', 37: 'L26', 38: 'L25', 39: 'L24', 40: 'L23', 41: 'L22', 42: 'L21',
                43: 'L20', 44: 'L19', 45: 'L18', 46: 'L17', 47: 'L16', 48: 'L15', 49: 'L14',
                50: 'L13', 51: 'L12', 52: 'L11', 53: 'L10', 54: 'L9', 55: 'L8', 56: 'L7',
                57: 'L6', 58: 'L5', 59: 'L4', 60: 'L3', 61: 'L2', 62: 'L1', 63: '0', 64: '0',
                65: 'R1', 66: 'R2', 67: 'R3', 68: 'R4', 69: 'R5', 70: 'R6', 71: 'R7', 72: 'R8',
                73: 'R9', 74: 'R10', 75: 'R11', 76: 'R12', 77: 'R13', 78: 'R14', 79: 'R15',
                80: 'R16', 81: 'R17', 82: 'R18', 83: 'R19', 84: 'R20', 85: 'R21', 86: 'R22',
                87: 'R23', 88: 'R24', 89: 'R25', 90: 'R26', 91: 'R27', 92: 'R28', 93: 'R29',
                94: 'R30', 95: 'R31', 96: 'R32', 97: 'R33', 98: 'R34', 99: 'R35', 100: 'R36',
                101: 'R37', 102: 'R38', 103: 'R39', 104: 'R40', 105: 'R41', 106: 'R42',
                107: 'R43', 108: 'R44', 109: 'R45', 110: 'R46', 111: 'R47', 112: 'R48',
                113: 'R49', 114: 'R50', 115: 'R51', 116: 'R52', 117: 'R53', 118: 'R54',
                119: 'R55', 120: 'R56', 121: 'R57', 122: 'R58', 123: 'R59', 124: 'R60',
                125: 'R61', 126: 'R62', 127: 'R63'})


PARAM_PAN20 = ({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8',
                9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15',
                16: '16', 17: '17', 18: '18', 19: '19', 20: '20'})

PARAM_DEPTH20 = ({44: '-20', 45: '-19', 46: '-18', 47: '-17', 48: '-16', 49: '-15',
                  50: '-14', 51: '-13', 52: '-12', 53: '-11', 54: '-10', 55: '-9',
                  56: '-8', 57: '-7', 58: '-6', 59: '-5', 60: '-4', 61: '-3', 62: '-2',
                  63: '-1', 64: '0', 65: '1', 66: '2', 67: '3', 68: '4', 69: '5',
                  70: '6', 71: '7', 72: '8', 73: '9', 74: '10', 75: '11', 76: '12',
                  77: '13', 78: '14', 79: '15', 80: '16', 81: '17', 82: '18', 83: '19',
                  84: '20'})

PARAM_PHASE = ({0: '0', 1: '2', 2: '4', 3: '6', 4: '8', 5: '10', 6: '12', 7: '14', 8: '16',
                9: '18', 10: '20', 11: '22', 12: '24', 13: '26', 14: '28', 15: '30',
                16: '32', 17: '34', 18: '36', 19: '38', 20: '40', 21: '42', 22: '44',
                23: '46', 24: '48', 25: '50', 26: '52', 27: '54', 28: '56', 29: '58',
                30: '60', 31: '62', 32: '64', 33: '66', 34: '68', 35: '70', 36: '72',
                37: '74', 38: '76', 39: '78', 40: '80', 41: '82', 42: '84', 43: '86',
                44: '88', 45: '90', 46: '92', 47: '94', 48: '96', 49: '98', 50: '100',
                51: '102', 52: '104', 53: '106', 54: '108', 55: '110', 56: '112',
                57: '114', 58: '116', 59: '118', 60: '120', 61: '122', 62: '124',
                63: '126', 64: '128', 65: '130', 66: '132', 67: '134', 68: '136',
                69: '138', 70: '140', 71: '142', 72: '144', 73: '146', 74: '148',
                75: '150', 76: '152', 77: '154', 78: '156', 79: '158', 80: '160',
                81: '162', 82: '164', 83: '166', 84: '168', 85: '170', 86: '172',
                87: '174', 88: '176', 89: '178', 90: '180'})

# PARAM_ROOM = tools.mergeRanges(range(0x00, 0x06), ['Room1', 'Room2', 'Plate1', 'Plate2', 'Hall1', 'Hall2'])
PARAM_ROOM = ({0: 'Room1', 1: 'Room2', 2: 'Plate1/Stage1', 3: 'Plate2/Stage2', 4: 'Hall1', 5: 'Hall2'})

# PARAM_HFDAMP = tools.mergeRanges(range(0x00, 0x0B), tools.ulist(-10, 0, 1))
PARAM_HFDAMP = ({0: '-10', 1: '-9', 2: '-8', 3: '-7', 4: '-6', 5: '-5',
                 6: '-4', 7: '-3', 8: '-2', 9: '-1', 10: '0'})

# PARAM_DIFFUSION = tools.mergeRanges(range(0x00, 0x0B), tools.ulist(0, 10, 1))
PARAM_DIFFUSION = ({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10'})

#PARAM_FEEDBACK_48 = tools.mergeRanges(range(0x28, 0x59), tools.ulist(-48, +48, 2, '%'))
PARAM_FEEDBACK_48 = ({40: '-48%', 41: '-46%', 42: '-44%', 43: '-42%', 44: '-40%', 45: '-38%', 46: '-36%',
                      47: '-34%', 48: '-32%', 49: '-30%', 50: '-28%', 51: '-26%', 52: '-24%', 53: '-22%',
                      54: '-20%', 55: '-18%', 56: '-16%', 57: '-14%', 58: '-12%', 59: '-10%', 60: '-8%',
                      61: '-6%', 62: '-4%', 63: '-2%', 64: '0%', 65: '2%', 66: '4%', 67: '6%', 68: '8%',
                      69: '10%', 70: '12%', 71: '14%', 72: '16%', 73: '18%', 74: '20%', 75: '22%', 76: '24%',
                      77: '26%', 78: '28%', 79: '30%', 80: '32%', 81: '34%', 82: '36%', 83: '38%', 84: '40%',
                      85: '42%', 86: '44%', 87: '46%', 88: '48%'})

# PARAM_LMGAIN_6024 = tools.mergeRanges(range(0x04, 0x59), tools.ulist(-60, +24, 1, 'dB'))
PARAM_LMGAIN_6024 = ({4: '-60dB', 5: '-59dB', 6: '-58dB', 7: '-57dB', 8: '-56dB', 9: '-55dB', 10: '-54dB', 11: '-53dB',
                      12: '-52dB', 13: '-51dB', 14: '-50dB', 15: '-49dB', 16: '-48dB', 17: '-47dB', 18: '-46dB',
                      19: '-45dB', 20: '-44dB', 21: '-43dB', 22: '-42dB', 23: '-41dB', 24: '-40dB', 25: '-39dB',
                      26: '-38dB', 27: '-37dB', 28: '-36dB', 29: '-35dB', 30: '-34dB', 31: '-33dB', 32: '-32dB',
                      33: '-31dB', 34: '-30dB', 35: '-29dB', 36: '-28dB', 37: '-27dB', 38: '-26dB', 39: '-25dB',
                      40: '-24dB', 41: '-23dB', 42: '-22dB', 43: '-21dB', 44: '-20dB', 45: '-19dB', 46: '-18dB',
                      47: '-17dB', 48: '-16dB', 49: '-15dB', 50: '-14dB', 51: '-13dB', 52: '-12dB', 53: '-11dB',
                      54: '-10dB', 55: '-9dB', 56: '-8dB', 57: '-7dB', 58: '-6dB', 59: '-5dB', 60: '-4dB', 61: '-3dB',
                      62: '-2dB', 63: '-1dB', 64: '0dB', 65: '1dB', 66: '2dB', 67: '3dB', 68: '4dB', 69: '5dB',
                      70: '6dB', 71: '7dB', 72: '8dB', 73: '9dB', 74: '10dB', 75: '11dB', 76: '12dB', 77: '13dB',
                      78: '14dB', 79: '15dB', 80: '16dB', 81: '17dB', 82: '18dB', 83: '19dB', 84: '20dB',
                      85: '21dB', 86: '22dB', 87: '23dB', 88: '24dB'})
#PARAM_LMTHRESHOLD_60_0 = tools.mergeRanges(range(0x04, 0x041), tools.ulist(-60, 0, 1, 'dB'))
PARAM_LMTHRESHOLD_60_0 = ({4: '-60dB', 5: '-59dB', 6: '-58dB', 7: '-57dB', 8: '-56dB', 9: '-55dB', 10: '-54dB',
                           11: '-53dB', 12: '-52dB', 13: '-51dB', 14: '-50dB', 15: '-49dB', 16: '-48dB', 17: '-47dB',
                           18: '-46dB', 19: '-45dB', 20: '-44dB', 21: '-43dB', 22: '-42dB', 23: '-41dB', 24: '-40dB',
                           25: '-39dB', 26: '-38dB', 27: '-37dB', 28: '-36dB', 29: '-35dB', 30: '-34dB', 31: '-33dB',
                           32: '-32dB', 33: '-31dB', 34: '-30dB', 35: '-29dB', 36: '-28dB', 37: '-27dB', 38: '-26dB',
                           39: '-25dB', 40: '-24dB', 41: '-23dB', 42: '-22dB', 43: '-21dB', 44: '-20dB', 45: '-19dB',
                           46: '-18dB', 47: '-17dB', 48: '-16dB', 49: '-15dB', 50: '-14dB', 51: '-13dB', 52: '-12dB',
                           53: '-11dB', 54: '-10dB', 55: '-9dB', 56: '-8dB', 57: '-7dB', 58: '-6dB', 59: '-5dB',
                           60: '-4dB', 61: '-3dB', 62: '-2dB', 63: '-1dB', 64: '0dB'})

# PARAM_MODESELECT = tools.mergeRanges(range(0x00, 0x06), tools.ulist(1, 6, 1))
PARAM_MODESELECT = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6'}

# PARAM_ENHANCER = tools.mergeRanges(range(0x00, 0x80), tools.ulist(-64, 63, 1))
PARAM_ENHANCER =({0: '-64', 1: '-63', 2: '-62', 3: '-61', 4: '-60', 5: '-59', 6: '-58', 7: '-57', 8: '-56', 9: '-55',
                  10: '-54', 11: '-53', 12: '-52', 13: '-51', 14: '-50', 15: '-49', 16: '-48', 17: '-47', 18: '-46',
                  19: '-45', 20: '-44', 21: '-43', 22: '-42', 23: '-41', 24: '-40', 25: '-39', 26: '-38', 27: '-37',
                  28: '-36', 29: '-35', 30: '-34', 31: '-33', 32: '-32', 33: '-31', 34: '-30', 35: '-29', 36: '-28',
                  37: '-27', 38: '-26', 39: '-25', 40: '-24', 41: '-23', 42: '-22', 43: '-21', 44: '-20', 45: '-19',
                  46: '-18', 47: '-17', 48: '-16', 49: '-15', 50: '-14', 51: '-13', 52: '-12', 53: '-11', 54: '-10',
                  55: '-9', 56: '-8', 57: '-7', 58: '-6', 59: '-5', 60: '-4', 61: '-3', 62: '-2', 63: '-1', 64: '0',
                  65: '1', 66: '2', 67: '3', 68: '4', 69: '5', 70: '6', 71: '7', 72: '8', 73: '9', 74: '10', 75: '11',
                  76: '12', 77: '13', 78: '14', 79: '15', 80: '16', 81: '17', 82: '18', 83: '19', 84: '20', 85: '21',
                  86: '22', 87: '23', 88: '24', 89: '25', 90: '26', 91: '27', 92: '28', 93: '29', 94: '30', 95: '31',
                  96: '32', 97: '33', 98: '34', 99: '35', 100: '36', 101: '37', 102: '38', 103: '39', 104: '40',
                  105: '41', 106: '42', 107: '43', 108: '44', 109: '45', 110: '46', 111: '47', 112: '48', 113: '49',
                  114: '50', 115: '51', 116: '52', 117: '53', 118: '54', 119: '55', 120: '56', 121: '57', 122: '58',
                  123: '59', 124: '60', 125: '61', 126: '62', 127: '63'})

#PARAM_MODE_1_4 = tools.mergeRanges(range(0x00, 0x04), ['Mode1', 'Mode2', 'Mode3', 'Mode4'])
PARAM_MODETYPE_1_4 = {0: 'Mode1', 1: 'Mode2', 2: 'Mode3', 3: 'Mode4'}

# PARAM_PREFILTER = tools.mergeRanges(range(0x00, 0x03), ['Off', 'LPF', 'HPF'])
PARAM_PREFILTER = {0: 'Off', 1: 'LPF', 2: 'HPF'}

# TODO: Finish to add all necessary PARAM constants to complete the effects...

# Let's initialise the dictionaries with the parameters.
FULL_EFX_TYPE = {}
FULL_EFX_PARAMETERS = {}

# FULL_EFX_PARAMETERS[]: How to build them (brainstorming)
# I need ranges in human form, bisides the HEX one for the SYSEX, so that the SPINBOX can show the human value and apply
# the HEX value (whereas the decimal value would be fine too)
# By now, if FULL_EFX_PARAMETERS[x] = par, we have
# par[0]: parameter name (i.e. 'Reverb Time');
# par[1]: range in "human" form
# par[2]: complete hex range -> the single values must be passed through SYSEX
# **** par[2] is a dictionaru where keys are hex values to pass and argument is the human value
# **** **** like: {0: '0ms', 1: '1ms'}
# par[3]: LSB/MSB of the parameter -> to pass to SYSEX
# par[4]: default value (hex or decimal)
#

# TODO: get rid of "mergeRange" to make the code faster.
# So, we don't want to calculate the mergedRange on the fly, but put it statically in the definitions.

# FULL EFFECT MODE
FULL_EFX_TYPE[1] = ('High Quality Reverb', [0x00, 0x11])
FULL_EFX_PARAMETERS[1] = (
    ('Type', 'Room1/2/Plate1/2/Hall1/2', PARAM_ROOM, [0x03], 0x03),
    ('Pre Dly', '0ms - 80ms - 635ms', PARAM_TYPE_5, [0x04], 0x10),
    ('Reverb Time', '0.1s - 2s - 38s', PARAM_TYPE_16, [0x05], 0x13),
    ('HF Damp', '-10 - -4 -0', PARAM_HFDAMP, [0x06], 0x06),
    ('ER Pre Dly', '0 - 40ms - 635 ms', PARAM_TYPE_5, [0x07], 0x08),
    ('ER Mix', '0 - 15 - 127', PARAM_0127, [0x08], 0x0f),
    ('Diffusion', '0 - 9 - 10', PARAM_DIFFUSION, [0x09], 0x09),
    ('Tone Low', '-12dB - 0dB - +12dB', PARAM_12DB, [0x0A], 0x40),
    ('Tone High', '-12dB - 0dB - +12dB', PARAM_12DB, [0x0B], 0x40),
    ('Balance', 'D > 0E - D0 < E', PARAM_BALANCE, [0x0C], 0x7f),
    ('EQ Low Freq', '200/400Hz', {0: '200Hz', 1: '400Hz'}, [0x0D], 0x00),
    ('EQ Low Gain', '-12dB - 0dB - +12dB', PARAM_12DB, [0x0E], 0x40),
    ('EQ Mid1 Freq', '200Hz - 315Hz - 6300 Hz', PARAM_TYPE_10, [0x0F], 16),
    ('EQ Mid1 Q', '0.5/1.0/2.0/4.0/9.0', {0: '0.5', 1: '1.0', 2: '2.0', 3: '4.0', 4: '9.0'}, [0x10], 0),
    ('EQ Mid1 Gain', '-12dB - 0dB - +12dB', PARAM_12DB, [0x11], 0x40),
    ('EQ Mid2 Freq', '200Hz - 800Hz - 6300 Hz', PARAM_TYPE_10, [0X12], 48),
    ('EQ Mid2 Q', '0.5/1.0/2.0/4.0/9.0', {0: '0.5', 1: '1.0', 2: '2.0', 3: '4.0', 4: '9.0'}, [0x13], 1),
    ('EQ Mid2 Gain', '-12dB - 0dB - +12dB', PARAM_12DB, [0x14], 0x40),
    ('EQ High Freq', '4k/8kHz', {0: '4kHz', 1: '8kHz'}, [0x15], 0),
    ('EQ High Gain', '-12dB - 0dB - +12dB', PARAM_12DB, [0x16], 0x40)
)

FULL_EFX_TYPE[2] = ('Mic Simulator', [0x00, 0x12])
FULL_EFX_PARAMETERS[2] = (
    ('Mic Conv', 'Off/On', PARAM_ON_OFF, [0x03], 1),
    ('Input', 'DR-20/Sml.Dy/Hed.Dy/Flat', {0: 'DR-20', 1: 'Sml.Dy', 2: 'Hed.Dy', 3: 'Flat'}, [0x04], 3),
    ('Output', 'Sml.Dy/Voc.Dy/Lrg.Dy/Sml.Cn/Lrg.Cn/Vnt.C/Flat',
     {0: 'Sml.Dy', 1: 'Voc.Dy', 2: 'Lrg.Dy', 3: 'Sml.Cn', 4: 'Lrg.Cn', 5: 'Vnt.C', 6: 'Flat'}, [0x05], 4),
    ('Phase', '+/-', {0: '-', 1: '+'}, [0x06], 1),
    ('Bass Cut Switch', 'Off/On', PARAM_ON_OFF, [0x07], 0),
    ('Bass Cut Freq', '20Hz-2000Hz', PARAM_TYPE_15, [0x08], 0),
    ('Distance Switch', 'Off/On', PARAM_ON_OFF, [0x09], 0),
    ('Prox. Fx', '-12dB - 0dB - +12dB', PARAM_12DB, [0x0A], 0x40),
    ('Distance', '0-127', PARAM_0127, [0x0B], 0),
    ('Limiter Switch', 'Off/On', PARAM_ON_OFF, [0x0C], 0),
    ('Lm Freq', '20Hz - 115Hz - 2000Hz', PARAM_TYPE_15, [0x0D], 40),
    ('Lm Gain', '-60dB - +2dB - +24dB', PARAM_LMGAIN_6024, [0x0E], 66),
    ('Lm Threshold', '-60db - 0dB', PARAM_LMTHRESHOLD_60_0, [0x0F], 0x40),
    ('Lm Attack', '0 - 20 - 127', PARAM_0127, [0x10], 20),
    ('Lm Release', '0 - 30 - 127', PARAM_0127, [0x11], 30)
)

FULL_EFX_TYPE[3] = ('Vocoder', [0x00, 0x13])
FULL_EFX_PARAMETERS[3] = (
    ('Speech Input', 'Mic1/2/Wave1/2', {0: 'Mic1', 1: 'Mic2', 2: 'Wave1', 3: 'Wave2'}, [0x03], 0x00),
    ('Mode Select', '1 - 3 - 6', PARAM_MODESELECT, [0x04], 0x02),
    ('Speech Gain', '0 - 100 - 127', PARAM_0127, [0x05], 100),
    ('Speech Cutoff', '250Hz - 630Hz - 800Hz', PARAM_TYPE_9, [0x06], 32),
    ('Speech Mix Level', '0 - 25 -127', PARAM_0127, [0x07], 25),
    ('Response Time', 'Slow/Normal/Fast', {0: 'Slow', 1: 'Normal', 2: 'Fast'}, [0x08], 0x01),
    ('Level', '0 - 127', PARAM_0127, [0x09], 0x7F)
)

FULL_EFX_TYPE[4] = ('Vocal Multi', [0x00, 0x14])
FULL_EFX_PARAMETERS[4] = (
    ('Ns Threshold', '0 - 127', PARAM_0127, [0x03], 0x00),
    ('Lm Threshol', '0 - 127', PARAM_0127, [0x04], 0x7F),
    ('De-esser Level', '0 - 127', PARAM_0127, [0x05], 0x08),
    ('Enhancer Level', '-64 - +5 - +63', PARAM_ENHANCER, [0x06], 69),
    ('EQ Low Gain', '-12dB - 0dB - +12dB', PARAM_12DB, [0x07], 0x41),
    ('EQ Mid Freq', '200Hz - 800Hz - 6300 Hz', PARAM_TYPE_10, [0x08], 48),
    ('EQ Mid Q', '0.5/1.0/2.0/4.0/9.0', {0: '0.5', 1: '1.0', 2: '2.0', 3: '4.0', 4: '9.0'}, [0x09], 1),
    ('EQ Mid Gain', '-12dB - +2dB - +12dB', PARAM_12DB, [0x0A], 0x42),
    ('EQ High Gain', '-12dB - -4dB - +12dB', PARAM_12DB, [0x0B], 0x3C),
    ('Ps P.Coarse', '-24  -0 - +12', PARAM_2412, [0x0C], 0x40),
    ('Ps P.Fine', '-100 -48 - +100', PARAM_100100, [0x0D], 40),
    ('Ps Balance', 'D > 0E - D > 42E - D0 <E', PARAM_BALANCE, [0x0E], 28),
    ('Dly Time', '0ms - 260ms - 500ms', PARAM_TYPE_4, [0x0F], 112),
    ('Dly Feedback', '-98% - -10% - +98%', PARAM_9898, [0x10], 59),
    ('Dly Balance', 'D > 0E - D > 22E - D0 < E', PARAM_BALANCE, [0x11], 15),
    ('Cho Rate', '0.05 - 0.65 - 10.0', PARAM_TYPE_6, [0x12], 12),
    ('Cho Depth', '0 - 30 - 127', PARAM_0127, [0x13], 30),
    ('Cho Balance', 'D > 0 E - D=E - D0 < E', PARAM_BALANCE, [0x14], 0)
)

FULL_EFX_TYPE[5] = ('Game', [0x00, 0x16])
FULL_EFX_PARAMETERS[5] = (
    ('Enhancer Level', '-64 - +35 - +63', PARAM_ENHANCER, [0x03], 69),
    ('Low Boost Level', '0dB - +8dB - 18dB', PARAM_0_18DB, [0x04], 72),
    ('Low Boost Freq','60Hz - 400Hz', PARAM_TYPE_17, [0x05], 9),
    ('Lm Mix Level','0 - 127', PARAM_0127 , [0x06], 127),
    ('GtRv Mix Level','0 - 70 - 127', PARAM_0127 , [0x07], 70),
    ('Rv Mix Level','0 - 60 - 127', PARAM_0127, [0x08], 60),
    ('3D Switch','Off / On', PARAM_ON_OFF , [0x09], 1),
    ('3D Range','1 - 3 -4', PARAM_1_4, [0x0A], 2),
    ('Out','Speaker/Phones', {0: 'Speaker', 1: 'Phones'}, [0x0B], 0),
    ('Lm Threshold','0 - 112 - 127', PARAM_0127, [0x0C], 112),
    ('GtRv Pre Dly','0ms - 20ms - 100ms', PARAM_TYPE_1, [0x0D], 70), # NOTE: ranges in the docs is wrong!
    ('GtRv Time','5ms - 15ms - 500ms', PARAM_TYPE_5_SHORT, [0x0E], 3),
    ('Rv Type','Room1/2/Stage1/2/Hall1/2', PARAM_ROOM, [0x0F], 5),
    ('Rv Pre Delay','0ms - 200ms - 500ms', PARAM_TYPE_4, [0x10], 106),
    ('Rv Time','0 - 26 -127', PARAM_0127, [0x11], 26),
    ('Rv HF Damp','315Hz - 6.3kHz - 8kHz', PARAM_TYPE_8, [0x12], 104),
    ('Rv Low Gain','-12dB - +2dB - +12dB', PARAM_12DB, [0x13], 66),
    ('Rv High Gain','-12dB - -4dB - +12dB', PARAM_12DB, [0x14], 60),
    ('Low Gain','-12dB - +2dB - +12dB', PARAM_12DB, [0x15], 66),
    ('High Gain','-12dB - +4dB - +12dB', PARAM_12DB, [0x16], 68),
    ('Level', '0 - 100 - 127', PARAM_0127, [0x17], 100)
)

# 6: Rotary Multi
# this is the same as COMPACT_INS_EFX_PARAMETERS[47] defined later (the other way round as described in the documentation)
FULL_EFX_TYPE[6] = ('Rotary Multi', [0x03, 0x00])
FULL_EFX_PARAMETERS[6] = (
    ('OD Drive', '0 - 40 - 127', PARAM_0127, [0x03], 40),
    ('OD Sw', 'Off/*On', PARAM_ON_OFF, [0x04], 1),
    ('EQ L Gain', '-12dB - 0dB - +12dB', PARAM_12DB, [0x05], 0x41),
    ('EQ M Fq', '200Hz - 1.6kHz - 6.3kHz', PARAM_TYPE_10, [0x06], 72),
    # ('EQ M Q', '0.5/1.0/2.0/4.0/9.0', mergedRange, [0x07], _default_),
    ('EQ M Gain', '-12dB - 0dB - +12dB', PARAM_12DB, [0x08], 64),
    ('EQ H Gain', '-12dB - 0dB - +12dB', PARAM_12DB, [0x09], 64),
    ('RT L Slow', '0.05Hz - 0.35Hz - 10.0Hz', PARAM_TYPE_6, [0x0A], 6),
    ('RT L Fast', '0.05Hz - 6.40Hz - 10.0Hz', PARAM_TYPE_6, [0x0B], 113),
    ('RT Lo Accl', '0 - 3 - 15', PARAM_TYPE_14, [0x0C], 24),
    ('RT Lo Lev', '0 - 127', PARAM_0127, [0x0D], 127),
    ('RT H Slow', '0.05Hz - 0.90Hz - 10.0Hz', PARAM_TYPE_6, [0x0E], 17),
    ('RT H Fast', '0.05Hz - 7.50Hz - 10.0Hz', PARAM_TYPE_6, [0x0F], 120),
    ('RT Hi Accl', '0 - 11 - 15', PARAM_TYPE_14, [0x10], 88),
    ('RT Hi Lev', '0 - 64 - 127', PARAM_0127, [0x11], 64),
    ('RT Sept', '0 - 90 - 127', PARAM_0127, [0x12], 90),
    #('RT Speed', 'Slow/Fast', mergedRange, [0x13], _default_),
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 30 - 127', PARAM_0127, [0x25], 30)
)

# 7: GTR Multi 1
# this is the same as COMPACT_INS_EFX_PARAMETERS[48] defined later (the other way round as described in the documentation)
FULL_EFX_TYPE[7] = ('GTR Multi 1', [0x04, 0x00])
FULL_EFX_PARAMETERS[7] = (
    ('Cmp Atk', '0 - 80 - 127', PARAM_0127, [0x03], 80),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
)

# 8: GTR Multi 2
# this is the same as COMPACT_INS_EFX_PARAMETERS[49]
FULL_EFX_TYPE[8] = ('GTR Multi 2', [0x04, 0x01])
FULL_EFX_PARAMETERS[8] = (
    ('Cmp Atk', '0 - 80 - 127', PARAM_0127, [0x03], 80),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 40 - 127', PARAM_0127, [0x25], 40)
)

# 9: GTR Multi 3
# this is the same as COMPACT_INS_EFX_PARAMETERS[50]
FULL_EFX_TYPE[9] = ('GTR Multi 3', [0x04, 0x02])
FULL_EFX_PARAMETERS[9] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 40 - 127', PARAM_0127, [0x25], 40)
)

# 10: Clean Gt Multi 1
# this is the same as COMPACT_INS_EFX_PARAMETERS[51]
FULL_EFX_TYPE[10] = ('Clean Gt Multi 1', [0x04, 0x03])
FULL_EFX_PARAMETERS[10] = (
    ('Cmp Atk', '0 - 80 - 127', PARAM_0127, [0x03], 80),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# 11: Clean Gt Multi 2
# this is the same as COMPACT_INS_EFX_PARAMETERS[52]
FULL_EFX_TYPE[11] = ('Clean Gt Multi 2', [0x04, 0x04])
FULL_EFX_PARAMETERS[11] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 100 - 127', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# 12: Bass Multi
# this is the same as COMPACT_INS_EFX_PARAMETERS[53]
FULL_EFX_TYPE[12] = ('Bass Multi', [0x04, 0x05])
FULL_EFX_PARAMETERS[12] = (
    ('Cmp Atk', '0 - 80 - 127', PARAM_0127, [0x03], 80),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 40 - 127', PARAM_0127, [0x25], 40)
)

# 13: E.Piano Multi
# this is the same as COMPACT_INS_EFX_PARAMETERS[54]
FULL_EFX_TYPE[13] = ('E.Piano Multi', [0x04, 0x06])
FULL_EFX_PARAMETERS[13] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# 14: Keyboard Multi
# this is the same as COMPACT_INS_EFX_PARAMETERS[55]
FULL_EFX_TYPE[14] = ('Keyboard Multi', [0x05, 0x00])
FULL_EFX_PARAMETERS[14] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)


# TODO: fill up the missing FULL EFFECTS with their PARAMETERS

# ***********************************************************
# COMPACT EFFECTS MODE
# Let's define the SYS first. They are actually a bit easier.

# REMEMBER: SYS1 only has DELAY and CHORUS
#           SYS2 only has DELAY and REVERB
# THIS MEANS: we must differentiate the two of them somehow. Fuck.

COMPACT_SYS1_EFX_TYPE = ({1: ('Delay', [0x00, 0x21]),
                          2: ('Chorus', [0x00, 0x22])})
COMPACT_SYS2_EFX_TYPE = ({1: ('Delay', [0x00, 0x31]),
                          2: ('Reverb', [0x00, 0x32])})

COMPACT_SYS1_EFX_PARAMETERS = {}

COMPACT_SYS1_EFX_PARAMETERS[1] = (
    ('Dly Tm LtoL', '0.0ms - 110ms - 360ms', PARAM_TYPE_4_SHORT, [0x03], 97),
    ('Dly Tm LtoR', '0.0ms - 13.0ms - 360ms', PARAM_TYPE_4_SHORT, [0x04], 63),
    ('Dly Tm RtoR', '0.0ms - 100ms - 360ms', PARAM_TYPE_4_SHORT, [0x05], 96),
    ('Dly Tm RtoL', '0.0ms - 8.0ms - 360ms', PARAM_TYPE_4_SHORT, [0x06], 56),
    ('Feedback Level', '-48% - -34% - +48%', PARAM_FEEDBACK_48, [0x07], 47),
    ('Cross Fd Level', '-48% - -34% - +48%', PARAM_FEEDBACK_48, [0x08], 47),
    ('HF Damp', '315Hz - 8kHz/Bypass', PARAM_TYPE_8, [0x09], 120),
    ('Cross HF Damp', '315Hz - 6.3kHz - 8kHz/Bypass', PARAM_TYPE_8, [0x0A], 104),
    ('Cross Balance', '0-98-127', PARAM_0127, [0x0B], 0x62),
    ('Balance', 'D > 0E - D0 < E', PARAM_BALANCE, [0x0C], 0x7F)
)

COMPACT_SYS1_EFX_PARAMETERS[2] = (
    ('Type', 'Mode 1 - 2 - 4', PARAM_MODETYPE_1_4, [0x03], 0x01),
    ('Pre Filter', 'Off/LPF/HPF', PARAM_PREFILTER, [0x04], 0x02),
    ('Cutoff', '250Hz - 630Hz - 8000Hz', PARAM_TYPE_9, [0x05], 32),
    ('Pre Dly', '0ms - 100ms', PARAM_TYPE_1, [0x06], 80),
    ('Rate', '0.05 - 0.35 - 10.0', PARAM_TYPE_6, [0x07], 6),
    ('Depth', '0-116-127', PARAM_0127, [0x08], 0x74),
    ('Balance', 'D > 0E - D0 < E', PARAM_BALANCE, [0x09], 0x7F)
)
COMPACT_SYS2_EFX_PARAMETERS = {}

COMPACT_SYS2_EFX_PARAMETERS[1] = (
    ('Dly Tm LtoL', '0.0ms - 110ms - 360ms', PARAM_TYPE_4_SHORT, [0x03], 97),
    ('Dly Tm LtoR', '0.0ms - 13.0ms - 360ms', PARAM_TYPE_4_SHORT, [0x04], 63),
    ('Dly Tm RtoR', '0.0ms - 100ms - 360ms', PARAM_TYPE_4_SHORT, [0x05], 96),
    ('Dly Tm RtoL', '0.0ms - 8.0ms - 360ms', PARAM_TYPE_4_SHORT, [0x06], 56),
    ('Feedback Level', '-48% - -34% - +48%', PARAM_FEEDBACK_48, [0x07], 47),
    ('Cross Fd Level', '-48% - -34% - +48%', PARAM_FEEDBACK_48, [0x08], 47),
    ('HF Damp', '315Hz - 8kHz/Bypass', PARAM_TYPE_8, [0x09], 120),
    ('Cross HF Damp', '315Hz - 6.3kHz - 8kHz/Bypass', PARAM_TYPE_8, [0x0A], 104),
    ('Cross Balance', '0-98-127', PARAM_0127, [0x0B], 0x62),
    ('Balance', 'D > 0E - D0 < E', PARAM_BALANCE, [0x0C], 0x7F)
)

COMPACT_SYS2_EFX_PARAMETERS[2] = (
    ('Type', 'Room1/2/Plate1/2/Hall1/2', PARAM_ROOM, [0x03], 0x05),
    ('Pre Dly', '0ms - 100ms', PARAM_TYPE_1, [0x04], 0x7F),
    ('Reverb Time', '0 - 23 - 127', PARAM_0127, [0x05], 0x17),
    ('HF Damp','315 - 8kHz/Bypass', PARAM_TYPE_8, [0X06], 120),
    ('Low Gain', '-12dB - +2dB - +12dB', PARAM_12DB, 66),
    ('High Gain', '-12dB - -6dB - +12dB', PARAM_12DB, 58),
    ('Balance', 'D > 0E - D0 < E', PARAM_BALANCE, [0x09], 0x7F)
)

# Now we must define the COMPACT INSERTION EFFECT.
# Remember: they are grouped, as in the documentation

COMPACT_INS_EFX_GROUP = ({
    # Effects that modify the tone (filter type)
    0: ('Filter', range(0, 5)),
    # Effects that distort the sound (distortion type)
    1: ('Distorsion', range(5, 7)),
    # Effects that modulate the sound (modulation type)
    2: ('Modulation', range(7, 14)),
    # Effects that affect the level (compressor type)
    3: ('Compressor', range(14, 16)),
    # Effects that broaden the sound (chorus type)
    4: ('Chorus', range(16, 21)),
    # Effects that reverberate the sound (delay/reverb type)
    5: ('Delay/Reverb', range(21, 29)),
    # Effects that modify the pitch (pitch shift type)
    6: ('Pitch', range(29, 31)),
    #  Other Effects
    7: ('Other', range(31, 35)),
    # Effects that connect two types of effect in series (series 2)
    8: ('Connect 2 effects (series)', range(35, 47)),
    # Effects that connect three or more types of effecs in series (series 3/series 4/series 5)
    9: ('Connect 3 or more effects (series)', range(47, 56)),
    # Effects that connect two types of effect in parallel (parallel 2)
    10: ('Connect 2 effects (parallel)', range(56, 65))}
)

COMPACT_INS_EFX_TYPE = ({
    # Effects that modify the tone (filter type)
    0: ('Noise Suppressor', [0x00, 0x00]),
    1: ('Stereo Eq', [0x01, 0x00]),
    2: ('Spectrum', [0x01, 0x01]),
    3: ('Enhancer', [0x01, 0x02]),
    4: ('Humanizer', [0x01, 0x03]),
    # Effects that distort the sound (distortion type)
    5: ('Overdrive', [0x01, 0x10]),
    6: ('Distorsion', [0x01, 0x11]),
    # Effects that modulate the sound (modulation type)
    7: ('Phaser', [0x01, 0x20]),
    8: ('Auto Wah', [0x01, 0x21]),
    9: ('Rotary', [0x01, 0x22]),
    10: ('Stereo Flanger', [0x01, 0x23]),
    11: ('Step Flanger', [0x01, 0x24]),
    12: ('Tremolo', [0x01, 0x25]),
    13: ('Auto Pan', [0x01, 0x26]),
    # Effects that affect the level (compressor type)
    14: ('Compressor', [0x01, 0x30]),
    15: ('Limiter', [0x01, 0x31]),
    16: ('Hexa Chorus', [0x01, 0x40]),
    # Effects that broaden the sound (chorus type)
    17: ('Tremolo Chorus', [0x01, 0x41]),
    18: ('Stereo Chorus', [0x01, 0x42]),
    19: ('Space D', [0x01, 0x43]),
    20: ('3D Chorus', [0x01, 0x44]),
    # Effects that reverberate the sound (delay/reverb type)
    21: ('Stereo Delay', [0x01, 0x50]),
    22: ('Mod Delay', [0x01, 0x51]),
    23: ('3 Tap Delay', [0x01, 0x52]),
    24: ('4 Tap Delay', [0x01, 0x53]),
    25: ('Tm Ctrl Delay', [0x01, 0x54]),
    26: ('Reverb', [0x01, 0x55]),
    27: ('Gate Reverb', [0x01, 0x56]),
    28: ('3D Delay', [0x01, 0x57]),
    # Effects that modify the pitch (pitch shift type)
    29: ('Pitch Shifter', [0x01, 0x60]),
    30: ('Fb P, Shifter', [0x01, 0x61]),
    #  Other Effects
    31: ('3D Auto', [0x01, 0x70]),
    32: ('3D Manual', [0x01, 0x71]),
    33: ('Lo-Fi 1', [0x01, 0x72]),
    34: ('Lo-Fi 2', [0x01, 0x73]),
    # Effects that connect two types of effect in series (series 2)
    35: ('OD -> Chorus', [0x02, 0x00]),
    36: ('OD -> Flanger', [0x02, 0x01]),
    37: ('OD -> Delay', [0x02, 0x02]),
    38: ('DS -> Chorus', [0x02, 0x03]),
    39: ('DS -> Flanger', [0x02, 0x04]),
    40: ('DS -> Delay', [0x02, 0x05]),
    41: ('EH -> Choru', [0x02, 0x06]),
    42: ('EH -> Flanger', [0x02, 0x07]),
    43: ('EH -> Delay', [0x02, 0x08]),
    44: ('Cho -> Delay', [0x02, 0x09]),
    45: ('FL -> Delay', [0x02, 0x0A]),
    46: ('Cho -> Flanger', [0x02, 0x0B]),
    # Effects that connect three or more types of effecs in series (series 3/series 4/series 5)
    47: ('Rotary Multi', [0x03, 0x00]),
    48: ('GTR Multi 1', [0x04, 0x00]),
    49: ('GTR Multi 2', [0x04, 0x01]),
    50: ('GTR Multi 3', [0x04, 0x02]),
    51: ('Clean Gt Multi 1', [0x04, 0x03]),
    52: ('Clean Gt Multi 2', [0x04, 0x04]),
    53: ('Bass Multi', [0x04, 0x05]),
    54: ('E. Piano Multi', [0x04, 0x06]),
    55: ('Keyboard Multi', [0x05, 0x00]),
    # Effects that connect two types of effect in parallel (parallel 2)
    56: ('Cho / Delay', [0x11, 0x00]),
    57: ('FL / Delay', [0x11, 0x01]),
    58: ('Cho / Flanger', [0x11, 0x02]),
    59: ('OD1 / OD2', [0x11, 0x03]),
    60: ('OD / Rotary', [0x11, 0x04]),
    61: ('OD / Phaser', [0x11, 0x05]),
    62: ('OD / AutoWah', [0x11, 0x06]),
    63: ('PH / Rotary', [0x11, 0x07]),
    64: ('PH / AutoWah', [0x11, 0x08])
})

COMPACT_INS_EFX_PARAMETERS = {}

# 0: Noise suppressor
COMPACT_INS_EFX_PARAMETERS[0] = (
    ('Noise Suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10),
)

# 1: Stereo Eq
COMPACT_INS_EFX_PARAMETERS[1] = (
    ('Low Freq', '200/400Hz', {0: '200Hz', 1: '400Hz'}, [0x03], 0x00),
    ('Low Gain', '-12dB - +6dB - +12dB', PARAM_12DB, [0x04], 0x46),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    ('Noise Suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# 2: Spectrum
COMPACT_INS_EFX_PARAMETERS[2] = (
    ('Band 1', '-12dB - +5dB - +12dB', PARAM_12DB, [0x03], 0x45),
    ('Band 2', '-12dB - +2dB - +12dB', PARAM_12DB, [0x04], 0x42),
    ('Band 3', '-12dB - -2dB - +12dB', PARAM_12DB, [0x05], 0x3E),
    ('Band 4', '-12dB - -1dB - +12dB', PARAM_12DB, [0x06], 0x3F),
    ('Band 5', '-12dB - +3dB - +12dB', PARAM_12DB, [0x07], 0x43),
    ('Band 6', '-12dB - +5dB - +12dB', PARAM_12DB, [0x08], 0x45),
    ('Band 7', '-12dB - +6dB - +12dB', PARAM_12DB, [0x09], 0x46),
    ('Band 8', '-12dB - -6dB - +12dB', PARAM_12DB, [0x0A], 0x3A),
    ('Width', '0.5/1.0/*2.0*/4.0/9.0', {0: '0.5', 1: '1.0', 2: '2.0', 3: '4.0', 4: '9.0'}, [0x0B], 2),
    # ('Pan', 'L63 - 0 - R63', PARAM_PAN, [0x15], _default_),
    ('Level', '0 - *127*', PARAM_0127, [0x16], 0x7f),
    ('Noise Suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)

)

# TODo: Complete the definitions which lack some parameters...

# 3: Enhancer
COMPACT_INS_EFX_PARAMETERS[3] = (
    ('Sens', '0 - 64 - 127', PARAM_0127, [0x03], 64),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
)

# 4: Humanizer
COMPACT_INS_EFX_PARAMETERS[4] = (
    ('Drive', '0 - 90 - 127', PARAM_0127, [0x03], 90),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
)

# Effects that distort the sound (distortion type)
# 5: Overdrive
COMPACT_INS_EFX_PARAMETERS[5] = (
    ('Drive', '0 - 90 - 127', PARAM_0127, [0x03], 90),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
)

# 6: Distorsion
COMPACT_INS_EFX_PARAMETERS[6] = (
    ('Drive', '0 - 127', PARAM_0127, [0x03], 127),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 70)
)

# Effects that modulate the sound (modulation type)
# 7: Phaser
COMPACT_INS_EFX_PARAMETERS[7] = (
    # ('Manual', '100Hz - 860Hz - 8kHz', PARAM_TYPE_12 *to be defined!* , [0x03], default),
    ('Rate', '0.05Hz - 0.40Hz - 10.0Hz', PARAM_TYPE_6, [0x04], 7),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    ('Level', '0 - 90 - 127', PARAM_0127, [0x16], 90),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# 8: Auto Wah
COMPACT_INS_EFX_PARAMETERS[8] = (
    ('Fil Type', 'LPF/BOF', {0: 'LPF', 1: 'BOF'}, [0x03], 127),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# 9: Rotary
COMPACT_INS_EFX_PARAMETERS[9] = (
    ('Low Slow', '0.05Hz - 0.35Hz - 10.0Hz', PARAM_TYPE_6, [0x03], 6),
    ('Low Fast', '0.05Hz - 6.40Hz - 10.0H', PARAM_TYPE_6, [0x04], 113),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# 10: Stereo Flanger
COMPACT_INS_EFX_PARAMETERS[10] = (
    ('Pre Filter', 'Off/LPF/HPF', {0: 'Off', 1: 'LPF', 2: 'HPF'}, [0x03], 2),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# 11: Step Flanger
COMPACT_INS_EFX_PARAMETERS[11] = (
    ('Pre Dly', '0.0ms - 1.0ms - 100ms', PARAM_TYPE_1, [0x03], 2),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# 12: Tremolo
COMPACT_INS_EFX_PARAMETERS[12] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    ('Mod Rate', '0.05Hz - 6.00Hz - 10.0Hz', PARAM_TYPE_6, [0x04], 109),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# 13: Auto Pan
COMPACT_INS_EFX_PARAMETERS[13] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    ('Mod Depth', '0 - 60 - 127', PARAM_0127, [0x05], 60),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# Effects that affect the level (compressor type)
# 14: Compressor
COMPACT_INS_EFX_PARAMETERS[14] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# 15: Limiter
COMPACT_INS_EFX_PARAMETERS[15] = (
    ('Threshold', '0 - 20 - 127', PARAM_0127, [0x03], 20),
    #('Ratio', '1/1.5, 1/2, 1/4, 1/100', mergedRange, [0x04], 0x02),
    ('Release', '0 - 100 - 127', PARAM_0127, [0x05], 100),
    # ('Post Gain', '0/+6/+12/+18dB', mergedRange, [0x06], 0x02),
    ('Low Gain', '-12dB - 0dB - +12dB', PARAM_12DB , [0x13], 64),
    ('Hi Gain', '-12dB - 0dB - +12dB', PARAM_12DB, [0x14], 64),
    ('Pan', 'L63 - 0 - R63', PARAM_PAN63, [0x15], 63),
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 20 - 127', PARAM_0127, [0x25], 20)
)

# Effects that broaden the sound (chorus type)
# 16: Hexa Chorus
COMPACT_INS_EFX_PARAMETERS[16] = (
    ('Pre Dly', '0.0ms - 2.0ms - 100ms', PARAM_TYPE_1, [0x03], 20),
    ('Rate', '0.05Hz - 0.50Hz - 10.0Hz', PARAM_TYPE_6, [0x04], 9),
    ('Depth', '0 - 40 - 127', PARAM_0127, [0x05], 40),
    ('Pre Dly Dev', '0 - 10 - 20', PARAM_PAN20, [0x06], 10),
    ('Depth Dev', '-20 - 0 - +20', PARAM_DEPTH20, [0x07], 64),
    ('Pan Dev', '0-20', PARAM_PAN20, [0x08], 0x14),
    ('Balance', 'D > 0E - D=E - D0 < E', PARAM_BALANCE, [0x12], 64),
    ('Low Gain', '-12dB - 0dB - +12dB', PARAM_12DB, [0x13], 64),
    ('Hi Gain', '-12dB - 0dB - +12dB', PARAM_12DB, [0x14], 64),
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# 17: Tremolo Chorus
COMPACT_INS_EFX_PARAMETERS[17] = (
    ('Pre Dly', '0.0ms - 2.0ms - 100ms', PARAM_TYPE_1, [0x03], 20),
    ('Cho Rate', '0.05Hz - 0.50Hz - 10.0Hz', PARAM_TYPE_6, [0x04], 9),
    ('Cho Depth', '0 - 40 - 127', PARAM_0127, [0x05], 40),
    ('Trem Phase', '0 - 90 - 180', PARAM_PHASE, [0x06], 45),
    ('Trem Rate', '0.05Hz - 4.00Hz - 10.0Hz', PARAM_TYPE_6, [0x07], 79),
    ('Trem Sep', '0 - 110 - 127', PARAM_0127 , [0x08], 110),
    ('Balance', 'D > 0E - D30 < E - D0 < E', PARAM_BALANCE, [0x12], 20),
    ('Low Gain', '-12dB - 0dB - +12dB', PARAM_12DB, [0x13], 64),
    ('Hi Gain', '-12dB - 0dB - +12dB', PARAM_12DB, [0x14], 64),
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# 18: Stereo Chorus
COMPACT_INS_EFX_PARAMETERS[18] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    ('Depth', '0 - 80 - 127', PARAM_0127, [0x05], 80),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 19: Space D
COMPACT_INS_EFX_PARAMETERS[19] = (
    ('Pre Filter', '0.0ms - 2.0ms - 100ms', PARAM_TYPE_1 , [0x03], 20),
    ('Rate', '0.05Hz - 0.30Hz - 10.0Hz', PARAM_TYPE_6 , [0x04], 5),
    ('Depth', '0 - 80 - 127', PARAM_0127, [0x05], 80),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 20: 3D Chorus
COMPACT_INS_EFX_PARAMETERS[20] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# Effects that reverberate the sound (delay/reverd type)
# 21: Stereo Delay
COMPACT_INS_EFX_PARAMETERS[21] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 22: Mod Delay
COMPACT_INS_EFX_PARAMETERS[22] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 100 - 127', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 23: 3 Tap Delay
COMPACT_INS_EFX_PARAMETERS[23] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 100 - 127', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 24: 4 Tap Delay
COMPACT_INS_EFX_PARAMETERS[24] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 100 - 127', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 25: Tm Ctrl Delay
COMPACT_INS_EFX_PARAMETERS[25] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 100 - 127', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 26: Reverb
COMPACT_INS_EFX_PARAMETERS[26] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 100 - 127', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 27: Gate Reverb
COMPACT_INS_EFX_PARAMETERS[27] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 100 - 127', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 28: 3D Delay
COMPACT_INS_EFX_PARAMETERS[28] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 100 - 127', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# Effects tha modify the pitch (pitch shift type)
# 29: 2 Pitch Shifter
COMPACT_INS_EFX_PARAMETERS[29] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 100 - 127', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 30: Fb P.Shifter
COMPACT_INS_EFX_PARAMETERS[30] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 100 - 127', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# Other Effects
# 31: 3D Auto
COMPACT_INS_EFX_PARAMETERS[31] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 32: 3D Manual
COMPACT_INS_EFX_PARAMETERS[32] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 33: Lo-Fi 1
COMPACT_INS_EFX_PARAMETERS[33] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 34: Lo-Fi 2
COMPACT_INS_EFX_PARAMETERS[34] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# Effects that connect two types of effect in series (series 2)
# 35: OD -> Chorus
COMPACT_INS_EFX_PARAMETERS[35] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 100 - 27', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 40 - 127', PARAM_0127, [0x25], 40)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 36: OD -> Flanger
COMPACT_INS_EFX_PARAMETERS[36] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 100 - 127', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 40 - 127', PARAM_0127, [0x25], 40)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 37: OD -> Delay
COMPACT_INS_EFX_PARAMETERS[37] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 40 - 127', PARAM_0127, [0x25], 40)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 38: DS -> Chorus
COMPACT_INS_EFX_PARAMETERS[38] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 100 - 127', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 40 - 127', PARAM_0127, [0x25], 40)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 39: DS -> Flanger
COMPACT_INS_EFX_PARAMETERS[39] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 100 - 127', PARAM_0127, [0x16], 100),
    ('Noise suppressor', '0 - 40 - 127', PARAM_0127, [0x25], 40)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 40: DS -> Delay
COMPACT_INS_EFX_PARAMETERS[40] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 40 - 127', PARAM_0127, [0x25], 40)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 41: EH -> Chorus
COMPACT_INS_EFX_PARAMETERS[41] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 42: EH -> Flanger
COMPACT_INS_EFX_PARAMETERS[42] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 43: EH -> Delay
COMPACT_INS_EFX_PARAMETERS[43] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 44: Cho -> Delay
COMPACT_INS_EFX_PARAMETERS[44] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 45: FL -> Delay
COMPACT_INS_EFX_PARAMETERS[45] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 46: Cho -> Flanger
COMPACT_INS_EFX_PARAMETERS[46] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

#  Effects that connect three or more types of effect in series (series 3/series 4/series 5)
# 47: Rotary Multi (same as Full Effect 6)
COMPACT_INS_EFX_PARAMETERS[47] = FULL_EFX_PARAMETERS[6]

# 48: GTR Multi (same as Full Effect 7)
COMPACT_INS_EFX_PARAMETERS[48] = FULL_EFX_PARAMETERS[7]

# 49: GTR Multi 2
COMPACT_INS_EFX_PARAMETERS[49] = FULL_EFX_PARAMETERS[8]

# 50: GTR Multi 3
COMPACT_INS_EFX_PARAMETERS[50] = FULL_EFX_PARAMETERS[9]

# 51: Clean Gt Multi 1
COMPACT_INS_EFX_PARAMETERS[51] = FULL_EFX_PARAMETERS[10]

# 52: Clean Gt Multi 2
COMPACT_INS_EFX_PARAMETERS[52] = FULL_EFX_PARAMETERS[11]

# 53: Bass Multi
COMPACT_INS_EFX_PARAMETERS[53] = FULL_EFX_PARAMETERS[12]

# 54: E.Piano Multi
COMPACT_INS_EFX_PARAMETERS[54] = FULL_EFX_PARAMETERS[13]

# 55: Keyboard Multi
COMPACT_INS_EFX_PARAMETERS[55] = FULL_EFX_PARAMETERS[14]

#  Effects that connect two types of effect in parallel (parallel 2)
# 56: Cho / Delay
COMPACT_INS_EFX_PARAMETERS[56] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)


# 57: FL / Delay
COMPACT_INS_EFX_PARAMETERS[57] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)


# 58: Cho /Flanger
COMPACT_INS_EFX_PARAMETERS[58] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)


# 59: OD1 / OD2
COMPACT_INS_EFX_PARAMETERS[59] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 40 - 127', PARAM_0127, [0x25], 40)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)


# 60: OD / Rotary
COMPACT_INS_EFX_PARAMETERS[60] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 40 - 127', PARAM_0127, [0x25], 40)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)


# 61: OD / Phaser
COMPACT_INS_EFX_PARAMETERS[61] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 40 - 127', PARAM_0127, [0x25], 40)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)


# 62: OD / AutoWah
COMPACT_INS_EFX_PARAMETERS[62] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 40 - 127', PARAM_0127, [0x25], 40)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)


# 63: PH / Rotary
COMPACT_INS_EFX_PARAMETERS[63] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    ('Level', '0 - 127', PARAM_0127, [0x16], 127),
    ('Noise suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
)

# 64: PH /AutoWah
COMPACT_INS_EFX_PARAMETERS[64] = (
    # ('PH Man', 'description', mergedRange, [0xXX], _default_),
    # ('PH Rate', 'description', mergedRange, [0xXX], _default_),
    ('PH Depth', '0 - 70 - 127', PARAM_0127, [0x05], 70),
    ('PH Reso', '0 - *127*', PARAM_0127, [0x06], 127),
    ('PH Mix', '0 - *127*', PARAM_0127, [0x07], 127),
    # ('PH Pan', 'description', mergedRange, [0xXX], _default_),
    ('PH Level', '0 - 90 - 127', PARAM_0127, [0x13], 90),
    # ('AW Filter', 'description', mergedRange, [0xXX], _default_),
    ('AW Sens', '0 - 40 - 127', PARAM_0127, [0x09], 40),
    ('AW Man', '0 - 10 - 127', PARAM_0127, [0x0A], 10),
    ('AW Peak', '0 - 20 - 127', PARAM_0127, [0x0B], 20),
    ('AW Rate', '0.05Hz - 2.00Hz - 10.0Hz', PARAM_TYPE_6, [0x0C], 39),
    ('AW Depth', '0 - 90 - 127', PARAM_0127, [0x0D], 90),
    ('AW Pol', 'Down/*Up*', PARAM_UP_DOWN, [0x0E], 1),
    ('AW Pan', 'L63 - 0 - R63', PARAM_PAN63, [0x14], 0),
    ('AW Level', '0 - *127*', PARAM_0127, [0x15], 0x7f),
    ('Level', '0 - *127*', PARAM_0127, [0x16], 0x7f),
    ('Noise Suppressor', '0 - 10 - 127', PARAM_0127, [0x25], 10)
)

# Generic Compact Insertion Effect:
# If you want to help, fill the fields:

# Name:         the name of the "Parameter" as in the docs (i.e. Pre Dly, Rate or whatever;
# Description:  human readable setting values. The *BOLD* value is the default. In the description, don't care about that;
# mergedRange:  this should be a dictionary of the possible values. If in doubt, leave the live commented and add 'TODO' tag at the end. I'll take care of it sooned or later;
# [0xXX]:       the HEX value of the parameter to be passed via SysEx messages. It's in the docs, so please DO fill it;
# _default_:    the default value. If you can't figure it out, just leave it as is (line commented)

# Uncomment line only if you are sure of what you do.
# if only one parameter is there, please leave the trailing COMMA (,). If more than one parameter is done, the last one CAN (but must not) be without the trailing COMMA.
# if the effect if finished (all parameters filled), the last one has no trailing comma.
#
#COMPACT_INS_EFX_PARAMETERS[XXXX] = (
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_),
    # ('Name', 'description', mergedRange, [0xXX], _default_)
    # ADD ENOUGH LINES OR DELETE THOSE YOU DON'T NEED.
#)

#

# The VT Effect Mode

VT_EFFECT = ('VT Effect', [0x00, 0x01])

VT_EFFECT_PARAMETERS = (
    ('Direct Level', '0 - 127', PARAM_0127, [0x03], 0x00),
)

# End of exclusive (EOX)
EOX = [0xF7]
