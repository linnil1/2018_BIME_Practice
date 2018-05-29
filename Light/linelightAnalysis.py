import numpy as np
import matplotlib.pyplot as plt
from data import *

def calOne(x, y, t):
    logx = np.log(x)
    logy = np.log(y)
    head_a, intval_a, intval_b, head_b, r_square = linearReg(logx, logy)
    fit_y = head_b * logx + head_a
    print(t, ": R square =", r_square)
    exp_x = np.linspace(x.min(), x.max())
    return fit_y, (exp_x ** head_b) * np.exp(head_a)

plt.figure(figsize=(12, 9))
plt.suptitle("指數回歸")
ax1 = plt.subplot(121)
ax2 = plt.subplot(122)

ax1.set_title("log " + dis_name[1] + " vs log 距離 \nwith " + line_text + " and 反光板")
ax1.set_ylabel("log " + dis_name[1])
ax1.set_xlabel("log " + dis_xname)
for j in range(3):
    y = line_data[1, :, j]
    fit_log_y, fit_y = calOne(dis, y, str(line_dis[j]) + "cm")
    ax1.plot(np.log(dis), np.log(y), 'o', label=str(line_dis[j]) + "cm")
    ax1.plot(np.log(dis), fit_log_y, label="fit line " + str(line_dis[j]) + "cm")
    ax2.plot(dis, y, 'o', label=str(line_dis[j]) + "cm")
    ax2.plot(np.linspace(dis.min(), dis.max()), fit_y, label="fit line " + str(line_dis[j]) + "cm")
ax2.set_title(dis_name[1] + " vs 距離 \nwith " + line_text + " and 反光板")
ax2.set_ylabel(dis_name[1])
ax2.set_xlabel(dis_xname)

plt.savefig("linelightAnalysis.png")
plt.show()

"""
def plotOne(x, y, name):
    text, fit_y = analysisOne(x, y)
    print(name)
    print(text)
    plt.plot(x, y, 'o', label=name)
    plt.plot(x, fit_y, label=name + " fit line")
    # plt.legend(loc = 0)

plt.figure(figsize=(8, 6))
plt.title("線性回歸 of " + dis_name[1] + " vs 距離 \nwith " + line_text + " and 反光板")
plt.ylabel(dis_name[1])
plt.xlabel(dis_xname)
for j in range(3):
    plotOne(dis, line_data[1, :, j], str(line_dis[j]) + "cm")
plt.legend()
plt.xticks(dis)
plt.savefig("linelightAnalysis_linear.png")
plt.show()
"""
