#
#
#
# The whole setup for the mainMixerWindow should be here.

def setupMixer(ui,window):
    '''
    I thought it'd be better to setup the connections here, as qt4designer is not so nice with custom slots.
    Moreover, setting up the connection in qt4designer means that every single new connection must be done outside
    of here.
    '''
    
    # *************** MIC1 *********************

    # Setting Up the Mic1 Fader
    ui.Mic1.valueChanged.connect(ui.Mic1Lcd.display)
    ui.Mic1.valueChanged.connect(functools.partial(window.valueChange, CC_MIC1_CH, CC_MAIN_FADER_PAR))
    #ui.Mic1.setProperty("value", CC_0127_DEFAULT)
    ui.Mic1.setProperty("channel", CC_MIC1_CH)
    ui.Mic1.setProperty("parameter", CC_MAIN_FADER_PAR)
    
    # Setting Up the Mic1 Pan Dial
    ui.Mic1Pan.valueChanged.connect(ui.Mic1PanLcd.display)
    ui.Mic1Pan.valueChanged.connect(functools.partial(window.valueChange, CC_MIC1_CH, CC_PAN_PAR))
    #ui.Mic1Pan.setProperty("value", CC_0127_DEFAULT)
    ui.Mic1Pan.setProperty("channel", CC_MIC1_CH)
    ui.Mic1Pan.setProperty("parameter", CC_PAN_PAR)
    
    # *************** MIC2 *********************
    
    # Setting Up the Mic2 Fader
    ui.Mic2.valueChanged.connect(ui.Mic2Lcd.display)
    ui.Mic2.valueChanged.connect(functools.partial(window.valueChange, CC_MIC2_CH, CC_MAIN_FADER_PAR))
    #ui.Mic2.setProperty("value", CC_0127_DEFAULT)
    ui.Mic2.setProperty("channel", CC_MIC2_CH)
    ui.Mic2.setProperty("parameter", CC_MAIN_FADER_PAR)
    
    # Setting Up the Mic2 Pan Dial
    ui.Mic2Pan.valueChanged.connect(ui.Mic2PanLcd.display)
    ui.Mic2Pan.valueChanged.connect(functools.partial(window.valueChange, CC_MIC2_CH, CC_PAN_PAR))
    #ui.Mic2Pan.setProperty("value", CC_0127_DEFAULT)
    ui.Mic2Pan.setProperty("channel", CC_MIC2_CH)
    ui.Mic2Pan.setProperty("parameter", CC_PAN_PAR)
    
    # *************** WAVE1 *********************
    
    # Setting up the Wave1 Fader
    ui.Wave1.valueChanged.connect(ui.Wave1Lcd.display)
    ui.Wave1.valueChanged.connect(functools.partial(window.valueChange, CC_WAVE1_CH, CC_MAIN_FADER_PAR))
    #ui.Wave1.setProperty("value", CC_0127_DEFAULT)
    ui.Wave1.setProperty("channel", CC_WAVE1_CH)
    ui.Wave1.setProperty("parameter", CC_MAIN_FADER_PAR)
    
    # *************** WAVE2 *********************
    
    # Setting up the Wave1 Fader
    ui.Wave2.valueChanged.connect(ui.Wave2Lcd.display)
    ui.Wave2.valueChanged.connect(functools.partial(window.valueChange, CC_WAVE2_CH, CC_MAIN_FADER_PAR))
    #ui.Wave2.setProperty("value", CC_0127_DEFAULT)
    ui.Wave2.setProperty("channel", CC_WAVE2_CH)
    ui.Wave2.setProperty("parameter", CC_MAIN_FADER_PAR)    
    
    # *************** MASTERLINE *********************
    
    # Setting Up the MasterLine Fader
    ui.MasterLine.valueChanged.connect(ui.MasterLineLcd.display)
    ui.MasterLine.valueChanged.connect(functools.partial(window.valueChange, CC_LINE_MASTER_CH, CC_MAIN_FADER_PAR))
    #ui.MasterLine.setProperty("value", CC_0127_DEFAULT)
    ui.MasterLine.setProperty("channel", CC_LINE_MASTER_CH)
    ui.MasterLine.setProperty("parameter", CC_MAIN_FADER_PAR)
