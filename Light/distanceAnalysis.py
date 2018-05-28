import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

plt.figure(figsize=(12, 9))

"""
A B C F G
目測燈管顏色	白	橘	藍	白	紅
電流值(A)	0.51	0.78	0.59	0.58	0.72

20 30 37.5
"""

data_ori = """
520	241	101	352	98
9.086	3.3572	6.9353	7.9326	2.7841
7.5746	3.0126	5.0793	6.4479	2.7191
0.42	2.15	0.01	0.26	171.29
7.26	7.01	1.03	6.09	49.52

337	160	66	235	57
5.8825	2.2275	4.6356	5.2699	1.6263
4.9021	1.9993	3.3935	4.2841	1.5862
0.42	2.14	0.01	0.26	127.33
7.34	7.01	1.32	5.68	44.87

262	112	49	156	51
4.5842	1.5580	3.4428	3.5249	1.4643
3.8227	1.3977	2.5203	2.8648	1.4258
0.42	2.12	0.01	0.26	89.87
7.27	7.02	0.95	6.21	35.4"""

data = np.array(data_ori.split(), dtype=np.float).reshape(3, 5, 5)
dis = np.array([20, 30, 37.5])

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
    plt.text(.95, .05, text,
             horizontalalignment='right',
             verticalalignment='bottom',
             transform=plt.gca().transAxes)
    plt.plot(x, y, 'o', label="original data")
    plt.plot(x, fit_y, label="fit line")
    plt.legend(loc = 0)

names = ["log 照度（Lux）", "log 光量子密度 PPFD(umol/m^2s)"]
for i, name in enumerate(names):
    plt.subplot(211 + i)
    plt.title(name + " vs -2 log 距離")
    plt.ylabel(name)
    plt.xlabel("-2 * log 燈源與光譜儀距離 (cm)")

    d = np.log(data[1:, i, :] / data[0, i, :] / (20 ** 2))
    plotOne(np.tile(-2 * np.log(dis[1:])[:, np.newaxis], 5).flatten(), d.flatten())
    plt.legend(["points", "Fit Line"])
    # plt.plot(-2 * np.log(dis[1:]), d)
    # plt.legend(["A", "B", "C" ,"D" ,"E"])

plt.savefig("distanceAnalysis.png")
plt.show()
