from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from copy import deepcopy
import sys
import cv2
import numpy as np
from PIL import Image

srcfilename = 'Bush.jpg'
targetfilename = 'Arnie.jpg'

# Code taken from https://www.learnopencv.com/face-morph-using-opencv-cpp-python/

def rect_contains(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[2]:
        return False
    elif point[1] > rect[3]:
        return False
    return True

def draw_point(img, p, color):
    cv2.circle(img, p, 2, color, cv2.cv.CV_FILLED, cv2.CV_AA, 0)

def draw_delaunay(img, subdiv, delaunay_color):
    triangleList = subdiv.getTriangleList()
    size = img.shape
    r = (0, 0, size[1], size[0])

    for t in triangleList:

        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3):

            cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)



def estimate_affine_transform(src, dest):
    # Solve the least squares problem X * A = Y
    pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))])
    x = pad(src)
    y = pad(dest)

    A = np.linalg.lstsq(x, y)[0]
    return A


# Change dest and src to get invese transform 
# This version get transform matrix 
def get_transform(dest, src):
    # Create Ax=b linear equation then 
    # take inverse of A and x will be  A{inverse} b
    # if we change the parameter order ot would give inverse transform 
    A = np.array([ [dest[0][0], dest[0][1], 1, 0, 0, 0],
                   [dest[1][0], dest[1][1], 1, 0, 0, 0],
                   [dest[2][0], dest[2][1], 1, 0, 0, 0],
                   [0, 0, 0, dest[0][0], dest[0][1], 1],
                   [0, 0, 0, dest[1][0], dest[1][1], 1],
                   [0, 0, 0, dest[2][0], dest[2][1], 1]] )
    b = np.array([ src[0][0], src[1][0], src[2][0], src[0][1], src[1][1], src[2][1]]).T
    
    x = np.linalg.lstsq(A, b)[0]
    
    transform = np.array( [ [x[0], x[1], x[2] ],
                          [ x[3],  x[4], x[5] ]] )
    
    # opencv WARPAFFINE take 2x3 matrix 
    return transform

def applyAffineTransform(src, srcTri, dstTri, size):

    warpMat = get_transform(np.float32(srcTri), np.float32(dstTri))
    # print(warpMat)
    #warpMat = cv2.getAffineTransform(np.float32(srcTri), np.float32(dstTri))
    """
    This code is for warping image with nearest neighboor but it does not work as I expected
    I used opencv function to warp 
    newIm = np.zeros(src.shape)
    for i in range(newIm.shape[0]):
        for j in range(newIm.shape[1]):
            backward_point = np.dot(warpMat, np.array([ i, j , 1]))
            x,y = round(backward_point[0]),round(backward_point[1])
            try:
                newIm[x][y]=src[x][y]
            except:
                pass
    
    After interpolating resize operation is required
    
    pil_im = Image.fromarray(newIm.astype(np.uint8))
    pil_im = pil_im.resize((size[0], size[1]))
    newIm = np.asarray(pil_im)
    """
    
    dst = cv2.warpAffine(src, warpMat, (size[0], size[1]), None,
                         flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return dst

# Code taken from Code taken from https://www.learnopencv.com/face-morph-using-opencv-cpp-python/
def morphTriangle(img1, img, t1, t2, t):
    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    r = cv2.boundingRect(np.float32([t]))

    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    tRect = []

    for i in range(0, 3):
        tRect.append(((t[i][0] - r[0]), (t[i][1] - r[1])))
        t1Rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))

    # Get mask by filling triangle
    mask = np.zeros((r[3], r[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0), 16, 0)

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]

    size = (r[2], r[3])
    warpImage = applyAffineTransform(img1Rect, t1Rect, tRect, size)
    # Alpha blend rectangular patches
    # Copy triangular region of the rectangular patch to the output image
    
    img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] = img[r[1]:r[1] +
                                                  r[3], r[0]:r[0] + r[2]] * (1 - mask) + warpImage * mask

class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.init_size_name()
        self.init_menu()

        src_pixmap = QPixmap(srcfilename)
        self.source_label = QLabel(self)
        self.source_label.setPixmap(src_pixmap)
        self.source_label.resize(src_pixmap.width(), src_pixmap.height())
        self.source_label.mousePressEvent = self.getPixelSrc
        self.source_label.move(50, 50)
        self.src = cv2.imread(srcfilename)
        
        target_pixmap = QPixmap(targetfilename)
        self.target_label = QLabel(self)
        self.target_label.setPixmap(target_pixmap)
        self.target_label.resize(target_pixmap.width(), target_pixmap.height())
        self.target_label.mousePressEvent = self.getPixelTarget
        self.target_label.move(500, 50)
        self.target = cv2.imread(targetfilename)
        self.src_points = []
        self.target_points = []


    def init_size_name(self):
        self.resize(1000, 1000)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('Face Moprhing')


    def init_menu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        impMenu = QMenu('File', self)
        self.morph_action = QAction('Morph', self)
        self.quit = QAction('Exit', self)
        self.morph_action.triggered.connect(self.morph)
        fileMenu.addAction(self.morph_action)
        fileMenu.addAction(self.quit)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())
