import os
import re
import numpy as np
import matplotlib.pyplot as plt

# save to file
if not os.path.isfile("saveCV.npz"):
    print("run cv.py first")
    exit()
else:
    fload = np.load("saveCV.npz")
    meta = fload['meta'] 
    data = fload['data']

rank = np.argsort([int(re.findall(r"\d+", m[0]['name'])[0]) \
    if 'shake' not in m[0]['name'] else np.inf for m in meta])
meta = meta[rank]
data = data[rank]

# number = 6
# plt.figure(figsize=(12, 9))
# plt.subplots_adjust(left=0.07, right=0.97,top=0.92, bottom=0.05, wspace=0.25)
plt.subplots_adjust(left=0.2)
plt.title("Cyclic Voltammetry")
plt.xlabel(meta[0][0]['cols'][0])
plt.ylabel(meta[0][0]['cols'][1])
plt.gca().invert_xaxis()

for i in range(5):
    plt.plot(data[i, meta[i][0]['len'][-3]:meta[i][0]['len'][-1], 0].T,
             data[i, meta[i][0]['len'][-3]:meta[i][0]['len'][-1], 1].T,
             label=meta[i][0]['name'].replace("mvs", "mV/s"))
plt.legend()
plt.savefig('cv_overlap.png')
plt.show()

plt.title("Cyclic Voltammetry with shaking")
plt.subplots_adjust(left=0.2)
plt.xlabel(meta[0][0]['cols'][0])
plt.ylabel(meta[0][0]['cols'][1])
plt.gca().invert_xaxis()
for i in [2, 5]:
    # sliding window
    y = data[i, meta[i][0]['len'][-3]:meta[i][0]['len'][-1], 1]
    w = 20
    y = np.hstack([np.tile(y[0], w), y, np.tile(y[-1], w)])
    y = np.average(np.vstack([np.roll(y, j) for j in range(-w, w+1)]), axis=0)
    y = y[w:-w]
    # plot
    plt.plot(data[i, meta[0][0]['len'][-3]:meta[0][0]['len'][-1], 0].T,
             y.T,
             label=meta[i][0]['name'].replace("mvs", "mV/s"))
plt.legend()
plt.savefig('cv_overlap_shake.png')
plt.show()
