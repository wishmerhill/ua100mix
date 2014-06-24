import sys
import os
import pyportmidi as pm


pm.init()

numDevs = pm.get_count()
dev = 0
while dev < numDevs:
   print 'device ', dev, ': ',pm.get_device_info(dev)
   dev = dev + 1

print "i device dovrebbero essere", numDevs

o = pm.midi.Output(4)

o.write_short(0xB2,18,0)

o.close()


