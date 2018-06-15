import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
import csv
from functools import reduce



def LoadData(filePath):
    with open(filePath, 'r') as csvfile:
        buffer = list(csv.reader(csvfile))
        buffer = buffer[1:]
        data = np.array(buffer,float)
        return data


class KMeans():
    def __init__(self,K,n_iters=20):
        self.K = K
        print(K)
        self.n_iters = n_iters

    def __dist__(self,x,Y):
        dist_list = list(map( lambda t: np.sqrt((x[0]-t[0])**2+(x[1]-t[1])**2), Y )) 
        return dist_list.index(min(dist_list)),min(dist_list)

    # Convergence is wrong,
    # Needed to update
    # We should check centroids positions instead of constant number of iterations.
    # Iterations may be optional to make algorithm faster(but it can decrease the performance.)
    def train(self,X):
        K = self.K
        np.random.seed(1)
        centroids = X[ np.random.randint(X.shape[0], size=K) ]
        for it in range(self.n_iters):
            labels = [  self.__dist__(i,centroids)[0] for i in X ]
            labels_filtered = [ np.array(list(filter(lambda x: x is not None, [ X[j] if labels[j] ==i else None for j in range(len(X)) ] )))  for i in range(K) ]
            centroids = [ i.mean(0) for i in labels_filtered ]
        
        error = sum([  self.__dist__(i,centroids)[1] for i in X ], 0) 
        labels = [  self.__dist__(i,centroids)[0] for i in X ]
        return centroids,labels,error


    def plot(self,data,labels):
        ft = data.T[0]
        sd = data.T[1]
        colors = ['C0', 'C1','C2','C3','C4','C5','C6','C7','C8']
        plt.scatter( ft, sd, s = 15, c=labels, cmap=clrs.ListedColormap(colors))
        plt.xlabel('component 1')
        plt.ylabel('component 2')
        plt.title('K = {} - means '.format(self.K))
        plt.show()
        plt.savefig("fig.pdf"),
        return


            
data = LoadData("Cluster.csv")
reduced_data = PCA(n_components=2).fit_transform(data)
# scaling changes the clustering
# scaled_reduced_data = StandardScaler().fit_transform(reduced_data) 

# numbers to try
k = [1,2,5,10,20]
for i in k:
    km = KMeans(i,n_iters=100) 
    centroids,labels,error = km.train(reduced_data)
    print("K = {} and error = {}".format(i,error))
    km.plot(reduced_data,labels)
