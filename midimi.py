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


# syex message per chiedere il livello del volume del master
# o.write_sys_ex(pyportmidi.time(),[0xf0,0x41,0x10,0x00,0x11,0x11,0x00,0x40,0x50,0x03,0x00,0x00,0x00,0x01,0x6c,0xf7])

# i primi 6 valori (0xf0,0x41,0x10,0x00,0x11,0x11) sono "standard" per la richiesta RQ1
# 0x00,0x40,0x50,0x03 e' l'indirizzo del "Master Level"
# 0x00,0x00,0x00,0x01 e' la dimensione

# 0x6c e' il *checksum*
# 0xf7 (247 in decimale) e' la fine dell'exclusive.

# aprendo uno stream in input e leggendolo con i.read(buffer_len) ottengo (in decimale)

# [i = pm.midi.Input(5) --> OKKIO che il device e' diverso!!! il 4 era solo output, questo e' input
# poi print i.read(1)]

# [[[240, 65, 16, 0], 24568015], [[17, 18, 0, 64], 24568015], [[80, 3, 100, 9], 24568015], [[247, 0, 0, 0], 24568015]]

# dove il dato di interesse e' il "18" (0x12) che identifica il Data Set 1 (DT1) e il 100, che sarebbe il livello del volume al momento.

# il "9" (0x9) e' sempre il nostro bel checksum!

# per impostare un livello con un SysEx message, devo usare il DT1 (data set 1), ovvero
# o.write_sys_ex(pyportmidi.time(),[0xf0,0x41,0x10,0x00,0x11,0x12,0x00,0x40,0x50,0x03,0x7f,0x6e,0xf7])

# dove, come sopra, 0x12 e' il comando (DT1), la dimensione non la metto ma metto solo il valore (0x7f, 127 in decimale)
# aggiungo il checksum e infine f7 (247) per finire il messaggio


# *************************************************************
# *****************  CHECKSUM *********************************

# SI SOMMANO I SINGOLI VALORI DI (INDIRIZZO + CANALE) O (INDIRIZZO + DATI), SI DIVIDE PER 128 (DECIMALE), SI PRENDE IL RESTO E SE NE FA IL COMPLEMENTO A 128
# SI CONVERTE IN HEX IL RISULTATO ET VOILA'!

# fosse: aa bb cc dd ee ff gg hh canale+dimensione farei [128 - (aa+bb+cc+dd+ee+ff+gg mod 128)] con tutti i valori in decimale.
# fosse: aa bb cc dd ee ff  canale + dati, idem. 
