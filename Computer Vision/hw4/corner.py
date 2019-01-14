import cv2
import numpy as np
from scipy import signal


def filterFactory(filterName):
    filter_x = None
    if filterName == "sobel":
        filter_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    if filterName == "prewitt":
        filter_x = np.array([[-1, -1, -1], [0, 0, 0, ], [1, 1, 1]])

    if filter_x is None:
        raise ValueError("Given filter is not found.")
    return filter_x, filter_x.T


def imgConv(img, kernel, threshold=10):
    C = img.shape[2]
    res = np.ones(img.shape)
    for i in range(C):
        res[:, :, i] = signal.convolve2d(img[:, :, i], kernel, mode="same")
    res = np.abs(res)
    res[res < 15] = 0
    res = res.astype(np.float)
    res = 255 * (res-np.min(res)) / (np.max(res) - np.min(res))
    return res


def harrisCorner(img, filterName, ksize=3, sigma=1.0):
    # Smooth the image
    smoothImage = cv2.GaussianBlur(img, (ksize, ksize), sigma)

    # Get Filter
    filter_x, filter_y = filterFactory(filterName)

    # Calculate I_x AND I_yt
    Ix = imgConv(smoothImage, filter_x)
    Iy = imgConv(smoothImage, filter_y)

    cv2.imwrite("Ix.jpg", Ix.astype(np.uint8))
    cv2.imwrite("Iy.jpg", Iy.astype(np.uint8))

    # Calculate Ix2 and Iy2 and Ixy
    Ixx = Ix**2
    Iyy = Iy**2
    Ixy = Iy*Ix

    corner_x = []
    corner_y = []

    h = img.shape[0]
    w = img.shape[1]

    wsize = 2
    half = wsize//2

    color_img = img.copy()
    thresh = 700

    for y in range(half, h-half):
        for x in range(half, w-half):
            # Normalize sums respect number of elements in window
            Sumxx = Ixx[y-half:y+half+1, x -
                        half:x+half+1].sum() / wsize**2
            Sumxy = Ixy[y-half:y+half+1, x -
                        half:x+half+1].sum() / wsize**2
            Sumyy = Iyy[y-half:y+half+1, x -
                        half:x+half+1].sum() / wsize**2

            G = np.array([[Sumxx, Sumxy], [Sumxy, Sumyy]])

            lamdas, vector = np.linalg.eig(G)
            r = lamdas.min()

            if r > thresh:
                corner_x.append(x)
                corner_y.append(y)

    color_img[corner_y, corner_x] = (0, 255, 0)
    cv2.imwrite("corners.jpg", color_img.astype(np.uint8))
    return color_img
