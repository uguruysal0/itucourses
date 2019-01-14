from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.text import Text
from matplotlib.image import AxesImage

from matplotlib.figure import Figure
import numpy as np
import sys
import cv2


def applyAffineTransform(src, srcTri, dstTri, size):

    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform(np.float32(srcTri), np.float32(dstTri))

    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine(src, warpMat, (size[0], size[1]), None,
                         flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)

    return dst


# Warps and alpha blends triangular regions from img1 and img2 to img
def morphTriangle(img1, img2, img, t1, t2, t, alpha):

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
    img2Rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

    size = (r[2], r[3])
    warpImage1 = applyAffineTransform(img1Rect, t1Rect, tRect, size)
    warpImage2 = applyAffineTransform(img2Rect, t2Rect, tRect, size)

    # Alpha blend rectangular patches
    imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2

    # Copy triangular region of the rectangular patch to the output image
    img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img[r[1]:r[1] +
                                              r[3], r[0]:r[0]+r[2]] * (1 - mask) + imgRect * mask


class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.init_menu()
        self.init_size_name()

    def get_source(self):
        filename = QFileDialog.getOpenFileName(self, 'Open Input', '.')[0]
        self.source = cv2.imread(filename)
        b, g, r = cv2.split(self.source)
        self.source = cv2.merge([r, g, b])
        self.source_canvas = PlotCanvas(
            self, width=5, height=4, im=self.source)
        self.source_canvas.move(50, 50)

    def get_target(self):
        filename = QFileDialog.getOpenFileName(self, 'Open Target', '.')[0]
        self.target = cv2.imread(filename)
        b, g, r = cv2.split(self.target)
        self.target = cv2.merge([r, g, b])

        self.target_canvas = PlotCanvas(
            self, width=5, height=4, im=self.target)
        self.target_canvas.move(800, 50)

    def morph(self):

        src_pts_x, src_pts_y = self.source_canvas.getPoints()
        target_pts_x, target_pts_y = self.target_canvas.getPoints()

        self.morph_im = np.zeros(self.source.shape, dtype=self.source.dtype)

        print(f"Number of points {len(src_pts_x)} {len(target_pts_x)}")

        points = []
        alpha = 0.5
        # Compute weighted average point coordinates
        for i in range(0, len(src_pts_x)):
            x = (1 - alpha) * src_pts_x[i] + alpha * target_pts_x[i]
            y = (1 - alpha) * src_pts_y[i] + alpha * target_pts_y[i]
            points.append((x, y))

        rect = (0, 0, self.source.shape[1], self.source.shape[0])

        subdiv_src = cv2.Subdiv2D(rect)
        subdiv_target = cv2.Subdiv2D(rect)
        subdiv_morph = cv2.Subdiv2D(rect)

        for i in range(len(src_pts_x)):
            subdiv_src.insert((src_pts_x[i], src_pts_y[i]))

        for i in range(len(target_pts_x)):
            subdiv_target.insert((target_pts_x[i], target_pts_y[i]))

        for point in points:
            subdiv_morph.insert(point)

        triangles_src = subdiv_src.getTriangleList()
        triangles_target = subdiv_target.getTriangleList()
        triangles_morph = subdiv_morph.getTriangleList()

        print(triangles_src)
        print(triangles_target)
        print(triangles_morph)

        for i in range(len(triangles_src)):
            tr1 = [[triangles_src[i][0], triangles_src[i][1]], [
                triangles_src[i][2], triangles_src[i][3]], [triangles_src[i][4], triangles_src[i][5]]]

            tr2 = [[triangles_target[i][0], triangles_target[i][1]], [
                triangles_target[i][2], triangles_target[i][3]], [triangles_target[i][4], triangles_target[i][5]]]

            tr3 = [[triangles_morph[i][0], triangles_morph[i][1]], [
                triangles_morph[i][2], triangles_morph[i][3]], [triangles_morph[i][4], triangles_morph[i][5]]]

            morphTriangle(
                self.source, self.target, self.morph_im, tr1, tr2, tr3, alpha)

        self.morph_canvas = PlotCanvas(
            self, width=5, height=4, im=self.morph_im)
        cv2.imwrite('moprhed.jpg', self.morph_im)
        self.morph_canvas.move(1300, 50)

    def init_menu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        impMenu = QMenu('File', self)

        self.open_input = QAction('Open Input', self)
        self.open_target = QAction('Open Target', self)
        self.morph_action = QAction('Morph', self)
        self.quit = QAction('Exit', self)

        self.open_input.triggered.connect(self.get_source)
        self.open_target.triggered.connect(self.get_target)
        self.morph_action.triggered.connect(self.morph)

        fileMenu.addAction(self.open_input)
        fileMenu.addAction(self.open_target)
        fileMenu.addAction(self.morph_action)
        fileMenu.addAction(self.quit)

    def init_size_name(self):
        self.resize(1000, 1000)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('Face Moprhing')


class PlotCanvas(FigureCanvas):

    def onpick(self, event):
        x = None
        y = None
        if len(self.points_x) == 0:
            self.top_left_x = int(event.x)
            self.top_left_y = int(event.y)
            x = 0
            y = 0
        if len(self.points_x) == 1:
            self.bottom_right_x = int(event.x)
            self.bottom_right_y = int(event.y)
            x = self.im.shape[0]-5
            y = self.im.shape[1]-5
        else:
            x = int(event.x) - self.top_left_x
            y = (y+self.im.shape[1]) % 

        '''
        first point is bottom left corner points are selected from reverse image 
        '''

        print(event.x, event.y,  sep=' ')
        self.points_x.append(x)
        self.points_y.append(y)

        # print(self.points_x[-1], self.points_y[-1], sep=" ")

        self.pickPoint(self.points_x[-1], self.points_y[-1])

        self.plot()

    def __init__(self, parent=None, width=5, height=4, im=None, dpi=120):

        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)

        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.points_x = []
        self.points_y = []

        self.bottom_left_x = None
        self.bottom_left_y = None

        self.im = im

        fig.canvas.mpl_connect('button_press_event', self.onpick)
        self.plot()
        self.show()

    def plot(self):
        self.figure.clear()

        canvas = self.figure.add_subplot(111)
        canvas.imshow(np.uint8(self.im), origin="upper", extent=(
            0, self.im.shape[1], 0,  self.im.shape[0]))

        self.draw()

    def getPoints(self):
        return self.points_x, self.points_y

    def pickPoint(self, X, Y):
        for i in range(7):
            for j in range(7):
                try:
                    self.im[X+i][Y+j][0] = 255
                    self.im[X+i][Y+j][1] = 0
                    self.im[X+i][Y+j][2] = 0
                except:
                    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())
