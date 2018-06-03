freq = [0,30,125,250]
A = [2,4,-3,3]
phasors = [0,5/4,0,-1/4]


import matplotlib.pyplot as plt
from math import cos
from math import pi

x = []
y = []


def cosine(amplitude,freq, time, phasor):
    return amplitude*cos(2 * pi * freq * time - phasor*pi)


i = 0
while i < 0.1:
    x.append(i)
    t = 0
    for l in range(4):
        t += cosine(A[l],freq[l],i,phasors[l])
    y.append(t)
    i += 0.0001

print(x,y)
plt.plot(x, y)
plt.show()