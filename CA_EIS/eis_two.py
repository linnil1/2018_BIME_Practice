import os
import re
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

mname = "EIS"

def save_load():
    fname = "save" + mname + ".npz"
    fload = np.load(fname)
    meta = fload['meta'] 
    data = fload['data']
    return meta, data

meta, data = save_load()

# number = 6
plt.title("No counter electrode " + meta[0]['method'])

metas = [m['name'] for m in meta]
name = "protein #9"
i = metas.index(name)
plt.plot(data[i, :, 1], data[i, :, 2], label=name)
i = metas.index('two ' + name)
plt.plot(data[i, :, 1], data[i, :, 2], label=name + " without counter electrode")

plt.xlabel(meta[0]['cols'][1])
plt.ylabel(meta[0]['cols'][2])
plt.gca().invert_yaxis()
plt.legend()
plt.savefig("eis_two.png")
plt.show()
