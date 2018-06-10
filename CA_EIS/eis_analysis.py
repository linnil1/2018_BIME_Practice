import os
import re
import numpy as np
import matplotlib.pyplot as plt

mname = "EIS"

def save_load():
    # save to file
    fname = "save" + mname + ".npz"
    fload = np.load(fname)
    meta = fload['meta'] 
    data = fload['data']
    return meta, data

meta, data = save_load()

# simulate
def rctWCal(x, rct, zw):
    return (rct + 1 / zw * (x * 1j) ** -0.5)

def reqCal(x, rct, rs, c, n, zw):
    return rs + (c * (x * 1j) ** n + 
        rctWCal(x, rct, zw) ** -1) ** -1

# result data of simulating
name = ["bare #8", "bare #9", "blocking #8", "protein #8", "protein #9"]

# Rct Rs C n Zw
output_data = np.array("""
100 79.71351001 6.89801E-05 0.70 0.001741482
172.0571172 77.61104159 4.83004E-05 0.74 0.001783709
2230.476042 77.35437973 3.98676E-06 0.886145405 0.001437737
3093.776541 75.96432602 2.86568E-06 0.901051669 0.001319128
1237.883411 75.74738519 1.55129E-05 0.816963877 0.001741482""".split(),
                       dtype=np.float).reshape(5, 5)

# plot it
plt.figure(figsize=(12, 9))
plt.subplots_adjust(left=0.07, right=0.97,top=0.92, bottom=0.07, wspace=0.25)
plt.suptitle("Fitting of " + meta[0]['method'])

# number = 6
for i in range(6):
    if 'two' in meta[i]['name']:
        continue
    rearange = [1, 4, 6, 555, 2, 3]
    plt.subplot(2, 3, rearange[i])

    res = output_data[name.index(meta[i]['name'])]
    plt.plot(data[i, :, 1], data[i, :, 2], 'o', label="original data")
    y = reqCal(data[i, :, 0], *res)
    plt.plot(np.real(y), np.imag(y), label="fit data")
    plt.gca().invert_yaxis()

    plt.title(meta[i]['name'])
    plt.legend()
    plt.xlabel(meta[i]['cols'][1])
    plt.ylabel(meta[i]['cols'][2])
    text = 'Rct = {:.3}\nRs = {:.3}\nC = {:.3}\nn = {:.3}\nZw = {:.3} '''.format(*res)
    plt.text(.95, .05, text,
             horizontalalignment='right',
             verticalalignment='bottom',
             transform=plt.gca().transAxes)

plt.savefig("eis_analysis.png")
plt.show()

