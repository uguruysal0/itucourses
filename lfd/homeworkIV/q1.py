import csv
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt



def LoadData(filePath):
    with open(filePath, 'r') as csvfile:
        buffer = list(csv.reader(csvfile))
        buffer = buffer[1:]
        data = np.array(buffer)
        labels = np.array(data[:,-1],int)
        features = np.array(data[:,:-1],float)
        return features,labels

class NN:
    def __init__(self,learning_rate=0.0001,layersize=10,n_iter=200):
        if layersize<=0:
            raise ValueError("Number of layers should be positive number current parameter {}".format(layersize))
        if n_iter <=0:
            raise ValueError("Number of iterations should be positive number current paramteter {}".format(n_iter))
        self.learning_rate = learning_rate
        self.layersize = layersize
        self.n_iter = n_iter
        self.logs = []

    def __sigmoid__(self,x):
        return 1.0/(1.0+np.exp(-x))
    
    def __forward__(self,X):
        z1 = X.dot(self.layer_1) + self.bias1
        layer_1_output = self.__sigmoid__(z1)
        z2 = layer_1_output.dot(self.output_layer) + self.bias2
        exp_scores = np.exp(z2)
        probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        return probs,layer_1_output
    
    def __backward__(self,probs,layer_1_output,X,Y):
        m = X.shape[0]
        delta1 = probs
        delta1[range(m), Y] -= 1
        delta_output_layer = (layer_1_output.T).dot(delta1)
        delta_b2 = np.sum(delta1, axis=0, keepdims=True)
        delta2 = delta1.dot(self.output_layer.T) * (layer_1_output*(1 - layer_1_output))
        delta_layer_1 = np.dot(X.T, delta2)
        delta_b1 = np.sum(delta2, axis=0)
        return delta_layer_1,delta_output_layer,delta_b1,delta_b2

    def __loss__(self,X,Y):
        m = X.shape[0]
        probs,layer_1_output = self.__forward__(X) 
        logprobs = -np.log(probs[range(m), Y])
        loss = np.sum(logprobs)
        return loss/m

    def train(self,X,Y):
        np.random.seed(0)
        numberOfClasses = len(set(Y))
        # init hidden layer and bias units
        self.layer_1 = np.zeros( (X[0].shape[0], self.layersize))
        self.output_layer = np.random.randn(self.layersize, numberOfClasses) #this inits converges better than zeros 

        self.bias1 = np.zeros((1, self.layersize))        
        self.bias2 = np.zeros((1, numberOfClasses))       

        for i in range(self.n_iter+1):
            # Shuffle data set
            idx = np.random.permutation(X.shape[0])
            X,Y= X[idx], Y[idx]
            # forward
            probs, layer_1_output = self.__forward__(X)
            # backward
            delta_layer_1, delta_output_layer, delta_b1, delta_b2   = self.__backward__(probs,layer_1_output,X,Y)
            #update
            self.layer_1 -= self.learning_rate * delta_layer_1
            self.bias1 -= self.learning_rate * delta_b1
            self.output_layer -= self.learning_rate * delta_output_layer
            self.bias2 -= self.learning_rate * delta_b2
            # save loss for loss curve
            self.logs.append(self.__loss__(X,Y))

    def predict(self,X):
        probs,a= self.__forward__(X)
        return np.argmax(probs, axis=1)

    def plot(self):
        plt.plot([i for i in range(len(self.logs))],self.logs)
        plt.title('Loss Curve')
        plt.ylabel("Loss (%)")
        plt.xlabel("Iteration")
        plt.show()

# Program Starts
# Load
train_data, train_labels = LoadData("dataTrain.csv")
test_data, test_labels   = LoadData("dataTest.csv")
# Scale data before train, zero mean unit variance
train_data = StandardScaler().fit_transform(train_data)
test_data = StandardScaler().fit_transform(test_data)
# Create an instance of neural network
nn = NN(learning_rate=0.0005,layersize=10,n_iter=200)
# Train
nn.train(train_data,train_labels)
# Predictions for test and train
pred_train = nn.predict(train_data)
pred_test = nn.predict(test_data)
# Results
print("Accuracy train acc {}".format(accuracy_score(train_labels,pred_train)))
print("Accuracy test acc  {}".format(accuracy_score(test_labels,pred_test)))
# Loss curve
nn.plot()