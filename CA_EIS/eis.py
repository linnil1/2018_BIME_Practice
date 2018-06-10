import os
import re
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

mname = "EIS"

def stripArray(arr):
    return list(map(lambda a: a.strip(), arr))

# almost same as CA
def fileRead():
    files = os.listdir(mname)
    allmeta = []
    alldata = []

    for fname in files:
        # read
        if not fname.endswith(".txt"):
            continue
        name = re.findall(r"eis (.*)\.", fname)[0]
        f = open(mname + '/' + fname).readlines()

        cols = []
        data = [[]]
        meta = [[]]
        seg = 0

        # parse
        meta[0].append(["time", f[0]])
        meta[0].append(["method", f[1]])
        meta[0].append(['name', name])
        for fl in f[2:]:
            # seg
            if re.match('Step \d+:', fl):
                seg = int(re.findall(r"\d+", fl)[0])
                continue
            # data
            if cols:
                s = fl.split()
                if s:
                    data[seg - 1].append(s)
                continue
            # meta
            elif '=' in fl or ':' in fl:
                if '=' in fl:
                    fp = stripArray(fl.split('='))
                else:
                    fp = stripArray(fl.split(':'))
                # remove blank meta
                if len(fp) == 1:
                    print("?", fl)
                    continue
                meta[seg].append(fp)

                # count segments number of data
                if seg == 0 and meta[seg][-1][0] == 'Step':
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
        for i in range(len(meta)):
            meta[i] = dict(meta[i])
        data = np.vstack(data)
        data = np.array(data, dtype=np.float)

        # OK
        # from pprint import pprint
        # pprint(meta)
        allmeta.append(meta)
        alldata.append(data)

    alldata = np.array(alldata, dtype=np.float)
    allmeta = np.array(allmeta)
    return allmeta, alldata

def save_load():
    # save to file
    fname = "save" + mname + ".npz"
    if not os.path.isfile(fname):
        meta, data = fileRead()
        # rank it
        rank = np.argsort(np.max(data[:, :, 1], axis=1))
        data = data[rank]
        meta = meta[rank]
        meta = [m[0] for m in meta] # this data is only step = 1
        np.savez(fname, meta=meta, data=data)
    # load
    else:
        fload = np.load(fname)
        meta = fload['meta'] 
        data = fload['data']
    return meta, data

meta, data = save_load()

# number = 6
plt.figure(figsize=(16, 8))
plt.title("Nyquist Plot of " + meta[0]['method'])
plt.subplots_adjust(left=0.07, right=0.97,top=0.92, bottom=0.05, wspace=0.25)
for i in range(6):
    if 'two' in meta[i]['name']:
        continue
    plt.plot(data[i, :, 1], data[i, :, 2], label=meta[i]['name'])

plt.xlabel(meta[0]['cols'][1])
plt.ylabel(meta[0]['cols'][2])
plt.gca().invert_yaxis()
plt.legend()
plt.savefig("eis.png")

# number = 6
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')
plt.title("3D plot of " + meta[0]['method'])
plt.subplots_adjust(left=0.07, right=0.97,top=0.92, bottom=0.05, wspace=0.25)
for i in range(6):
    if 'two' in meta[i]['name']:
        continue
    ax.plot(data[i, :, 1], data[i, :, 2], np.log(data[i, :, 0]), label=meta[i]['name'])

plt.xlabel(meta[0]['cols'][1])
plt.ylabel(meta[0]['cols'][2])
ax.set_zlabel("log ({})".format(meta[0]['cols'][0]))
plt.gca().invert_yaxis()
plt.legend()
# plt.savefig("eis_3d.png")

# number = 6
plt.figure(figsize=(16, 8))
plt.subplots_adjust(left=0.07, right=0.97,top=0.92, bottom=0.07, wspace=0.25)
plt.suptitle("Bode Plot of " + meta[0]['method'])

plt.subplot(1, 2, 1)
plt.title("log(Amplitude) vs log(Frequency)")
for i in range(6):
    if 'two' in meta[i]['name']:
        continue
    plt.plot(np.log(data[i, :, 0]), np.log(data[i, :, 3]), label=meta[i]['name'])
plt.xlabel("log ({})".format(meta[0]['cols'][0]))
plt.ylabel("log ({})".format(meta[0]['cols'][3]))
plt.legend()

plt.subplot(1, 2, 2)
plt.title("Phase vs log(Frequency)")
for i in range(6):
    if 'two' in meta[i]['name']:
        continue
    plt.plot(np.log(data[i, :, 0]), data[i, :, 4], label=meta[i]['name'])

plt.xlabel("log ({})".format(meta[0]['cols'][0]))
plt.ylabel("log ({})".format(meta[0]['cols'][4]))
plt.gca().invert_yaxis()
plt.legend()

plt.savefig("eis_bode.png")
plt.show()
