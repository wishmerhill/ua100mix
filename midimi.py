'''
Not really part of the project. Just a sort of sandbox where i do some tests...

Please, don't waste yout time reading this file

'''

import sys
import os
import pyportmidi as pm


pm.init()

#numDevs = pm.get_count()
#dev = 0
#while dev < numDevs:
#   print 'device ', dev, ': ',pm.get_device_info(dev)
#   dev = dev + 1

numDevs = pm.get_count()

midiDevs = {}

for dev in range(0,numDevs):
   
   deviceInfo = pm.get_device_info(dev)
   
   print 'device ', dev, ': ',deviceInfo,' of type',type(deviceInfo)
   midiDevs[dev] = deviceInfo
#print midiDevs


for k in range(0,len(midiDevs)):
    if (midiDevs[k][1] == 'UA-100 Control') & (midiDevs[k][3] == 1):
      print 'Trovato! Il controller e il device ',k, ', ovvero ',midiDevs[k][1]
      UA100CONTROL = k

#print UA100CONTROL
   
#print "i device dovrebbero essere", numDevs

#for i in midiDevs:
#   print i,': ',midiDevs[i]




#o = pm.midi.Output(4)
#
#o.write_short(0xB2,18,0)
#
#o.close()

pm.quit()


