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

def rctWCal(x)
    return (rct + 1 / zw * (x * 1j) ** -0.5)
def reqCal(x):
    return rs + (c * (x * 1j) ** n + 
        rctWCal(x, rct, zw) ** -1) ** -1

def loss(a, b):
    return np.abs(a - b) ** 2

rct = 1237.883411
rs = 75.74738519
c = 1.55129E-05
n = 0.81
zw = 0.001741482

lr = 0.0001

# adagrad
ss_rs = 0
ss_c = 0
ss_n = 0
ss_rct = 0
ss_zw = 0

print("Start")
print(np.sum(loss(reqCal(x_feq), y_data)))
for iters in range(100):
    for i, x in enumerate(x_feq[:]):
        req = reqCal(x)
        rctW = rctWCal(x)
        l = y_data[i] - req

        wj = x * 1j
        req = (req - rs) ** -1
        d_rs  = 1
        d_c   = -(req) ** -2 * wj ** n
        d_n   = -(req) ** -2 * wj ** n * c * np.log(wj)
        d_rct = (req * rctW) ** -2
        d_zw  = -(req * rctW * zw) ** -2 * wj ** -0.5

        ss_rs  += np.abs(l * d_rs)  ** 2
        ss_c   += np.abs(l * d_c)   ** 2
        ss_n   += np.abs(l * d_n)   ** 2
        ss_rct += np.abs(l * d_rct) ** 2
        ss_zw  += np.abs(l * d_zw)  ** 2

        rs  += lr * np.abs(d_rs ) / np.sqrt(ss_rs )
        c   += lr * np.abs(d_c  ) / np.sqrt(ss_c  )
        n   += lr * np.abs(d_n  ) / np.sqrt(ss_n  )
        rct += lr * np.abs(d_rct) / np.sqrt(ss_rct)
        zw  += lr * np.abs(d_zw ) / np.sqrt(ss_zw )

        """
        rs  += lr * np.abs(l * d_rs)
        c   += lr * np.abs(l * d_c)
        n   += lr * np.abs(l * d_n)
        rct += lr * np.abs(l * d_rct)
        zw  += lr * np.abs(l * d_zw)
        """

    if iters % 10 == 0:
        print(iters)
        print(rct, rs, c, n, zw)
        print(np.sum(loss(reqCal(x_feq), y_data)))

