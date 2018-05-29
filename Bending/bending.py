import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

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

# fix weight
length = [31.4,40.4,47.5,57.6,73.1]
data = [1.35007,1.44944,1.52843,1.63034,1.79341]

plotOne(length, data)
plt.title("Bending data for Fixed Weight = 5kg")
plt.xlabel("length(cm)")
plt.ylabel("Voltage (1000 * V)")
plt.savefig("bending1.jpg")
plt.show()

weight = [2,4,6,8,10]
data = [1.31440,1.51823,1.71952,1.91823,2.11444]
plotOne(weight, data)
plt.title("Bending data for Fixed Length = 58cm")
plt.xlabel("Weight (kg)")
plt.ylabel("Voltage (1000 * V)")
plt.savefig("bending2.jpg")
plt.show()
