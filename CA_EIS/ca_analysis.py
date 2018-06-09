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

mname = "CA"
def save_load():
    fname = "save" + mname + ".npz"
    fload = np.load(fname)
    meta = fload['meta'] 
    data = fload['data']
    return meta, data

meta, data = save_load()

# number = 5
plt.title(meta[0]['method'] + " analysis with Cottrell Eqn")
plt.xlabel("1 / sqrt({})".format(meta[0]['cols'][0]))
plt.ylabel(meta[0]['cols'][1])

for i in  range(5):
    n = 0
    plt.plot(1. / np.sqrt(data[i][n:, 0]), data[i][n:, 1], 'o-', label=meta[i]['name'].replace('mm', 'mM'))

plt.legend()
plt.savefig("ca_analysis_1.png")
plt.show()


# number = 5
plt.figure(figsize=(12, 9))
plt.subplots_adjust(left=0.07, right=0.97,top=0.92, bottom=0.05, wspace=0.25)
plt.suptitle(meta[0]['method'] + " analysis with Cottrell Eqn")

allax = plt.subplot(2, 3, 6)
plt.title("all")
plt.xlabel("1 / sqrt({})".format(meta[0]['cols'][0]))
plt.ylabel(meta[0]['cols'][1])

for i in  range(5):
    n = 10
    x = 1. / np.sqrt(data[i][n:, 0])
    y = data[i][n:, 1]
    text, fit_y = analysisOne(x, y)

    plt.subplot(2, 3, i + 1)
    labelname = meta[i]['name'].replace('mm', 'mM')
    plt.title(labelname)
    plt.text(.95, .05, text,
             horizontalalignment='right',
             verticalalignment='bottom',
             transform=plt.gca().transAxes)
    print(text)
    plt.plot(x, y, 'o', label="original data")
    plt.plot(x, fit_y, label="fit line")

    plt.xlabel("1 / sqrt({})".format(meta[0]['cols'][0]))
    plt.ylabel(meta[0]['cols'][1])
    allax.plot(x, y, 'o', label=labelname)
    allax.plot(x, fit_y, label="")
    plt.legend()

allax.legend()
plt.savefig("ca_analysis_2.png")
plt.show()
