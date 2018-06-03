import csv
import numpy as np
from numpy.linalg import det as det
from numpy import transpose as tp
from numpy.linalg import inv as inv
import matplotlib.pyplot as plt

#standard IO method
def read(filename):
    data = []
    data_label = []
    with open(filename, 'r') as csvfile:
        buffer = list(csv.reader(csvfile))
        for numberOfRows in range(1,len(buffer)):
            row = buffer[numberOfRows]
            data.append( [ float(row[0]), float(row[1]) ]  )
            data_label.append(int(row[2]))
    
    return np.array(data),np.array(data_label)


#Covariance Matrix Calculation Method
#Let data_t matrix (n*d) and data_label is label feature vector(both np.array).
#first get labels from data and split them into arrays
#to calculate particular matrices. 
#let x = ([ones matrix (n*n)]*data)/(number of rows in data) -> each cell of same column is equal to mean of that column.  
#let y = data - x -> now y equal to each element that difference from mean. 
#let z = (y.T*y)/n(number of rows in data) ->  y transpose * y gives us element wise squares and divide them to n
#Now have easy cov matrix.
#Return covMatrices dictionary with i[key] = matrix where matrix is np array.
#meanVectors 1 x numberofclasses shaped np.array 
#classP each class probabilty.
def covm(data_t,data_label):
    
    labels = {}
    for i in range(len(data_label)):
        try:
            labels[ data_label[i] ].append(data_t[i])
        except:
            labels[ data_label[i] ] = []
            labels[ data_label[i] ].append(data_t[i])
    
    covMatrices = {}
    meanVectors = {}
    classP = {}
    for key in labels:
        data = np.array(labels[key])
        x =  (np.ones((len(data),len(data))).dot(data))/len(data)
        #this is not elegant----
        mean_1 = x[0][0]
        mean_2 = x[0][1]
        mean = [mean_1,mean_2]
        #------------------
        x = data - x
        
        covMatrices[key] = (tp(x).dot(x))/len(data)
      
        classP[key] = len(labels[key]) / len(data_train)
        meanVectors[key] = tp([mean])
    
    return covMatrices, meanVectors, classP   


#Discrimannt function calculator
#This is simple arithmetic operation
def condProb(x,covM,meanV,classC):
    y = tp([x])
    dif = y-meanV
    return np.exp ( -0.5 *np.dot(np.dot( tp(dif), inv(covM)), dif)) / np.sqrt( (2*np.pi)*det(covM))


def make_guess(data,covM,meanV,classC):
    maxL = float('-inf')
    guess = -1
    for key in covM:
        if  maxL < condProb(data, covM[key], meanV[key], classC[key]):
            guess = key
            maxL = condProb(data, covM[key], meanV[key], classC[key])
    return guess

#Predictions for test data
def pred(data,data_label,covM,meanV,classC):
    pred_label = []
    acc = 0
    for i in range(len(data_label)):
        guess = make_guess(data[i],covM,meanV,classC)
        pred_label.append(guess)
        if guess == data_label[i]:
            acc+=1
    return acc/len(data_label),pred_label


    
data_train, data_train_label  = read('datatrain.csv')
data_test, data_test_label  = read('datatest.csv')

covM, meanV, classC = covm(data_train,data_train_label)

acc, predictons = pred(data_test,data_test_label,covM,meanV,classC)

print(acc)



#from the link given at homework PDF
h = 0.02
x_min, x_max = data_test[:, 0].min() - .5, data_test[:, 0].max() + .5

y_min, y_max = data_test[:, 1].min() - .5, data_test[:, 1].max() + .5
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

Z = np.zeros_like(xx).reshape(-1)

for ix, i in enumerate(np.c_[xx.ravel(), yy.ravel()]):
    Z[ix] = make_guess(i,covM,meanV,classC)

Z = Z.reshape(xx.shape)
plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired)

plt.xlabel("X 1")
plt.ylabel("X 2")

plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.xticks(())
plt.yticks(())
plt.show()
