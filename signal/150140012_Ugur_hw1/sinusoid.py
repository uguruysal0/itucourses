import matplotlib.pyplot as plt
from math import cos
from math import pi

x = []
y = []

#just produce value for with the paramteres this is for question 7, push time an array and value to anotherthen  plot them
def cosine(amplitude,freq, time, phasor):
    return amplitude*cos(2 * pi * freq * time - phasor*pi)


i = 0
while i < 0.1:
    x.append(i)
    y.append(cosine(6,100, i, 0.19))
    i += 0.0001

#print(x,y)
plt.plot(x, y)
plt.show()