import numpy as np
import matplotlib.pyplot as plt
from data import *

plt.figure(figsize=(12, 9))

data = dis_data[0]
names = dis_name

def plotOne(x, y):
    text, fit_y = analysisOne(x, y)
    plt.text(.95, .95, text,
             horizontalalignment='right',
             verticalalignment='top',
             transform=plt.gca().transAxes)
    # plt.plot(x, y, 'o', label="original data")
    plt.plot(x, fit_y, label="fit line")
    # plt.legend(loc = 0)

for i in range(2):
    plt.subplot(211 + i)
    plt.title(names[i] + " vs " + amptext)
    plt.ylabel(names[i])
    plt.xlabel(amptext)
    plt.plot(amp, data[i, :], 'o')
    plotOne(amp, data[i, :])
    for j, tex in enumerate(light_type):
        plt.annotate(tex, (amp[j], data[i, j]))
plt.savefig("energy.png")
plt.show()
