import numpy as np
import matplotlib.pyplot as plt
from trace import *
from simulate import goSim

def getR2(name, sim, real):
    tot = np.sum((real - real.mean()) ** 2)
    res = np.sum((sim - real) ** 2)
    print("R^2 of", name, ":", 1 - res / tot)

# load data
one = 11
real_x = x[:one]
real_y = y[:one]
real_vx = vx[:one - 1]
real_vy = vy[:one - 1]
real_ax = ax[:one - 2]
real_ay = ay[:one - 2]
real_t = t[:one]

# simulate
vxy = goSim(180, one * 10) # phase

# position
plt.title("Simulating trace of Transplanter")
plt.xlabel("X(m)")
plt.ylabel("Y(m)")
plt.plot(vxy[:, 0], vxy[:, 1])
plt.savefig("trace_simulate.png")
plt.show()

# position analysis
sim_x = vxy[::10, 0] - vxy[::10, 0].mean()
real_x = real_x - real_x.mean()
sim_y = vxy[::10, 1] - vxy[::10, 1].mean()
real_y = real_y - real_y.mean()

sxy = np.sum((sim_x - real_x) * (sim_y - real_y))
sxx = np.sum((sim_x - real_x) ** 2)
syy = np.sum((sim_y - real_y) ** 2)
res = np.sum((sim_x - real_x) ** 2 + (sim_y - real_y) ** 2)
tot = np.sum(sim_x ** 2 + sim_y ** 2)
print("Position Coefficient")
print("r :", sxy / np.sqrt(sxx * syy))
print("R^2 :", 1 - res / tot) 

# position compare
plt.title("Comparing trace of Transplanter")
plt.plot(sim_x,  sim_y, 'o-', label="simulate_discrete")
plt.plot(vxy[:, 0] - np.mean(vxy[:, 0]), vxy[:, 1] - np.mean(vxy[:, 1]), label="simulate")
plt.plot(real_x, real_y, label='real')
plt.xlabel("X(m)")
plt.ylabel("Y(m)")
plt.legend()
plt.savefig("trace_simulate_comp.png")
plt.show()

# velcoity analysis
vxy = goSim(230, one * 10) # phase
t = (real_t.max() - real_t.min()) / one
vx = (vxy[1:, 0] - vxy[:-1, 0]) / (t / 10)
vy = (vxy[1:, 1] - vxy[:-1, 1]) / (t / 10)
vx_dis = vx[4:-5:one]
vy_dis = vy[4:-5:one]
getR2("Vx", vx_dis, real_vx)
getR2("Vy", vy_dis, real_vy)

# velcoity plot
plt.title("Velocity of trace of Transplanter")
plt.xlabel("Time(s)")
plt.ylabel("V(m/s)")
plt.plot(real_t[1:] - t / 2, real_vx, label='real_x')
plt.plot(real_t[1:] - t / 2, real_vy, label='real_y')

plt.plot(np.linspace(real_t.min(), real_t.max(), one * 10)[:-1],
         vx, '--', label='sim_x')
plt.plot(np.linspace(real_t.min(), real_t.max(), one * 10)[:-1],
         vy, '--', label='sim_y')
plt.legend()
plt.savefig("Trace_v_comp.png")
plt.show()

# acceration analysis
ax = (vx[1:] - vx[:-1]) / (t / 10)
ay = (vy[1:] - vy[:-1]) / (t / 10)
ax_dis = ax[10:-9:one]
ay_dis = ay[10:-9:one]
getR2("ax", ax_dis, real_ax)
getR2("ay", ay_dis, real_ay)

# acceration plot
plt.title("Accerlation of trace of Transplanter")
plt.xlabel("Time(s)")
plt.ylabel("a($m/s^2$)")
plt.plot(real_t[1:-1], real_ax, label='x')
plt.plot(real_t[1:-1], real_ay, label='y')
plt.plot(np.linspace(real_t.min(), real_t.max(), one * 10)[:-2],
         ax, '--', label='sim_x')
plt.plot(np.linspace(real_t.min(), real_t.max(), one * 10)[:-2],
         ay, '--', label='sim_y')
plt.legend()
plt.savefig("Trace_a_comp.png")
plt.show()

# plt.figure(figsize=(12, 6))
# plt.subplots_adjust(left=0.07, right=0.97,top=0.90, bottom=0.10, wspace=0.25)
