import numpy as np
import matplotlib.pyplot as plt

# time temperture
tt = """
0 34.6
1 34.7
2 35.1
3 36.0
4 37.4
5 39.8
6 42.7
7 46.0
8 49.8
9 53.7
10 58.1
11 62.4
12 66.9
13 70.9
14 76.0
15 81.8
16 85.6
17 88.9
18 92.7
19 96.8
20 98.0
21 98.3
22 98.4"""

time_temp = np.array(tt.split(), dtype=np.float).reshape(-1,2)
ht = 22
kwh = 0.3
water_weight = 500
heat_time = np.linspace(0, ht)
temp_min = time_temp[:, 1].min()
cal_t = kwh * 1000 * 60 * 60 / 4.2 / water_weight
plt.plot(time_temp[:, 0], time_temp[:, 1], 'b')
plt.ylim([temp_min, temp_min + cal_t])
plt.ylabel('Temperture', color='b')
plt.xlabel('Time(min)')
plt.tick_params('y', colors='b')

plt.twinx()
heat_kwh = np.linspace(0, kwh)
plt.plot(heat_time, heat_kwh, 'r')
plt.ylim(ymin=0)
plt.ylabel('Energy(kWh)', color='r')
plt.tick_params('y', colors='r')
plt.show()