import numpy as np
import matplotlib.pyplot as plt
from data import *
data = dis_data
names = dis_name

plt.figure(figsize=(12, 9))

want = [0, 1, 3, 4]
for i in range(4):
    plt.subplot(221 + i)
    plt.title(names[want[i]] + " vs 距離")
    plt.ylabel(names[want[i]])
    plt.xlabel(dis_name)
    plt.plot(dis, data[:, want[i], :])
    plt.xticks(dis)
    plt.legend(light_type)
# plt.savefig("distance.png")
plt.show()
