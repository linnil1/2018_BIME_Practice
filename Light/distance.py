import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 9))

"""
A B C F G
目測燈管顏色	白	橘	藍	白	紅
電流值(A)	0.51	0.78	0.59	0.58	0.72

20 30 37.5
"""

data_ori = """
520	241	101	352	98
9.086	3.3572	6.9353	7.9326	2.7841
7.5746	3.0126	5.0793	6.4479	2.7191
0.42	2.15	0.01	0.26	171.29
7.26	7.01	1.03	6.09	49.52

337	160	66	235	57
5.8825	2.2275	4.6356	5.2699	1.6263
4.9021	1.9993	3.3935	4.2841	1.5862
0.42	2.14	0.01	0.26	127.33
7.34	7.01	1.32	5.68	44.87

262	112	49	156	51
4.5842	1.5580	3.4428	3.5249	1.4643
3.8227	1.3977	2.5203	2.8648	1.4258
0.42	2.12	0.01	0.26	89.87
7.27	7.02	0.95	6.21	35.4"""

data = np.array(data_ori.split(), dtype=np.float).reshape(3, 5, 5)
dis = np.array([20, 30, 37.5])

names = ["照度（Lux）", "光量子密度 PPFD(umol/m^2s)", "有效光量電子密度 YPFD(umol/m^2s)", "R/B", "R/FR"]
want = [0, 1, 3, 4]
for i in range(4):
    plt.subplot(221 + i)
    plt.title(names[want[i]] + " vs 距離")
    plt.ylabel(names[want[i]])
    plt.xlabel("燈源與光譜儀距離 (cm)")
    plt.plot(dis, data[:, want[i], :])
    plt.xticks(dis)
    plt.legend(["A", "B", "C" ,"D" ,"E"])
plt.savefig("distance.png")
plt.show()
