from PyQt5.QtWidgets import *
from functools import wraps
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from scipy.signal import convolve2d as cn2
from scipy.misc import imsave
from gtransform import *
from PIL import Image
import matplotlib.image as mpimg


class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.image = None
        self.initUI()
        self.show()

    def initUI(self):
        self.init_menu()
        self.setWindowTitle('Filtering & Geometric Transforms')
        self.init_size()

    def open_image(self):
        filename = QFileDialog.getOpenFileName(self, 'Open Input', '.')[0]
        self.image = Image.open(filename)
        self.image.load()
        self.image = np.asarray(self.image)[:, :, :3]
        self.image = self.image.astype(np.uint8)
        self.input_canvas = PlotCanvas(
            self, width=5, height=4, data=self.image)
        self.input_canvas.move(850, 250)

    def save_image(self):
        try:
            imsave('output.jpg', self.image)
        except:
            pass

    def init_size(self):
        self.resize(1000, 1000)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_menu(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        filtersMenu = menubar.addMenu('&Filters')

        geometricTransforms = menubar.addMenu('Geometric Transforms')

        open_image = QAction('Open', self)
        save_image_action = QAction('Save', self)
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit')

        fileMenu.addAction(open_image)
        fileMenu.addAction(exitAct)
        fileMenu.addAction(save_image_action)

        open_image.triggered.connect(self.open_image)
        save_image_action.triggered.connect(self.save_image)
        exitAct.triggered.connect(qApp.quit)

        avg_filter_menu = filtersMenu.addMenu('Avarage Filters')
        gaussian_filter_menu = filtersMenu.addMenu('Gaussian Filters')
        median_filter_menu = filtersMenu.addMenu('Median Filters')

        for i in range(3, 16, 2):
            avg_filter_menu.addAction(self.createAction(
                avg_filter_menu, i, "a"))

        for i in range(3, 16, 2):
            gaussian_filter_menu.addAction(self.createAction(
                gaussian_filter_menu, i, "g"))

        for i in range(3, 16, 2):
            median_filter_menu.addAction(self.createAction(
                median_filter_menu, i, "m"))

        rotate_menu = geometricTransforms.addMenu('Rotae')
        scale_menu = geometricTransforms.addMenu('Scale')
        translate_menu = geometricTransforms.addMenu('Translate')

        rotate_10_right = QAction('Rotate 10 Degree Right', rotate_menu)
        rotate_menu.addAction(rotate_10_right)
        rotate_10_left = QAction('Rotate 10 Degree Left', rotate_menu)
        rotate_menu.addAction(rotate_10_left)

        scale_2x = QAction('2x', scale_menu)
        scale_half = QAction('1/2x', scale_menu)
        scale_menu.addAction(scale_2x)
        scale_menu.addAction(scale_half)
        translate_left = QAction('Left', translate_menu)
        translate_right = QAction('Right', translate_menu)
        translate_menu.addAction(translate_left)
        translate_menu.addAction(translate_right)
        rotate_10_right.triggered.connect(self.rotate_10_right)
        rotate_10_left.triggered.connect(self.rotate_10_left)
        scale_2x.triggered.connect(self.scale_2x)
        scale_half.triggered.connect(self.scale_half)

    def createAction(self, parent, size, type):
        action = QAction('{}x{}'.format(size, size), parent)
        action.triggered.connect(self.filter_factory(type, size))
        return action

    def avarage_filter(self, kernel_size):
        kernel = np.array([[1/(kernel_size**2)]*kernel_size]*kernel_size)

        ch_1 = cn2(self.image[..., 0], kernel, "same")
        ch_2 = cn2(self.image[..., 1], kernel, "same")
        ch_3 = cn2(self.image[..., 2], kernel, "same")
        self.image = np.dstack((ch_1, ch_2, ch_3)).astype(np.uint8)
        self.input_canvas.plot(self.image)

    def avarage_filter_3(self):
        return self.avarage_filter(3)

    def avarage_filter_5(self):
        return self.avarage_filter(5)

    def avarage_filter_7(self):
        return self.avarage_filter(7)

    def avarage_filter_9(self):
        return self.avarage_filter(9)

    def avarage_filter_11(self):
        return self.avarage_filter(11)

    def avarage_filter_13(self):
        return self.avarage_filter(13)

    def avarage_filter_15(self):
        return self.avarage_filter(15)

    def gaussian_filter(self, kernel_size):
        m, n = int((kernel_size-1.)/2), int((kernel_size-1.)/2)
        y, x = np.array([i for i in range(-m, m+1)]
                        ), np.array([i for i in range(-n, n+1)])
        y = y.reshape(-1, 1)
        x = x.reshape(-1, 1).T
        kernel = np.exp(-(x*x + y*y) / (2))
        kernel[kernel < 1e-5 * kernel.max()] = 0
        sumh = kernel.sum()
        if sumh != 0:
            kernel /= sumh

        ch_1 = cn2(self.image[..., 0], kernel, "same")
        ch_2 = cn2(self.image[..., 1], kernel, "same")
        ch_3 = cn2(self.image[..., 2], kernel, "same")
        self.image = np.dstack((ch_1, ch_2, ch_3)).astype(np.uint8)
        self.input_canvas.plot(self.image)

    def gaussian_filter_3(self):
        return self.gaussian_filter(3)

    def gaussian_filter_5(self):
        return self.gaussian_filter(5)

    def gaussian_filter_7(self):
        return self.gaussian_filter(7)

    def gaussian_filter_9(self):
        return self.gaussian_filter(9)

    def gaussian_filter_11(self):
        return self.gaussian_filter(11)

    def gaussian_filter_13(self):
        return self.gaussian_filter(13)

    def gaussian_filter_15(self):
        return self.gaussian_filter(15)

    def median_filter(self, kernel_size):

        ch_1 = self.image[..., 0]
        ch_2 = self.image[..., 1]
        ch_3 = self.image[..., 2]

        nch_1 = np.ones(ch_1.shape)
        nch_2 = np.ones(ch_1.shape)
        nch_3 = np.ones(ch_1.shape)

        for i in range(ch_1.shape[0]):
            for j in range(ch_1.shape[1]):
                elems = []
                for r in range(kernel_size):
                    for l in range(kernel_size):
                        try:
                            elems.append(ch_1[i+r][j+l])
                        except:
                            pass
                elems.sort()
                nch_1[i][j] = elems[len(elems)//2]

        for i in range(ch_1.shape[0]):
            for j in range(ch_1.shape[1]):
                elems = []
                for r in range(kernel_size):
                    for l in range(kernel_size):
                        try:
                            elems.append(ch_2[i+r][j+l])
                        except:
                            pass
                elems.sort()
                nch_2[i][j] = elems[len(elems)//2]

        for i in range(ch_1.shape[0]):
            for j in range(ch_1.shape[1]):
                elems = []
                for r in range(kernel_size):
                    for l in range(kernel_size):
                        try:
                            elems.append(ch_3[i+r][j+l])
                        except:
                            pass
                elems.sort()
                nch_3[i][j] = elems[len(elems)//2]

        self.image = np.dstack((nch_1, nch_2, nch_3)).astype(np.uint8)
        self.input_canvas.plot(self.image)
        self.input_canvas.move(850, 250)

    def median_filter_3(self):
        return self.median_filter(3)

    def median_filter_5(self):
        return self.median_filter(5)

    def median_filter_7(self):
        return self.median_filter(7)

    def median_filter_9(self):
        return self.median_filter(9)

    def median_filter_11(self):
        return self.median_filter(11)

    def median_filter_13(self):
        return self.median_filter(13)

    def median_filter_15(self):
        return self.median_filter(15)

    def filter_factory(self, type, s):
        if type == "a":
            if s == 3:
                return self.avarage_filter_3
            if s == 5:
                return self.avarage_filter_5
            if s == 7:
                return self.avarage_filter_7
            if s == 9:
                return self.avarage_filter_9
            if s == 11:
                return self.avarage_filter_11
            if s == 13:
                return self.avarage_filter_13
            if s == 15:
                return self.avarage_filter_15
        if type == "g":
            if s == 3:
                return self.gaussian_filter_3
            if s == 5:
                return self.gaussian_filter_5
            if s == 7:
                return self.gaussian_filter_7
            if s == 9:
                return self.gaussian_filter_9
            if s == 11:
                return self.gaussian_filter_11
            if s == 13:
                return self.gaussian_filter_13
            if s == 15:
                return self.gaussian_filter_15
        if type == "m":
            if s == 3:
                return self.median_filter_3
            if s == 5:
                return self.median_filter_5
            if s == 7:
                return self.median_filter_7
            if s == 9:
                return self.median_filter_9
            if s == 11:
                return self.median_filter_11
            if s == 13:
                return self.median_filter_13
            if s == 15:
                return self.median_filter_15

    def translate_right(self):
        pass

    def translate_left(self):
        pass

    def rotate_10_right(self):
        trans_matrix = np.array([[np.cos(np.pi/18), -np.sin(np.pi/18), 0],
                                 [np.sin(np.pi/18), np.cos(np.pi/18), 0],
                                 [0, 0, 1]])
        self.image = backward_mapping(self.image, trans_matrix)
        self.input_canvas.plot(self.image)

    def rotate_10_left(self):
        trans_matrix = np.array([[np.cos(-np.pi/18), -np.sin(-np.pi/18), 0],
                                 [np.sin(-np.pi/18), np.cos(-np.pi/18), 0],
                                 [0, 0, 1]])
        self.image = backward_mapping(self.image, trans_matrix)
        self.input_canvas.plot(self.image)

    def scale_2x(self):
        trans_matrix = np.array([[2, 0, 0],
                                 [0, 2, 0],
                                 [0, 0, 1]])
        self.image = backward_mapping(self.image, trans_matrix, scale=1)
        self.input_canvas.plot(self.image)

    def scale_half(self):
        trans_matrix = np.array([[0.5, 0, 0],
                                 [0, 0.5, 0],
                                 [0, 0, 1]])
        self.image = backward_mapping(self.image, trans_matrix, scale=1)
        self.input_canvas.plot(self.image)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, data=None, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)

        FigureCanvas.updateGeometry(self)
        self.plot(data)
        self.show()

    def plot(self, data):
        self.figure.clear()
        image = self.figure.add_subplot(111)
        image.imshow(data)
        self.draw()
