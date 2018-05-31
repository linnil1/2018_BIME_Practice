import os
import re
import numpy as np
import matplotlib.pyplot as plt

def stripArray(arr):
    return list(map(lambda a: a.strip(), arr))

def fileRead():
    files = os.listdir("CV")
    allmeta = []
    alldata = []

    for fname in files:
        # read
        if not fname.endswith(".txt"):
            continue
        name = re.findall(r"cv (.*)\.", fname)[0]
        f = open('CV/' + fname).readlines()

        cols = []
        data = [[]]
        meta = [[]]
        seg = 0

        # parse
        for fl in f:
            # seg
            if re.match('Segment \d+:', fl):
                seg = int(re.findall(r"\d+", fl)[0])
                continue
            # data
            if cols:
                s = fl.split()
                if s:
                    data[seg - 1].append(s)
                continue
            # meta
            elif '=' in fl:
                meta[seg].append(stripArray(fl.split('=')))
                # get number of segments
                if seg == 0 and meta[seg][-1][0] == 'Segment':
                    meta.append([])
                    for i in range(1, int(meta[seg][-1][1])):
                        meta.append([])
                        data.append([])
                continue
            # column of data
            if ',' in fl and '/' in fl:
                cols = stripArray(fl.split(','))
                meta[0].append(['cols', cols])
                continue

        # add meta, conver to dict, convert data to nparray
        meta[0].append(['len', np.cumsum([len(i) for i in data])])
        meta[0].append(['name', name])
        for i in range(len(meta)):
            meta[i] = dict(meta[i])
        data = np.vstack(data)
        data = np.array(data, dtype=np.float)

        # OK
        # from pprint import pprint
        # pprint(meta)
        allmeta.append(meta)
        alldata.append(data)
    return allmeta, alldata

# save to file
if not os.path.isfile("saveCV.npz"):
    meta, data = fileRead()
    data = np.array(data, dtype=np.float)
    np.savez("saveCV.npz", meta=meta, data=data)
else:
    fload = np.load("saveCV.npz")
    meta = fload['meta'] 
    data = fload['data']

rank = np.argsort([int(re.findall(r"\d+", m[0]['name'])[0]) \
    if 'shake' not in m[0]['name'] else np.inf for m in meta])
meta = meta[rank]
data = data[rank]

# number = 6
plt.figure(figsize=(15, 9))
plt.suptitle("Cyclic Voltammetry")
plt.subplots_adjust(left=0.07, right=0.97,top=0.92, bottom=0.05, wspace=0.25)
alltext = []
for i in range(6):
    plt.subplot(2, 3, i + 1)
    plt.title(meta[i][0]['name'].replace("mvs", "mV/s"))
    plt.xlabel(meta[i][0]['cols'][0])
    plt.ylabel(meta[i][0]['cols'][1])
    plt.plot(data[i, :, 0], data[i, :,1])
    plt.gca().invert_xaxis()

plt.savefig('cv_ori.png')
plt.show()
