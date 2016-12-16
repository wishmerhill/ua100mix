
DEBUG_MODE = 0

def ulist(start,stop,step,unit=""):
    r=start
    lista=[]
    while (r <= stop):
        lista.append(str(r) + unit)
        r += step
    return lista

def rlist(start, stop, step, unit="", factor=1, reverse = False):
    r = start
    lista = []
    if (start < stop) and (step > 0):
        while (r <= stop):
            for i in range(factor):
                #lista.append(unit + str(r))
                lista.append('{}'.format((str(r) + unit) if not reverse else (unit + str(r))))
            r += step
    elif (start > stop) and (step < 0):
        print('inverso...')
        while (r >= stop):
            for i in range(factor):
                lista.append('{}'.format((str(r) + unit) if not reverse else (unit + str(r))))
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