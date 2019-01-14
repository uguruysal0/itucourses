import numpy as np
from math import ceil, floor


def deriv_x(px, py, image):
    res = 0
    try:
        val = image[px+1][py] - image[px-1][py]
        return val/2
    except:
        pass

    try:
        val = image[px+1][py] - image[px][py]
        return val
    except:
        pass
    try:
        val = image[px][py] - image[px-1][py]
        return val
    except:
        pass

    return res


def deriv_y(px, py, image):
    res = 0
    try:
        val = image[px][py+1] - image[px][py-1]
        return val/2
    except:
        pass

    try:
        val = image[px][py+1] - image[px][py]
        return val
    except:
        pass

    try:
        val = image[px][py] - image[px][py-1]
        return val
    except:
        pass

    return res


def bilinear(x, y, image):

    if x < 0 or y < 0:
        x = 0
        y = 0

    val = 0

    # this written for bicubic but it did not work.
    # x_0, y_0 = ceil(x),  floor(y)
    # x_1, y_1 = floor(x), ceil(y)
    # fi = np.array([[1, 0, 0, 0],
    #                [0, 0, 1, 0],
    #                [-3, 3, -2, -1],
    #                [2, -2, 1, 1]])
    # mid = np.array([[image[x_0][y_0], image[x_0][y_1], deriv_y(x_0, y_0, image), deriv_y(x_0, y_1, image)],
    #                 [image[x_1][y_0], image[x_1][y_1],
    #                  deriv_y(x_1, y_0, image), deriv_y(x_1, y_1, image)],
    #                 [deriv_x(x_0, y_0, image), deriv_x(x_0, y_1, image), 0, 0],
    #                 [deriv_x(x_1, y_0, image), deriv_x(x_1, y_1, image), 0, 0]])

    # th = np.array([[1, 0, -3, 2],
    #                [0, 0, 3, -2],
    #                [0, 1, -2, -1],
    #                [0, 0, -1, 1]])

    # coef = np.dot(fi, np.dot(mid, th))
    # print(fi, mid, th)
    # print(coef)
    # l = np.array([1, x, x**2, x**3])
    # r = np.array([1, y, y**2, y**3])
    # val = np.dot(l, np.dot(coef, r))

    try:
        x_0, y_0 = floor(x),  floor(y)
        x_1, y_1 = ceil(x), ceil(y)
        val = (x_1-x)*(y_1-y)*image[x_0][y_0] + \
            (x-x_0)*(y-y_0)*image[x_0][y_1] + \
            (x_1-x)*(y-y_0)*image[x_1][y_0] + \
            (x-x_0)*(y_1-y)*image[x_1][y_1]
    except:
        print(floor(x), floor(y))
        print(ceil(x), ceil(y))
    return val


def backward_mapping(image, transformation_matrix, scale=1):
    inverse = y = np.linalg.inv(transformation_matrix)
    nch_1 = np.zeros((int(image.shape[0]*scale), int(image.shape[1]*scale)))
    nch_2 = np.zeros((int(image.shape[0]*scale), int(image.shape[1]*scale)))
    nch_3 = np.zeros((int(image.shape[0]*scale), int(image.shape[1]*scale)))

    for i in range(nch_1.shape[0]):
        for j in range(nch_1.shape[1]):
            new_point = np.dot(np.array([i, j, 1]), inverse)
            val = bilinear(
                new_point[0], new_point[1], image[..., 0])
            nch_1[i][j] = val

    for i in range(nch_1.shape[0]):
        for j in range(nch_1.shape[1]):
            new_point = np.dot(np.array([i, j, 1]), inverse)
            val = bilinear(
                new_point[0], new_point[1], image[..., 1])
            nch_2[i][j] = val

    for i in range(nch_1.shape[0]):
        for j in range(nch_1.shape[1]):
            new_point = np.dot(np.array([i, j, 1]), inverse)
            val = bilinear(
                new_point[0], new_point[1], image[..., 2])
            nch_3[i][j] = val

    return np.dstack((nch_1, nch_2, nch_3)).astype(np.uint8)
