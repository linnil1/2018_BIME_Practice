import numpy as np
import matplotlib.pyplot as plt
from trace import *
from simulate import goSim

def getR2(name, sim, real):
    tot = np.sum((real - real.mean()) ** 2)
    res = np.sum((sim - real) ** 2)
    print("R^2 of", name, ":", 1 - res / tot)

# load
one = 11
real_t = t[:one]
real_ax = ax[:one - 2]
real_ay = ay[:one - 2]
real_t -= real_t.min()
t = (real_t.max() - real_t.min()) / one

# data
# Ax	Ay	Az	Angle	Time(ms)
data = np.array("""
0.32	0.02	-0.26	-12.86	7518
-0.36	1.4	-0.44	7.94	7618
-0.53	0.32	0.98	24.24	7719
0.81	2	-1.02	24.59	7817
-0.48	2	-0.71	19.78	7918
0.32	1.22	0.49	-11.09	8018
-0.83	0.93	-0.55	-7.85	8118
-0.4	-0.14	-0.87	-18.11	8218
0.32	0.3	-1.01	-34.7	8319
0.16	0.07	-0.74	-34.43	8418
-0.02	0.59	-0.71	0.09	8518
-0.45	0.82	-0.01	13.53	8619
0.18	1.14	0.31	27.97	8719
1.64	-2	1.77	33.4	8820
-0.09	1.76	-0.45	-2.42	8919
-0.35	-0.16	0.21	-14.06	9020
-0.77	-0.35	-0.34	-0.21	9121
-0.19	0.35	-1.07	-2.99	9220
-0.09	-0.02	-0.73	-25.77	9320
0.3	0.26	-0.77	2.67	9420
0.13	1.98	-1.43	17.74	9520
0.58	0.22	0.47	28.12	9621
-0.07	2	-1.15	27.01	9721
""".split(), dtype=np.float).reshape(-1, 5)

# cal
ac_t = (data[:, 4] - data[:, 4].min()) / 1000
th = data[:, 3] * np.pi / 180
ax = data[:, 2] * np.cos(th) - data[:, 1] * np.sin(th)
ay = data[:, 2] * np.sin(th) + data[:, 1] * np.cos(th)
ax = ax * 9.81
ay = ay * 9.81 - 9.81

# simulate acceration
vxy = goSim(40, one * 10)
vx = (vxy[1:, 0] - vxy[:-1, 0]) / (t / 10)
vy = (vxy[1:, 1] - vxy[:-1, 1]) / (t / 10)
sim_ax = (vx[1:] - vx[:-1]) / (t / 10)
sim_ay = (vy[1:] - vy[:-1]) / (t / 10)

# repeat
n = 3
mult_t = np.linspace(0, real_t.max(), one * 10)[1:-1]
mult_t = np.hstack([mult_t + t * one * i for i in range(n)])
mult_ax = np.tile(sim_ax, n)
mult_ay = np.tile(sim_ay, n)

# analysis
corres = [np.where(mult_t >= act)[0][0] for act in ac_t]
getR2("Ax", mult_ax[corres], ax)
getR2("Ay", mult_ay[corres], ay)


# plot 
plt.figure(figsize=(12, 6))
plt.subplots_adjust(left=0.07, right=0.97,top=0.90, bottom=0.10, wspace=0.25)

plt.subplot(1, 2, 1)
plt.title("X-Acceration detected by sensor compare to acceration trace of Transplanter")
plt.xlabel("Time(s)")
plt.ylabel("a($m/s^2$)")
plt.plot(ac_t, ax, label="x")
plt.plot(mult_t, mult_ax, '--', label='sim_x')
plt.legend()

plt.subplot(1, 2, 2)
plt.title("Y-Acceration detected by sensor compare to acceration trace of Transplanter")
plt.xlabel("Time(s)")
plt.ylabel("a($m/s^2$)")
plt.plot(ac_t, ay, label="y")
plt.plot(mult_t, mult_ay, '--', label='sim_y')
plt.legend()
plt.savefig("fail_acmeter.png")
plt.show()
