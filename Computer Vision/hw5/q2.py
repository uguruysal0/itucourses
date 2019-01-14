import cv2
import numpy as np
import os
from datetime import datetime


def normalize(X):
    mean = (np.sum(X, axis=0).reshape((1, -1)) / (X.shape[0]))
    sample_face = eigenvector_toImg(mean)
    cv2.imwrite("mean.jpg", sample_face)
    return X - mean, sample_face


def get_data(directory):
    global R
    global C
    elems = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".tif"):
                img = cv2.imread(os.path.join(root, file))
                R = img.shape[0]
                C = img.shape[1]
                elems.append(img.flatten())

    return np.array(elems)


def eigenvector_toImg(eigvector,  R=168, C=136, denorm=False):
    im = eigvector.reshape(R, C, 3)
    im = cv2.resize(im, (R, C))
    if denorm:
        for i in range(3):
            im[..., i] = scale(im[..., i])

    return im.astype(np.uint8)


def scale(im, a=0, b=255):
    mi = np.min(im)
    ma = np.max(im)
    return (im-mi)*(b-a)/(ma-mi)+a


def reduce_dim(vectors, data, dim=None):
    if dim is None:
        dim = vectors.shape[0]
    return np.dot(data, vectors[:dim].T)


def add_gaussian(data):
    noise = np.random.normal(0, 2, data.shape)
    return data+noise


def get_closest(data, point):
    mindex = 0
    mi = np.sum((data[0] - point)*(data[0] - point)) / (point.shape[0])
    print("Index and Cost")
    for i in range(1, data.shape[0]):
        dist = np.sum((data[i] - point)*(data[i] - point)) / (point.shape[0])
        print("i: {} distance: {}".format(i, dist))
        if dist < mi:
            mindex = i
            mi = dist
    return i


def eigen_faces(X, R=168, C=136):
    u, s, v = np.linalg.svd(X, full_matrices=False)
    ims = []
    for i in range(5):
        sample_face = eigenvector_toImg(v[i], R, C, denorm=True)
        cv2.imwrite("eigenc_face_{}.jpg".format(i), sample_face)
        ims.append(sample_face)
    return ims


X = get_data("Face_database")
X, mean = normalize(X)


random_elem = np.random.randint(0, 32)
c = X[random_elem]
c = add_gaussian(c)
X[random_elem] = c
print("RANDOM ELEM is {}".format(random_elem))
u, s, v = np.linalg.svd(X, full_matrices=False)
reducedX = reduce_dim(v, X, dim=5)
reducedC = reduce_dim(v, c, dim=5)
get_closest(reducedX, reducedC)
