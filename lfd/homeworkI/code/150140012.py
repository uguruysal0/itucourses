# Ugur Uysal 150140012 python3 source code for BLG 454E Learnin From Data course#
# pip3 -install matplotlib to run the code  
import matplotlib.pyplot as plt
from functools import reduce
from math import ceil, floor, sqrt, pi, exp

def read_file(filename):
    with open(filename) as f:
        content = list(map(float, f.readlines()))
        return content


def getAssests(content):
    mean = reduce(lambda x, y: x + y, content) / len(content)
    variance = reduce(lambda x, y: x + y,
                      map(lambda x: (x - mean)**2, content)) / len(content)
    std = sqrt(variance)
    return mean, variance, std

def gassuianLikelihoodGenerator(mean,variance):
    i = 0
    res = []
    while i < 18:
        res.append( exp(-(((i-mean)**2)/(2*variance))) / sqrt(2*pi*variance))
        i+= 18/27
    return   res


data = read_file("data.txt")
mean, variance , std = getAssests(data)
y = gassuianLikelihoodGenerator(mean,variance)

n,bins,patches = plt.hist(data, bins=27, normed=1, facecolor='green', alpha=0.75,edgecolor='black')
plt.plot(bins, y, '-')
plt.title(r"""$\mathrm{{MLE\ results:}}\ \mu={0},\ \sigma={1}$""".format(
    "%.2f"%mean, "%.2f"%std))

plt.axis([0, 18, 0, 0.16])
plt.grid(True)
plt.show()