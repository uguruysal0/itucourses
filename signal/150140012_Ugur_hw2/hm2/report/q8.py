import numpy as np
from scipy.signal import convolve2d as cn2 
from scipy.misc import imread, imsave
kernel = np.array([[1/9]*3]*3)
base = imread("noisyCameraman.png")[:,:,0]
last = cn2(base, kernel, "same")
imsave('last.png', last)