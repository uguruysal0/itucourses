from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.image as mpimg
from matplotlib.figure import Figure

import numpy as np
import sys
import cv2
import seg


class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.init_menu()
        self.init_size_name()

    def get_source(self):
        try:
            filename = QFileDialog.getOpenFileName(self, 'Open Input', '.')[0]
            self.img = cv2.imread(filename)
            self.input_canvas = PlotCanvas(
                self, width=10, height=15, data=self.img)
            self.input_canvas.move(50, 50)
        except ex:
            print(ex)

    def segmentation(self):
        self.segmented = seg.segmentation(self.img)

        self.result_canvas = PlotCanvas(
            self, width=10, height=15, data=self.segmented)
            
        self.result_canvas.move(750, 50)

    def init_menu(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        impMenu = QMenu('File', self)

        self.open_input = QAction('Open Input', self)
        self.segmantationAction = QAction('Do segmentation', self)
        self.quit = QAction('Exit', self)

        self.open_input.triggered.connect(self.get_source)
        self.segmantationAction.triggered.connect(self.segmentation)

        fileMenu.addAction(self.open_input)
        fileMenu.addAction(self.segmantationAction)
        fileMenu.addAction(self.quit)

    def init_size_name(self):
        self.resize(1000, 1000)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle("Question II, MR Image Segmentation")


class PlotCanvas(FigureCanvas):

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
        image = self.figure.add_subplot(111)
        image.imshow(img)
        image.set_title("Image {}".format(self.imname))
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())
