from scipy.io import wavfile as wav
import numpy as np
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline



data_train_label = []
data_test_label  = []

data_ones = []
data_twos = []

base = 'Ses'
direct = 'data/'
for i in range(1,41):
    rate, sound = wav.read(direct+base+str(i)+'.wav')
    sound = sound[:,0]
    if i<=20:
        if i <=15:
            data_train_label.append(0)
        data_ones.append(np.fft.fft(sound)[:100])
    else:
        if i <=35:
            data_train_label.append(1)
        data_twos.append(np.fft.fft(sound)[:100])

data_train = data_ones[:15] + data_twos[:15] 
data_test  = data_ones[15:] + data_twos[15:]

pca = PCA(n_components=5)
cls = LogisticRegression() 

pipe = Pipeline([('pca', pca), ('logistic', cls)])

data_train = np.array(data_train)

data_test = np.array(data_test)

data_train_label = np.array(data_train_label)

pipe.fit(data_train,data_train_label.ravel())

predictions = pipe.predict(data_test)

print(*predictions)