import numpy as np
import matplotlib.pyplot as plt

# time temperture
tt = """
34.6 25   25   25
50.0 37.1 29.8 27.6
70.1 48.5 35.6 31.6
90.2 69.5 54.2 44.8
"""
rods = np.array(tt.split(), dtype=np.float).reshape(-1, 4)
b_temp = [34, 50, 70, 90]
plt.plot(b_temp, rods)
plt.xticks(b_temp, [str(b) for b in b_temp])
plt.xlabel('Bottom temperture')

plt.ylabel('Temperture')
plt.title("Temperture measured on rod")
plt.legend(["45mm", "150mm", "260mm", "355mm"])
plt.show()