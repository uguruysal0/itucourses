from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def convertFromImage(image):
    return np.array(image)

def convertToImage(data):
    return Image.fromarray(data,'RGB')

def divideRGB(imageData):
    redData   = np.array(imageData[:, :, 0])/255
    greenData = np.array(imageData[:, :, 1])/255
    blueData  = np.array(imageData[:, :, 2])/255
    return redData, greenData, blueData

def getKRateMatrix(u, s, v, k):
    u_k = u[:,0:k]
    s_k = np.diag(s[0:k])
    v_k = v[0:k,:]
    return u_k, s_k, v_k

def mergeRGB(r,g,b):
    merged = np.zeros((len(r),len(r[1,:]),3))
    merged[:, :, 0] = r*255
    merged[:, :, 1] = g*255
    merged[:, :, 2] = b*255

    merged[merged>255] = 255
    merged[merged<0] = 0
    return np.array(merged, dtype='uint8')


def getSVD(matrix):
    a = np.array(matrix)
    aT = np.transpose(a)
    aTa = np.dot(aT,a)
    s2, v = np.linalg.eig(aTa)
    vT = np.transpose(v)
    s = np.abs(s2) ** 0.5
    sI = np.linalg.inv(np.diag(s))
    u = np.dot(a, np.dot(v, sI))
    return np.real(u), np.real(s), np.real(vT)


def getA(u,s,v):
    return np.dot(u,np.dot(s,v))

def main(imageName, k):
    img = Image.open(imageName)
    data = convertFromImage(img)
    #first we are dividing the image into its rgb matrices
    r,g,b = divideRGB(data)

    #then we apply svd to each matrix and find each of their u, s (sigma), v values
    rU, rS, rV = getSVD(r)
    gU, gS, gV = getSVD(g)
    bU, bS, bV = getSVD(b)
    #then we apply the K rate
    rUK, rSK, rVK = getKRateMatrix(rU,rS,rV,k)
    gUK, gSK, gVK = getKRateMatrix(gU,gS,gV,k)
    bUK, bSK, bVK = getKRateMatrix(bU,bS,bV,k)

    #we are getting the dot product for each u,s,v for each color matrix and combining them into image data
    #mergedData = mergeRGB(getA(rU, rS, rV), getA(gU, gS, gV), getA(bU, bS, bV))
    mergedData = mergeRGB(getA(rUK, rSK, rVK), getA(gUK, gSK, gVK), getA(bUK, bSK, bVK))

    #we are converting the image data to image object (to Pillow display)
    #newImage = convertToImage(mergedData)

    #then we return this image object
    return mergedData


def applyKRate():
    print("Calculating K=1 rate")
    img_1 = main('data.jpg',1)
    mpimg.imsave("baska_1.jpg",img_1)

    print("Calculating K=5 rate")
    img_5 = main('data.jpg',5)
    mpimg.imsave("baska_5.jpg",img_5)

    print("Calculating K=20 rate")
    img_20 = main('data.jpg',20)
    mpimg.imsave("baska_20.jpg",img_20)


    print("Calculating K=50 rate")
    img_50 = main('data.jpg',50)
    mpimg.imsave("baska_50.jpg",img_50)

    return img_1, img_5, img_20, img_50


img_1, img_5, img_20, img_50 = applyKRate()
# fig, ((oi1,i1),(oi2,i5),(oi3,i20),(oi4,i50)) = plt.subplots(4,2)
# img = convertFromImage(Image.open("data.jpg"))
# oi1.imshow(img)
# oi2.imshow(img)
# oi3.imshow(img)
# oi4.imshow(img)
# i1.imshow(img_1)
# i5.imshow(img_5)
# i20.imshow(img_20)
# i50.imshow(img_50)
# fig.show()












