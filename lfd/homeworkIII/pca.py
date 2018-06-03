import csv
import numpy as np
from numpy import transpose as tp
import matplotlib.pyplot as plt
import sklearn.preprocessing as standardization
import random


k = 2

# standard IO method for CSV files returns np.array
def read(filename):
    with open(filename, 'r') as csvfile:
        buffer = list(csv.reader(csvfile))
        return np.array(buffer,float)
    
data = read("data.txt")

# last column represent the labels 
labels = data.T[64:65]

data = data.T[:64].T

# built-in eigen values and eigen vectors
eigenvalues, eigenvectors = np.linalg.eig(np.cov(tp( data)))

# only k dimension sliced
new_data = np.dot(data,eigenvectors).T[:k].T

#built-in PCA is  different from my PCA I guesss it's about the standardization.

# axixes
ft = tp(new_data)[0:1]
sd = tp(new_data)[1:2]


fig, ax = plt.subplots()
ax.scatter(ft, sd)
randoms = {}
while True:
    i = random.randrange(len(data))
    if  i not in randoms:
        ax.annotate(str(int(labels[0][i])), (ft.T[i],sd.T[i]))
        randoms[i] = True
    if len(randoms)>=200:
        break

plt.xlabel("first eigen vector")
plt.ylabel('second eigen vector')
plt.title('Data after PCA')
plt.show()




