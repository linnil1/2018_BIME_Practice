import numpy as np
import matplotlib.pyplot as plt
from data import *

plt.figure(figsize=(8, 6))
plt.title(dis_name[1] + " vs 距離 \nwith " + line_text + " and 反光板")
plt.ylabel(dis_name[1])
plt.xlabel(dis_xname)
for i in range(2):
    for j in range(3):
        plt.plot(dis, line_data[i, :, j], label=reflect_text[i] + str(line_dis[j]) + "cm")
plt.legend()
plt.xticks(dis)
plt.savefig("linelight.png")
plt.show()
