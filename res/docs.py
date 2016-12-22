#!/usr/bin/python ua100mix/res/docs.py


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
