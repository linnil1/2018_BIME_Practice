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

if not os.path.isfile("saveOCP.npz"):
    print("run ocp.py first")
    exit()
else:
    fload = np.load("saveOCP.npz")
    meta = fload['meta'] 
    data = fload['data']

rank = np.argsort(data.mean(axis=1)[:, 1])
data = data[rank]
meta = meta[rank]

# number = 5
plt.title("OCP linear Regression")
# plt.subplots_adjust(left=0.07, right=0.97, bottom=0.05, wspace=0.25)

x = []
y = []
for i in range(1, 4):
    x.append(float(meta[i][0]['3-']) / float(meta[i][0]['4-']))
    y.append(data[i, (-len(data[i, :, 0]) // 10):, 1].mean())
x = np.log10(x)
text, fit_y = analysisOne(x, y)
plt.text(.95, .05, text,
         horizontalalignment='right',
         verticalalignment='bottom',
         transform=plt.gca().transAxes)
plt.plot(x, y, 'o', label="original data")
plt.plot(x, fit_y, label="fit line")
plt.legend(loc = 0)
plt.xlabel("log([O] / [R])")
plt.ylabel(meta[i][1][1])

plt.savefig('ocp_reg.png')
plt.show()

