# Defining costants (taken from UA-100 documentation)

# Control Change Messages (for the Mixer part) - SysEx messages will be implemented later on (maybe)

# Control Change *CHANNELS*
CC_MIC1_CH = 0xb0
CC_MIC2_CH = 0xb1
CC_WAVE1_CH = 0xb2
CC_WAVE2_CH = 0xb3
CC_SYSRET_CH = 0xb4
CC_SYSSUB_CH = 0xb5
CC_WAVEREC_CH = 0xbE
CC_LINE_MASTER_CH = 0xBF

# Control Change *PARAMETERS* 
CC_MICLINESELECTOR_PAR = 21 # 0x15
CC_PAN_PAR = 10 # 0x0A - 0 - 64 - 127 (LEFT - CENTER - RIGHT)
CC_SEND1_PAR = 16 # 0x10
CC_SEND2_PAR = 17 # 0x11
CC_MUTE_PAR = 18 # 0x12
CC_SOLO_PAR = 19 # 0x13
CC_SUB_FADER_PAR = 20 # 0x14
CC_MAIN_FADER_PAR = 7 # 0x70
CC_SELECTOR_PAR = 22 # 0x16
CC_EFFECTSWITHC_PAR = 23 # 0x23

# Control Change Setting range

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

CC_0127_DEFAULT = 64 # I think 'in media stat virtus'

# DEBUG MODE CONTROL
# 1: true
# 0: false

DEBUG_MODE = 1
