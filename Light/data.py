import numpy as np
from scipy.stats import t

light_type = ["A", "B", "C" ,"D" ,"E"]
data_dis_ori = """
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

dis_data = np.array(data_dis_ori.split(), dtype=np.float).reshape(3, 5, 5)
dis = np.array([20, 30, 37.5])
dis_name = ["照度（Lux）", "光量子密度 PPFD(umol/m^2s)", "有效光量電子密度 YPFD(umol/m^2s)", "R/B", "R/FR"]
dis_xname = "燈源與光譜儀距離 (cm)"

amp = np.array("0.51	0.78	0.59	0.58	0.72".split(), dtype=np.float)
amptext = "電流值(A)"

line_dis = np.array([5, 10, 15])
line_data = np.array("""
65.807 58.514 50.961
39.968 37.335 34.325
25.660 27.495 25.884
92.608 84.910 81.175
79.161 74.131 67.763
63.562 62.150 61.600""".split(), dtype=np.float).reshape(2, 3, 3)
line_text = "T5燈管間的水平距離(cm)"
reflect_text = ["無反光板", "裝反光板"]

another_data = np.array("""
1281 712 537 576 652 551
13.65 15.29 84.71 52.72 15.29 84.71
19.596 9.086 3.3572 6.9353 7.9326 2.7841""".split(), dtype=np.float).reshape(3, 6)
another_data = np.vstack([another_data[0] * another_data[1] / 1000, another_data[2]])

# this function modified from bending.py
def linearReg(x, y):
    x = np.array(x)
    y = np.array(y)
    # https://en.wikipedia.org/wiki/Simple_linear_regression
    # bx + a
    head_b = np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2)
    head_a = y.mean() - head_b * x.mean()
    fit_y = head_b * x + head_a
    r_square = np.sum((fit_y - y.mean()) ** 2) / np.sum((y - y.mean()) ** 2)

    # confidence of slope and intercept
    n = len(x)
    var_b = np.sum((y - fit_y) ** 2) / (n + 2) / np.sum((x - x.mean()) ** 2)
    intval_b = np.sqrt(var_b) * t.ppf(0.995, n - 2)
    var_a = var_b * np.sum(x ** 2) / n
    intval_a = np.sqrt(var_a) * t.ppf(0.995, n - 2)
    return head_a, intval_a, intval_b, head_b, r_square

def analysisOne(x, y):
    # plot
    head_a, intval_a, intval_b, head_b, r_square = linearReg(x, y)
    text = '''\
In 99% confidence
slope = {:.3}±{:.3}
intercept = {:.3}±{:.3}
r_squre = {:.3}
'''.format(head_b, intval_b, head_a, intval_a, r_square)
    fit_y = head_b * x + head_a
    return text, fit_y
