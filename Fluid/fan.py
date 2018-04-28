import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0.1, 1)
y =  x ** 3

plt.title("Fan laws")
plt.plot(x, y)
plt.xlabel('rpm ratio of fan')
plt.ylabel('Power ratio')

plt.savefig("fan.png")
plt.show()
