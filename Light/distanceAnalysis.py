import numpy as np
import matplotlib.pyplot as plt
from data import *
data = dis_data
names = dis_name

plt.figure(figsize=(12, 9))

def calOne(x, y, t):
    head_a, intval_a, intval_b, head_b, r_square = linearReg(x, y)
    fit_y = head_b * x + head_a
    print(t, ": R square =", r_square)
    exp_x = np.linspace(np.exp(-x).min(), np.exp(-x).max())
    return fit_y, (exp_x ** -head_b) * np.exp(head_a)

# log regression
for i in range(2):
    d = data[:, i, :]
    x = dis

    fit_ys = []
    fit_exp_ys = []
    for j in range(len(light_type)):
        y = calOne(-np.log(x), np.log(d)[:, j], light_type[j])
        fit_ys.append(y[0])
        fit_exp_ys.append(y[1])
    fit_ys = np.vstack(fit_ys).T
    fit_exp_ys = np.vstack(fit_exp_ys).T

    plt.subplot(221 + 2 * i)
    plt.title("log " + dis_name[0] + " vs - log 距離")
    plt.ylabel("log " + dis_name[0])
    plt.xlabel("- log " + dis_xname)
    plt.plot(-np.log(x), np.log(d), 'o')
    plt.plot(-np.log(x), fit_ys)
    plt.legend([*light_type, *[t + " fit line" for t in light_type]], loc=1)

    plt.subplot(221 + 2 * i + 1)
    plt.title(dis_name[1] + " vs 距離")
    plt.ylabel(dis_name[1])
    plt.xlabel(dis_xname)
    plt.plot(x, d, 'o')
    plt.plot(np.linspace(x.min(), x.max()), fit_exp_ys)
    plt.legend([*light_type, *[t + " fit line" for t in light_type]], loc=1)

# plt.savefig("distanceAnalysis.png")
plt.show()


plt.figure(figsize=(12, 9))
def plotOne(x, y, name):
    text, fit_y = analysisOne(x, y)
    print(name)
    print(text)
    plt.plot(x, y, 'o', label=name)
    plt.plot(x, fit_y, label=name + " fit line")
    # plt.legend(loc = 0)

# linear reg
for i in range(2):
    d = data[:, i, :]
    plt.subplot(211 + i)
    plt.title(dis_name[i] + " vs 距離")
    plt.ylabel(dis_name[i])
    plt.xlabel(dis_xname)
    # plt.plot(dis, data[:, i, :])
    plt.xticks(dis)
    for j in range(len(light_type)):
        plotOne(dis, data[:, i, j], light_type[j])
    plt.legend(loc=1)

plt.savefig("distanceAnalysis_linear.png")
plt.show()
