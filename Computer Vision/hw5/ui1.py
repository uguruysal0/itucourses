from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.image as mpimg
from matplotlib.figure import Figure

import sys
import cv2
import os
import numpy as np
from scipy import signal
import flow_vis


class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.init_menu()
        self.init_size_name()

    def get_data(self):
        directory = "traffic_sequence"
        elems = []
        for root, dirs, files in os.walk(directory):
            files.sort()
            for file in files:
                if file.endswith(".jpg"):
                    img = cv2.imread(os.path.join(root, file))
                    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                    elems.append(img_gray)

        self.video = np.array(elems).transpose(1, 2, 0)

    def lucas_kanade(self):
        flow_video = []
        self.video = self.video / 255.
        for i in range(self.video.shape[2] - 1):
            u, v = self.optical_flow(
                self.video[..., i], self.video[..., i+1], 39)
            flow_uv = np.array([u, v]).transpose(1, 2, 0)
            flow_color = flow_vis.flow_to_color(flow_uv, convert_to_bgr=True)
            flow_video.append(flow_color)
        self.flow_video = flow_video
        self.save_video()

        self.show_flow()

    def optical_flow(self, I_1, I_2, window_size=3, threshold=1e-2):
        w, h = I_1.shape
        window_size = window_size // 2
        u, v = np.zeros((w, h)), np.zeros((w, h))
        kernel_x = np.array([[-1., 1.],
                             [-1., 1.]])

        kernel_t = np.array([[1., 1.],
                             [1., 1.]])

        # gradients respect x,y and t
        fx = signal.convolve2d(I_1, kernel_x, mode="same")
        fy = signal.convolve2d(I_1, kernel_x.T, mode="same")
        ft = signal.convolve2d(I_2, kernel_t, mode="same") - \
            signal.convolve2d(I_1, kernel_t, mode="same")

        for i in range(window_size, w-window_size):
            for j in range(window_size, h-window_size):

                Ix = fx[i-window_size:i+window_size+1, j -
                        window_size:j+window_size+1].flatten()
                Iy = fy[i-window_size:i+window_size+1, j -
                        window_size:j+window_size+1].flatten()
                It = ft[i-window_size:i+window_size +
                        1, j-window_size:j+window_size+1].flatten()

                # construct the linear equation system Ax = b
                # x = (A.T*A)-1A.T*b
                b = np.reshape(It, (It.shape[0], 1))
                A = np.vstack((Ix, Iy)).T

                if np.min(abs(np.linalg.eigvals(np.matmul(A.T, A)))) >= threshold:
                    # refactor the
                    nu = np.matmul(np.linalg.pinv(A), b)  # get velocity here
                    u[i, j] = nu[0]
                    v[i, j] = nu[1]

        return (u, v)

    def init_menu(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        impMenu = QMenu('File', self)

        self.open_input = QAction('Load  Data', self)
        self.lucas_kanade_action = QAction('Apply Lucas-Kanade', self)
        self.save_action = QAction('Save Flows', self)

        self.quit = QAction('Exit', self)

        self.open_input.triggered.connect(self.get_data)
        self.save_action.triggered.connect(self.save_video)
        self.lucas_kanade_action.triggered.connect(self.lucas_kanade)

        fileMenu.addAction(self.open_input)
        fileMenu.addAction(self.lucas_kanade_action)
        fileMenu.addAction(self.save_action)

        fileMenu.addAction(self.quit)

    def save_video(self):
        directory = "optical_flows"
        images = self.flow_video
        try:
            os.mkdir(directory)
        except:
            pass

        prefix = directory+"/"
        suffix = ".jpg"
        for i in range(len(images)):
            cv2.imwrite(prefix+str(i)+suffix, images[i])

    def show_flow(self):
        frame = 1
        for image in self.flow_video:
            cv2.imshow("Frame {}".format(frame), image)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            frame += 1

    def init_size_name(self):
        self.resize(1000, 1000)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle(
            "Question I, Optical Flow, This can be take some time")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())
