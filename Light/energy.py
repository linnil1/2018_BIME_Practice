import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

plt.figure(figsize=(12, 9))

"""
A B C D E
目測燈管顏色	白	橘	藍	白	紅
20cm
"""

data_ori = """
520	241	101	352	98
9.086	3.3572	6.9353	7.9326	2.7841
7.5746	3.0126	5.0793	6.4479	2.7191
0.42	2.15	0.01	0.26	171.29
7.26	7.01	1.03	6.09	49.52
"""

# this function copy from bending.py
def plotOne(x, y):
    x = np.array(x)
    y = np.array(y)
    # https://en.wikipedia.org/wiki/Simple_linear_regression
    # bx + a
    head_b = np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2)
    head_a = y.mean() - head_b * x.mean()
    fit_y = head_b * x + head_a
    r_square = np.sum((fit_y - y.mean()) ** 2) / np.sum((y - y.mean()) ** 2)

    # confidence of slope and intercept
    n = len(x)
    var_b = np.sum((y - fit_y) ** 2) / (n + 2) / np.sum((x - x.mean()) ** 2)
    intval_b = np.sqrt(var_b) * t.ppf(0.995, n - 2)
    var_a = var_b * np.sum(x ** 2) / n
    intval_a = np.sqrt(var_a) * t.ppf(0.995, n - 2)

    # plot
    text = '''\
In 99% confidence
slope = {:.3}±{:.3}
intercept = {:.3}±{:.3}
r_squre = {:.3}
'''.format(head_b, intval_b, head_a, intval_a, r_square)
    plt.text(.95, .95, text,
             horizontalalignment='right',
             verticalalignment='top',
             transform=plt.gca().transAxes)
    # plt.plot(x, y, 'o', label="original data")
    plt.plot(x, fit_y, label="fit line")
    # plt.legend(loc = 0)

data = np.array(data_ori.split(), dtype=np.float).reshape(5, 5)
amp = np.array("0.51	0.78	0.59	0.58	0.72".split(), dtype=np.float)
amptext = "電流值(A)"

names = ["照度（Lux）", "光量子密度 PPFD(umol/m^2s)", "有效光量電子密度 YPFD(umol/m^2s)", "R/B", "R/FR"]


for i in range(2):
    plt.subplot(211 + i)
    plt.title(names[i] + " vs " + amptext)
    plt.ylabel(names[i])
    plt.xlabel(amptext)
    plt.plot(amp, data[i, :], 'o')
    plotOne(amp, data[i, :])
    for j, tex in enumerate(["A", "B", "C" ,"D" ,"E"]):
        plt.annotate(tex, (amp[j], data[i, j]))
plt.savefig("energy.png")
plt.show()
