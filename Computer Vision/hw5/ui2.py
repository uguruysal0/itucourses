from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.image as mpimg
from matplotlib.figure import Figure

import cv2
import numpy as np
import sys
import os
import q2


class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.init_menu()
        self.init_size_name()

    def get_data(self):
        elems = []
        directory = "Face_database"
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".tif"):
                    img = cv2.imread(os.path.join(root, file))
                    self.R = img.shape[0]
                    self.C = img.shape[1]
                    elems.append(img.flatten())

        self.data = np.array(elems)
        self.centered_data, self.mean = q2.normalize(self.data)
        self.eigfaces = q2.eigen_faces(self.centered_data, self.R, self.C)

    def show_eigen_faces(self):
        self.eigen_canvas = EiegenCanvas(
            self, width=10, height=15, data=self.eigfaces)

        self.eigen_canvas.move(750, 50)

    def show_mean(self):
        self.mean_canvas = MeanCanvas(
            self, width=10, height=15, data=self.mean)

        self.mean_canvas.move(50, 50)

    def init_menu(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        impMenu = QMenu('File', self)

        self.load_data = QAction('Load Data', self)
        self.show_eigen_faces_action = QAction('Show Eigen Faces', self)
        self.show_mean_face = QAction('Show Mean Face', self)
        self.quit = QAction('Exit', self)

        self.load_data.triggered.connect(self.get_data)
        self.show_eigen_faces_action.triggered.connect(self.show_eigen_faces)
        self.show_mean_face.triggered.connect(self.show_mean)

        fileMenu.addAction(self.load_data)
        fileMenu.addAction(self.show_eigen_faces_action)
        fileMenu.addAction(self.show_mean_face)
        fileMenu.addAction(self.quit)

    def init_size_name(self):
        self.resize(1000, 1000)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle("Question II, Eigenfaces")


class MeanCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, data=None, dpi=60, imname=""):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.imname = imname
        self.data = data
        self.plot(self.data)
        self.show()

    def plot(self, img):
        self.figure.clear()
        print(img.shape)
        image = self.figure.add_subplot(111)
        image.imshow(img)
        image.set_title("Mean Image ".format(self.imname))
        self.draw()


class EiegenCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, data=None, dpi=60, imname=""):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.imname = imname
        self.data = data
        self.plot(self.data)
        self.show()

    def plot(self, imgs):
        self.figure.clear()

        image1 = self.figure.add_subplot(511)
        image2 = self.figure.add_subplot(512)
        image3 = self.figure.add_subplot(513)
        image4 = self.figure.add_subplot(514)
        image5 = self.figure.add_subplot(515)

        image1.imshow(imgs[0])
        image2.imshow(imgs[1])
        image3.imshow(imgs[2])
        image4.imshow(imgs[3])
        image5.imshow(imgs[4])

        image1.set_title("Top 1 Eigen Face")
        image2.set_title("Top 2 Eigen Face")
        image3.set_title("Top 3 Eigen Face")
        image4.set_title("Top 4 Eigen Face")
        image5.set_title("Top 5 Eigen Face")

        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())
