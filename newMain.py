#!/usr/bin/python ua100mix/main.py

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

# this is in place of the old DEBUG_MODE (awful!)
import logging

# configuring the logger so that it does not log anything coming from imported modules
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Import phase
logger.info('Importing some required modules')
import sys, functools, numpy as np, signal, time
try:
    import mido
    import rtmidi
except ImportError:
    logger.warning('*** Warning *** mido and/or rtmidi not found. Can\'t go on, Bye.')
    sys.exit()

mido.set_backend('mido.backends.rtmidi/LINUX_ALSA')

# importing GUI modules
import PyQt4.uic
from PyQt4 import QtGui

# brutally importing all the parameters. I read somewhere in this case * is not deprecated.
logger.info('Reading MANY constants...')
from res.parameters import *

# get data in hex format (sometime it is useful, as the whole documentation expresses parameters in hex)
np.set_printoptions(formatter={'int': hex})

# defining some useful general purpose funtion to be called also from inside the classes
def send_RQ1(data, pmout):
    """

    :param data:
    :param pmout:
    :return:
    """
    message = RQ1_STATUS \
              + UA_SYSEX_ID \
              + RQ1_COMMAND \
              + data \
              + checksum(data) \
              + EOX
    logger.debug("Message RQ1: %s", message)

    p = mido.Parser()
    p.feed(message)
    sysEx_msg = p.get_message()
    logger.debug('Message to be sent: %s', sysEx_msg)
    pmout.send(sysEx_msg)


def send_DT1(data, pmout):
    message = DT1_STATUS \
              + UA_SYSEX_ID \
              + DT1_COMMAND \
              + data \
              + checksum(data) \
              + EOX
    logger.debug('DT1 Message: %s', np.array(message))

    p = mido.Parser()
    p.feed(message)
    sysEx_msg = p.get_message()
    logger.debug('Message to be sent: %s', sysEx_msg)
    pmout.send(sysEx_msg)


def checksum(toChecksum):
    '''
    That's how the UA-100 does the checksum:
    Take the data part of SYSEXES and do the maths.
    '''
    checksum_value = (128 - (sum(toChecksum) % 128))
    checksum_list = [checksum_value]
    return list(checksum_list)


# Let the drums roll! ROCK AND ROLL!
if (__name__ == '__main__'):
    logger.info('Let the music start')

    # brutal way to catch the CTRL+C signal if run in the console...
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = None
    if (not app):
        app = QtGui.QApplication([])

    window = MainWindow()
    window.show()

    if (app):
        app.exec_()