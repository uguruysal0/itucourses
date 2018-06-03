import matplotlib.pyplot as plt
from math import sqrt,pi,exp
import numpy as np
from functools import reduce

def read_file(filename):
    with open(filename) as f:
        content = list(map(float, f.readlines()))
        return content


def getAssests(content):
    mean = reduce(lambda x, y: x + y, content) / len(content)
    variance = reduce(lambda x, y: x + y,
                      map(lambda x: (x - mean)**2, content)) / len(content)
    std = sqrt(variance)
    return mean, std

data = read_file("data.txt")
mu,sigma = getAssests(data)
count, bins, ignored = plt.hist(data, 18, normed=True)
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
                np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
          linewidth=1, color='black')
plt.show()