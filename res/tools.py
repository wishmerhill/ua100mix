
DEBUG_MODE = 0

def ulist(start,stop,step,unit=""):
    r=start
    lista=[]
    while (r <= stop):
        lista.append(str(r) + unit)
        r += step
    return lista

def mergeRanges(keyRange,valuesRange):
    if not (len(keyRange) == len(valuesRange)):
        if (DEBUG_MODE):
            print('Huston, we a have a *RANGE* problem:')
        mergedDict={0:'errore nel congiungere le liste'}
    else:
        mergedDict={}
        i=0
        for key in keyRange:
            mergedDict[key]=valuesRange[i]
            i += 1
        if (DEBUG_MODE):
            print(mergedDict)
    return mergedDict