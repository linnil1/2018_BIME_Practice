import os
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

def analysisOne(x, y):
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
    fit_y = head_b * x + head_a
    return text, fit_y

# save to file
if not os.path.isfile("saveCV.npz"):
    print("run cv.py first")
    exit()
else:
    fload = np.load("saveCV.npz")
    meta = fload['meta']
    data = fload['data']

# sort it
rank = np.argsort([int(re.findall(r"\d+", m[0]['name'])[0]) \
    if 'shake' not in m[0]['name'] else np.inf for m in meta])
meta = meta[rank]
data = data[rank]

def goPlot(E, x):
    plt.figure(figsize=(8, 6))
    plt.suptitle("$I_p$ vs sqrt( Scan Rate (V/s) ) with linear regression")
    for i in range(2):
        plt.subplot(2, 1, i + 1)
        y = E[:, 2 * i + 1]
        text, fit_y = analysisOne(x, y)
        plt.text(.95, .55, text,
                 horizontalalignment='right',
                 verticalalignment='center',
                 transform=plt.gca().transAxes)
        plt.plot(x, y, 'o', label="original data")
        plt.plot(x, fit_y, label="fit line")
        plt.xlabel("sqrt Scan Rate (V/s)")
        plt.ylabel("$I_p$ (A)")
        plt.legend(loc = 0)

# get min max from data
v = []
E = []
# number = 6k
for i in range(5):
    data_len = meta[i][0]['len']
    x = data[i, data_len[-3]:data_len[-1], 0]
    y = data[i, data_len[-3]:data_len[-1], 1]
    argmin = np.argmin(y)
    argmax = np.argmax(y)
    E.append([x[argmin], y[argmin], x[argmax], y[argmax]])
    v.append(float(meta[i][0]['Scan Rate (V/s)']))
E = np.array(E)
x = np.sqrt(v)

# find E0
e = E[:, [0,2]].T
print(np.vstack([[float(m[0]['Scan Rate (V/s)']) for m in meta[:-1]],
    e, np.mean(e, axis=0)]))
print(e.mean())

goPlot(E,x)
plt.savefig('cv_reg_my.png')
plt.show()

# data from txt
E = []
for i in range(5):
    m = meta[i]
    E.append([float(m[-2]['Ep'][:-1]), float(m[-2]['ip'][:-1]),
              float(m[-1]['Ep'][:-1]), float(m[-1]['ip'][:-1])])
E = np.array(E)

goPlot(E,x)
plt.savefig('cv_reg.png')
plt.show()
