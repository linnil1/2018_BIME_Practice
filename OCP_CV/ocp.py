import os
import re
import numpy as np
import matplotlib.pyplot as plt

def fileRead():
    files = os.listdir("OCP")
    meta = []
    alldata = []

    for fname in files:
        if not fname.endswith(".txt"):
            continue
        cols = []
        data = []

        fes = dict(re.findall(r"(\d-) (\d+)m", fname))
        print(fes)
        f = open('OCP/' + fname).readlines()
        for fl in f:
            if cols:
                s = fl.split()
                if s:
                    data.append(s)
            if '/' in fl:
                cols = fl.split(',')
                cols = list(map(lambda a: a.strip(), cols))

        meta.append([fes, cols])
        alldata.append(data)

    return meta, alldata

if not os.path.isfile("saveOCP.npz"):
    meta, data = fileRead()
    data = np.array(data, dtype=np.float)
    np.savez("saveOCP.npz", meta=meta, data=data)
else:
    fload = np.load("saveOCP.npz")
    meta = fload['meta'] 
    data = fload['data']

rank = np.argsort(data.mean(axis=1)[:, 1])
data = data[rank]
meta = meta[rank]

# number = 5
plt.figure(figsize=(15, 9))
plt.suptitle("Open Circuit Potential - Time")
plt.subplots_adjust(left=0.07, right=0.97, bottom=0.05, wspace=0.25)
alltext = []
for i in range(5):
    plt.subplot(2, 3, i + 1)
    text = "赤血鹽: " + meta[i][0]['3-'] + "mM, "
    text += "黃血鹽: " + meta[i][0]['4-'] + "mM"

    alltext.append(text)
    plt.title(text)
    plt.xlabel(meta[i][1][0])
    plt.ylabel(meta[i][1][1])
    plt.plot(data[i, ::5, 0], data[i, ::5, 1])
    
    last = data[i, (-len(data[i, :, 0]) // 10):, 1]
    print(last.mean())
    if last.max() - last.min() < 0.0001:
        plt.plot(data[i, ::5, 0], np.repeat(last.mean(), len(data[i, ::5, 0])))
        plt.text(0, last.mean(), np.round(last.mean(), 4))

plt.subplot(2, 3, 6)
plt.title("Five OCP data in one plot")
plt.plot(data[:, :, 0].T, data[:, :, 1].T)
for i in range(5):
    plt.text(0, data[i, :, 1].mean(), np.round(data[i, :, 1].mean(), 4))
plt.xlabel(meta[0][1][0])
plt.ylabel(meta[0][1][1])
plt.legend(alltext, bbox_to_anchor=(0.95, 0.8))

plt.savefig('ocp.png')
plt.show()

