import rtmidi, mido, sys, time
mido.set_backend('mido.backends.rtmidi/LINUX_ALSA')

def actualMidiDevices():
    '''
    This should enumerate the devices to (later on) give then the possibility to choose one or guess the right one
    Returns a dictionary with tuples like

    midiDevs = { 0: (tuple), 1: (tuple), ... }

    where the tuple is in the format:

    ('ALSA', 'UA-100 MIDI 2', 0, 1, 0)

    '''

    IODevs = mido.get_input_names()
    numIODevs = len(IODevs)



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
            return int(i)

def print_message(message):
    print(message)


midiDevs = actualMidiDevices()
print(midiDevs)
UA100CONTROL = rightMidiDevice(midiDevs)
device = midiDevs[UA100CONTROL]
print(device)
try:
    #pmout = mido.open_output(device)
    pmin = mido.open_input(device, callback = print_message)
except:
    print('No ports! Bye')
    sys.exit()

while True:
    print('Waiting 5 sec...')
    time.sleep(5)