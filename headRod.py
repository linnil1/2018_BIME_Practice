import numpy as np
import matplotlib.pyplot as plt

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

plt.suptitle("Temperture measured on rod")
plt.subplot(121)
plt.plot(b_temp, rods, 'o-')
plt.xticks(b_temp, [str(b) for b in b_temp])
plt.xlabel('Bottom temperture')
plt.ylabel('Temperture(℃ )')
plt.legend([str(d) + "mm" for d in rod_d])

plt.subplot(122)
plt.plot(rods.T, 'o-')
plt.legend([str(d) + "℃ " for d in b_temp])
plt.xticks(range(len(rod_d)), [str(b) + "mm" for b in rod_d])
plt.xlabel('Distance from bottom')
plt.ylabel('Temperture(℃ )')

plt.show()