from numpy import cos, sin, sqrt, arctan, pi
import numpy as np
def solve(want):
    want = list(want)

    k1 = 2 * want[2][0] * (want[0][0] * cos(want[0][1]) +
                           want[1][0] * cos(want[1][1]))
    k2 = 2 * want[2][0] * (want[0][0] * sin(want[0][1]) +
                           want[1][0] * sin(want[1][1]))
    k3 = (want[0][0]**2 + want[1][0]**2  +
          want[2][0]**2 - want[3][0]**2) + \
         2 * want[0][0] * want[1][0] * (
          cos(want[0][1]) * cos(want[1][1]) +
          sin(want[0][1]) * sin(want[1][1]))
    A = -k1 + k3
    B =   2 * k2
    C =  k1 + k3
    ans = [(-B - sqrt(B**2 - 4 * A * C)) / (2 * A),
           (-B + sqrt(B**2 - 4 * A * C)) / (2 * A)]
    return map(lambda a: 2 * np.arctan(a), ans)

def rad(x):
    return x * pi / 180

def goSim(phase, numpoint):
    l  = [7.5, 3.5, 7, 7.5]
    th = [rad(90), 0, 0, 0]
    l1 = [16, 15]
    th1 = [rad(180), rad(180 + 90)]

    vxy = []
    for i in np.linspace(phase, phase - 360, numpoint):
        th[1] = rad(i)
        ans = list(solve(zip(l, th)))
        x = 0
        y = 0
        th[2] = ans[1]
        for j in range(3):
            x += l[j] * cos(th[j])
            y += l[j] * sin(th[j])
        for j in range(len(l1)):
            x += l1[j] * cos(th[2] + th1[j])
            y += l1[j] * sin(th[2] + th1[j])
        vxy.append([x,y])

    vxy = np.array(vxy) / 100
    return vxy
