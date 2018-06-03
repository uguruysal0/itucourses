import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# assuming image is 3 channeled
def SVD_Image(img,k=None):
    channel_1 = img[:,:,0]
    channel_2 = img[:,:,1]
    channel_3 = img[:,:,2]

    channel_1_svd =  SVD(channel_1,k)
    channel_2_svd =  SVD(channel_2,k)
    channel_3_svd =  SVD(channel_3,k)

    return  np.dstack( [channel_1_svd,channel_2_svd,channel_3_svd]).astype(np.uint8)
     

# 2-D matrix SVD
def SVD(mat,k=None):
    flag = False
    if mat.shape[0] < mat.shape[1]:
        mat  = mat.T
        flag = True

    if k is None:
        k = mat.shape[1]
    else:
        k = int((k/100)*mat.shape[1])


    # V matrix
    # burada eigen valueler sortladım ona correspond eden vektörlerle falan denedim 
    # ancak eigen valueler negatif gelitor burada mutlak değer vb negatiflii atıcak şeyler denedim
    # ancak bunların yardımı dokunmadı 
    # ki zaten benim yazdığım SVD bütün eigenvectorlerle hesaplarken tekrar aynı matrixi oluşturuyor ancak
    # K tane seçerken en anlamlı olanları seçemiyor o yüzden kötü sonuç veriyor.
    # yine aşağdaki kod parçasını uğraştığım belli olsun diye bırakıyorum bir sürü şey de denedim
    # ancak yararlı sonuçlar olmadı
    #---------------------------
    #  eigVal, V =  np.linalg.eig(np.dot(mat.T,mat))
    # V=np.array(V).T
    # ev_list = list(zip(eigVal,V))
    # ev_list.sort(key=lambda tup:np.abs(tup[0]), reverse=True)
    # eigVal, V = zip(*ev_list)
    # V=np.array(V).T
    # --------------------------
    eigVal, v =  np.linalg.eig(np.dot(mat.T,mat))
    v=np.array(v).T

    u = np.zeros((mat.shape[0],mat.shape[0]))
    
    # U matrix

    for i in range(mat.shape[1]):
        u[i] = np.dot(mat,v.T[i]) / np.sqrt(np.abs(eigVal[i]))
    

    # mat*mat^T den gelen eigenvectorler aynı sıralama mantığıyla U yu ıluşturmayı denedim ancak sıkıntılar çıktı
    # farklı bir metod denedim U yu oluşturmak için daha iyi sonuçlar aldım ama hala çok kötü sonuçlar
    # -------------
    # eigValU, U =  np.linalg.eig(np.dot(mat,mat.T))
    # U = np.array(U).T
    # ev_list = list(zip(eigValU,U))
    # ev_list.sort(key=lambda tup:np.abs(tup[0]), reverse=True)
    # eigValU, U = zip(*ev_list)
    # U = np.array(U)
    #----------
    # Sigma matrix
    # sigma için Sigma = U^T*A*V yi denedim ancak o zaman diagonal bir matrix gelmiyordu 
    # ----------------
    s = np.zeros(mat.shape)

    for i in range(len(eigVal)):
        try:
            s[i][i] = np.sqrt(np.abs(eigVal[i]))
        except:
            break
    
    res = np.dot(u.T[:,:k],np.dot(s[:k,:k],v.T[:k,:]))

    if flag:
        return res.T
    return res

img=mpimg.imread('data.jpg')
k = [1,5,20,50,100]
for i in k:
    new_img = SVD_Image(img,i)
    mpimg.imsave("after"+str(i)+".jpg",new_img)


