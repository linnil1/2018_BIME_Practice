import numpy as np
import matplotlib.pyplot as plt

def tempDist(x, L, m, h_mk):
    y = (np.cosh(m * (L - x)) + h_mk * np.sinh(m * (L - x))) / \
        (np.cosh(m *  L     ) + h_mk * np.sinh(m *  L    ) )
    return y

# real data
# time temperture
tt = """
34.6 29.5   25   25
50.0 37.1 29.8 27.6
70.1 48.5 35.6 31.6
90.2 69.5 54.2 44.8
"""
rods = np.array(tt.split(), dtype=np.float).reshape(-1, 4)
b_temp = [34, 50, 70, 90]
rod_d = [45, 150, 260, 355]
plt.plot(rod_d, rods.T, 'o-')
plt.xticks(rod_d, [str(b) + "mm" for b in rod_d])
plt.xlabel('Distance from bottom')
plt.ylabel('Temperture(℃ )')

def loss(L, m, h_mk):
    y = tempDist((np.array(rod_d) - np.min(rod_d)) / 1000, L, m, h_mk)
    y = y * (np.array(b_temp)[:, np.newaxis] - 25) + 25
    # compare without 90℃ 
    return np.sum((y[0:3] - rods[0:3]) ** 2)

# find min solu
L = 350 * 0.001
m = np.logspace(-2,2)
h_mk = np.logspace(-3,3)
min_loss = np.inf
min_var = []
for i in m:
    for j in h_mk:
        q = loss(L, i, j)
        if q < min_loss:
            min_loss = q
            min_var = [i,j]

# simulated solu
print(min_var)
# [4.941713361323833, 0.3727593720314938]
m = min_var[0]
h_mk = min_var[1]
x = np.linspace(0, L)
y = tempDist(x, L, m, h_mk)
y = y * (np.array(b_temp)[:, np.newaxis] - 25) + 25
plt.plot(x * 1000 + 45, y.T)
plt.legend([str(d) + "℃ " for d in b_temp] + ["Simulated " + str(d) + "℃ " for d in b_temp])

plt.show()
