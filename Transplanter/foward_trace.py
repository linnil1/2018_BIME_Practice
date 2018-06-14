import numpy as np
import matplotlib.pyplot as plt

from simulate import goSim
from trace import *
one = 11
real_t = t[:one]
vxy = goSim(0, one * 10) 

real_t -= real_t.min()
t = real_t.max() / one

plt.title("Trace of transplanter with const speed forwarding")
n = 3
plt.plot(np.tile(vxy[:, 0], n) + 0.3 * np.linspace(0, real_t.max() * n, one * 10 * n),
         np.tile(vxy[:, 1], n))
plt.xlabel("X(m)")
plt.ylabel("Y(m)")
plt.savefig("forward_trace.png")
plt.show()

