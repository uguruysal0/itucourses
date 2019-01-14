import cv2
import numpy as np
from scipy import signal


def randPoint(img, x, y):
    cords = np.random.randint(len(x))
    return img[x[cords], y[cords]]


def closest(val, point, centers):
    min = 0
    min_val = abs(centers[0] - val)
    for i in range(1, len(centers)):
        if abs(val - centers[i]) < min_val:
            min_val = abs(val - centers[i])
            min = i

    return min+1


def Kmeans(img, K=2, n_iters=20):
    np.random.seed(1)
    shape = img.shape
    x, y = np.where(img > 0)
    centers = [randPoint(img, x, y) for i in range(K)]
    clusters = np.zeros(shape)
    # Converge logic should be different
    for i in range(n_iters):

        for i in range(len(x)):
            clusters[x[i], y[i]] = closest(
                img[x[i], y[i]], (x[i], y[i]), centers)
        for i in range(K):
            mean = np.sum(img[clusters == i+1]) / \
                len(np.where(clusters == i+1)[0])
            centers[i] = mean

    clusters[clusters == 1] = round(centers[0])
    clusters[clusters == 2] = round(centers[1])

    # assumption ---  number of tumor pixels is less than number of normal pixels.

    a, b = len(np.where(clusters == round(centers[0]))[0]), len(
        np.where(clusters == round(centers[1]))[0])

    cv2.imwrite("clusters.jpg", clusters.astype(np.uint8))
    
    if a < b:
        clusters[clusters == round(centers[1])] = 0
    else:
        clusters[clusters == round(centers[0])] = 0

    return clusters


def getMask(img, threshold=55):
    mask = img.copy()
    mask[mask < threshold] = 0
    mask[mask >= threshold] = 255
    return mask


def extractSkull(mask):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask,  cv2.MORPH_OPEN, kernel, iterations=5)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask,  cv2.MORPH_OPEN, kernel, iterations=5)
    mask[mask == 255] = 1
    return mask


def getBoundaries(clusters):
    edges_y, edges_x = np.gradient(clusters)
    edges_y = edges_x + edges_y

    edges_y[edges_y == 0] = -1
    edges_y[edges_y > 0] = 1
    edges_y[edges_y == -1] = 0
    return edges_y


def segmentation(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    mask = getMask(img_gray)

    mask = extractSkull(mask)
    
    cv2.imwrite("mask.jpg", mask.astype(np.uint8)*255)

    img_gray = img_gray*mask
    clusters = Kmeans(img_gray, 2)

    

    boundaries = getBoundaries(clusters)

    x, y = np.where(boundaries != 0)
    img[ x,y ] = (0,0,255)
    cv2.imwrite("tumor boundaries.jpg",cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return img

