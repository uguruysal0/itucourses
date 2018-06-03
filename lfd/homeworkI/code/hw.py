import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

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
    while i <= 20:
        res.append((1/(sqrt(2*pi*variance))*exp(-((i-mean)**2)/(2*variance) )))
        i+= 0.01

    return   res


#x = sorted(read_file("data.txt"))
#mean, variance , std = getAssests(x)

#n, bins, patches = plt.hist(x, 1999, normed=1, facecolor='green', alpha=0.75)

#l = plt.plot(bins,gassuianLikelihoodGenerator(mean,variance), '-')
data = read_file("data.txt")


# Fit a normal distribution to the data:
mu, std = norm.fit(data)

# Plot the histogram.
plt.hist(data, bins=25, normed=True, alpha=0.6, color='g')

# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k')
title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
plt.title(title)

plt.show()

#data = read_file("data.txt")
#mean, variance = getAssests(data)
 
