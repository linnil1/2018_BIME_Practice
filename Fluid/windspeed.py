import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 101300)
C = 0.693 / np.sqrt(1 - 0.5 ** 4) * np.sqrt(2 / 1.225)
y = C * np.sqrt(x)

plt.title("Fan laws (Di/Do = 0.5)")
plt.plot(x, y)
plt.xlabel('Pressure Difference (Pa)')
plt.ylabel('Wind speed (m/s)')

plt.savefig("windspeed.png")
plt.show()
