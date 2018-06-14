import numpy as np
import matplotlib.pyplot as plt

data = np.array("""
0	27	0
100	30	-5
200	24	10
300	25	29
400	29	40
500	28	44
600	24	45
700	19	36
800	17	20
900	24	4
1000	31	-6
1100	25	4
1200	24	25
1300	28	37
1400	29	43
1500	26	45""".split(), dtype=np.float).reshape(-1, 3).T

x = data[1] * 0.005
y = data[2] * 0.005
t = data[0, :] / 1000
vx = (x[1:] - x[:-1]) / (t[1:] - t[:-1])
vy = (y[1:] - y[:-1]) / (t[1:] - t[:-1])
ax = (vx[1:] - vx[:-1]) / (t[2:] - t[1:-1])
ay = (vy[1:] - vy[:-1]) / (t[2:] - t[1:-1])

"""
plt.plot(x, y, 'o-')
plt.xlabel("X(m)")
plt.ylabel("Y(m)")
plt.title("Trace of Transplanter")
plt.savefig("Trace.png")
plt.plot(x, y)
"""

if __name__ == '__main__':
    plt.figure(figsize=(12, 6))
    plt.subplots_adjust(left=0.07, right=0.97,top=0.90, bottom=0.10, wspace=0.25)
    plt.subplot(1, 2, 1)
    plt.title("Velocity of trace of Transplanter")
    plt.xlabel("Time(s)")
    plt.ylabel("V(m/s)")
    plt.plot(t[1:], vx, label='x')
    plt.plot(t[1:], vy, label='y')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.title("Accerlation of trace of Transplanter")
    plt.xlabel("Time(s)")
    plt.ylabel("a($m/s^2$)")
    plt.plot(t[2:], ax, label='x')
    plt.plot(t[2:], ay, label='y')
    plt.legend()
    plt.savefig("Trace_v_a.png")

    plt.show()
