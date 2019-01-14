import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy import interpolate
import sympy as syp
import pandas as pd
pd.options.display.max_colwidth = 200
%matplotlib inline

def bicubic_interpolation(xi, yi, zi, xnew, ynew):

    # check sorting
    if np.any(np.diff(xi) < 0) and np.any(np.diff(yi) < 0) and\
    np.any(np.diff(xnew) < 0) and np.any(np.diff(ynew) < 0):
        raise ValueError('data are not sorted')

    if zi.shape != (xi.size, yi.size):
        raise ValueError('zi is not set properly use np.meshgrid(xi, yi)')

    z = np.zeros((xnew.size, ynew.size))

    deltax = xi[1] - xi[0]
    deltay = yi[1] - yi[0] 
    for n, x in enumerate(xnew):
        for m, y in enumerate(ynew):

            if xi.min() <= x <= xi.max() and yi.min() <= y <= yi.max():

                i = np.searchsorted(xi, x) - 1
                j = np.searchsorted(yi, y) - 1

                x0  = xi[i-1]
                x1  = xi[i]
                x2  = xi[i+1]
                x3  = x1+2*deltax

                y0  = yi[j-1]
                y1  = yi[j]
                y2  = yi[j+1]
                y3  = y1+2*deltay

                px = (x-x1)/(x2-x1)
                py = (y-y1)/(y2-y1)

                f00 = zi[i-1, j-1]      #row0 col0 >> x0,y0
                f01 = zi[i-1, j]        #row0 col1 >> x1,y0
                f02 = zi[i-1, j+1]      #row0 col2 >> x2,y0

                f10 = zi[i, j-1]        #row1 col0 >> x0,y1
                f11 = p00 = zi[i, j]    #row1 col1 >> x1,y1
                f12 = p01 = zi[i, j+1]  #row1 col2 >> x2,y1

                f20 = zi[i+1,j-1]       #row2 col0 >> x0,y2
                f21 = p10 = zi[i+1,j]   #row2 col1 >> x1,y2
                f22 = p11 = zi[i+1,j+1] #row2 col2 >> x2,y2

                if 0 < i < xi.size-2 and 0 < j < yi.size-2:

                    f03 = zi[i-1, j+2]      #row0 col3 >> x3,y0

                    f13 = zi[i,j+2]         #row1 col3 >> x3,y1

                    f23 = zi[i+1,j+2]       #row2 col3 >> x3,y2

                    f30 = zi[i+2,j-1]       #row3 col0 >> x0,y3
                    f31 = zi[i+2,j]         #row3 col1 >> x1,y3
                    f32 = zi[i+2,j+1]       #row3 col2 >> x2,y3
                    f33 = zi[i+2,j+2]       #row3 col3 >> x3,y3

                elif i<=0: 

                    f03 = f02               #row0 col3 >> x3,y0

                    f13 = f12               #row1 col3 >> x3,y1

                    f23 = f22               #row2 col3 >> x3,y2

                    f30 = zi[i+2,j-1]       #row3 col0 >> x0,y3
                    f31 = zi[i+2,j]         #row3 col1 >> x1,y3
                    f32 = zi[i+2,j+1]       #row3 col2 >> x2,y3
                    f33 = f32               #row3 col3 >> x3,y3             

                elif j<=0:

                    f03 = zi[i-1, j+2]      #row0 col3 >> x3,y0

                    f13 = zi[i,j+2]         #row1 col3 >> x3,y1

                    f23 = zi[i+1,j+2]       #row2 col3 >> x3,y2

                    f30 = f20               #row3 col0 >> x0,y3
                    f31 = f21               #row3 col1 >> x1,y3
                    f32 = f22               #row3 col2 >> x2,y3
                    f33 = f23               #row3 col3 >> x3,y3


                elif i == xi.size-2 or j == yi.size-2:

                    f03 = f02               #row0 col3 >> x3,y0

                    f13 = f12               #row1 col3 >> x3,y1

                    f23 = f22               #row2 col3 >> x3,y2

                    f30 = f20               #row3 col0 >> x0,y3
                    f31 = f21               #row3 col1 >> x1,y3
                    f32 = f22               #row3 col2 >> x2,y3
                    f33 = f23               #row3 col3 >> x3,y3

                px00 = (f12 - f10)/2*deltax
                px01 = (f22 - f20)/2*deltax 
                px10 = (f13 - f11)/2*deltax 
                px11 = (f23 - f21)/2*deltax

                py00 = (f21 - f01)/2*deltay
                py01 = (f22 - f02)/2*deltay
                py10 = (f31 - f11)/2*deltay
                py11 = (f32 - f12)/2*deltay

                pxy00 = ((f22-f20) - (f02-f00))/4*deltax*deltay
                pxy01 = ((f32-f30) - (f12-f10))/4*deltax*deltay
                pxy10 = ((f23-f21) - (f03-f01))/4*deltax*deltay
                pxy11 = ((f33-f31) - (f13-f11))/4*deltax*deltay


                f = np.array([p00,  p01,  p10, p11,
                              px00,  px01,  px10, px11,
                              py00, py01,  py10,  py11,
                              pxy00,  pxy01, pxy10, pxy11])

                a = A@f

                a = a.reshape(4,4).transpose()
                z[n,m] = np.array([1, px, px**2, px**3]) @ a @ np.array([1, py, py**2, py**3])

    return z


    def f(x,y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

x = np.linspace(-6, 6, 11)
y = np.linspace(-6, 6, 11)

xx, yy = np.meshgrid(x, y)

z = f(xx, yy)

x_new = np.linspace(-6, 6, 100)
y_new = np.linspace(-6, 6, 100)

xx_new, yy_new = np.meshgrid(x_new, y_new)

z_new = bicubic_interpolation(x, y, z, x_new, y_new)

z_true = f(xx_new, yy_new) 

f_scipy = interpolate.interp2d(x, y, z, kind='cubic')

z_scipy = f_scipy(x_new, y_new)

fig, ax = plt.subplots(2, 2, sharey=True, figsize=(16,12))

img0 = ax[0, 0].scatter(xx, yy, c=z, s=100)
ax[0, 0].set_title('original points')
fig.colorbar(img0, ax=ax[0, 0], orientation='vertical', shrink=1, pad=0.01)

img1 = ax[0, 1].imshow(z_new, vmin=z_new.min(), vmax=z_new.max(), origin='lower',
           extent=[x_new.min(), x_new.max(), y_new.max(), y_new.min()])
ax[0, 1].set_title('bicubic our code')
fig.colorbar(img1, ax=ax[0, 1], orientation='vertical', shrink=1, pad=0.01)


img2 = ax[1, 0].imshow(z_scipy, vmin=z_scipy.min(), vmax=z_scipy.max(), origin='lower',
           extent=[x_new.min(), x_new.max(), y_new.max(), y_new.min()])
ax[1, 0].set_title('bicubic scipy')
fig.colorbar(img2, ax=ax[1, 0], orientation='vertical', shrink=1, pad=0.01)


img3 = ax[1, 1].imshow(z_true, vmin=z_true.min(), vmax=z_true.max(), origin='lower',
           extent=[x_new.min(), x_new.max(), y_new.max(), y_new.min()])
ax[1, 1].set_title('true model')
fig.colorbar(img3, ax=ax[1, 1], orientation='vertical', shrink=1, pad=0.01)

plt.subplots_adjust(wspace=0.05, hspace=0.15)

plt.show()