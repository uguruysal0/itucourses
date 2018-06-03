import numpy as np 

basex = [2,4,6,4,2]
baseh = [3,-1,2,1]

x = np.array(basex)
h = np.array( [ [0 for t in basex]]*(len(baseh)+len(basex)-1))

#settingg values 
for i in range(len(baseh)+len(basex)-1):
    for j in range(len(baseh)):
        try:
            h[i+j][i] = baseh[j]
        except:
            pass

#matrix product
y = h.dot(x)
#result
print(y)