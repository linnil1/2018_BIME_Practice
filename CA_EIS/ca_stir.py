import os
import re
import numpy as np
import matplotlib.pyplot as plt

mname = "CA"
def save_load():
    fname = "save" + mname + ".npz"
    fload = np.load(fname)
    meta = fload['meta'] 
    data = fload['data']
    return meta, data

meta, data = save_load()

# number = 5
plt.title(meta[0]['method'])
plt.plot(data[4, :, 0], data[4, :, 1], label=meta[4]['name'].replace('mm', 'mM'))
plt.plot(data[4, :, 0], data[5, :, 1], label=meta[5]['name'].replace('mm', 'mM'))

plt.xlabel(meta[0]['cols'][0])
plt.ylabel(meta[0]['cols'][1])
plt.legend()
plt.savefig("ca_stir.png")
plt.show()
