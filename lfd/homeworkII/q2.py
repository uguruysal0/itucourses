import csv
import numpy as np
from numpy.linalg import det as det
from numpy import transpose as tp
from numpy.linalg import inv as inv
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt


#standard IO method
def read(filename):
    data = []
    data_label = []
    labels = {}
    with open(filename, 'r') as csvfile:
        buffer = list(csv.reader(csvfile))
        for row in buffer:
            if len(row)==5:
              data.append( [ float(1),float(row[0]), float(row[1]),float(row[2]), float(row[3]) ]  )
              data_label.append(row[4])
              labels[row[4]]=data[len(data)-1]
    
    return np.array(data),data_label,labels



def sigmoid(z):
    return 1.0 / (1 + np.exp(-z))

#Cost function
def costFunction(w, data, label):
    h = sigmoid(data.dot(w))
    return (-label.T.dot(np.log(h)) - (1-label).T.dot(np.log(1 - h)))/len(data)


##This function creates the gradient component for each Theta value 
##The gradient is the partial derivative by Theta of the current value of theta minus 
##a "learning speed factor aplha" times the average of all the cost functions for that theta
##For each Theta there is a cost function calculated for each member of the dataset
def cfd(data,labels,w,j,m,alpha):
  sumErrors = 0
  for i in range(m):
    xi = data[i]
    xij = xi[j]
    hi = w.dot(data[i])
    error = (hi - labels[i])*xij
    sumErrors += error
  const = -1/len(labels)
  loss = const * sumErrors
  return loss

##For each theta, the partial differential 
##The gradient, or vector from the current point in Theta-space (each theta value is its own dimension) to the more accurate point, 
##is the vector with each dimensional component being the partial differential for each theta value
def gradientDescent(X,Y,theta,m,alpha):
	new_theta = []
	for j in range(len(theta)):
		CFDerivative = cfd(X,Y,theta,j,m,alpha)
		new_theta_value = theta[j] - CFDerivative
		new_theta.append(new_theta_value)
	return new_theta

##The high level function for the LR algorithm which, for a number of steps (num_iters) finds gradients which take 
##the Theta values (coefficients of known factors) from an estimation closer (new_theta) to their "optimum estimation" which is the
##set of values best representing the system in a linear combination model
def logisticRegression(data,labels,alpha,w,num_iters):
  for x in range(num_iters):
    w_ = loss_grad_softmax_vectorized(w,data,labels)
    theta = w_
    if x % 100 == 0:
      #here the cost function is used to present the final hypothesis of the model in the same form for each gradient-step iteration
      costFunction(data,labels,w)
  return theta


def loss_grad_softmax_vectorized(W, X, y):
    """ Compute the loss and gradients using softmax with vectorized version"""
    loss = 0 
    grad = np.zeros_like(W)
    dim, num_train = X.shape

    scores = W.dot(X) # [K, N]
    # Shift scores so that the highest value is 0
    scores -= np.max(scores)
    scores_exp = np.exp(scores)
    correct_scores_exp = scores_exp[y, range(num_train)] # [N, ]
    scores_exp_sum = np.sum(scores_exp, axis=0) # [N, ]
    loss = -np.sum(np.log(correct_scores_exp / scores_exp_sum))
    loss /= num_train
    #loss += 0.5 * reg * np.sum(W * W)

    scores_exp_normalized = scores_exp / scores_exp_sum
    # deal with the correct class
    scores_exp_normalized[y, range(num_train)] -= 1 # [K, N]
    grad = scores_exp_normalized.dot(X.T)
    grad /= num_train
    grad += W

    return grad


W = np.zeros((3, 5))
data, data_label,labels = read('iris.data')
print(logisticRegression(data,labels,0.1,W,100))

