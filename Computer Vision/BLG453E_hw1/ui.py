from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.image as mpimg
from matplotlib.figure import Figure
import numpy as np
import equalizer

class UI(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
        
    def initUI(self):
        self.init_menu()
        self.init_size_name()
    
    def get_input(self):
        filename = QFileDialog.getOpenFileName(self, 'Open Input', '.')[0]
        input_image = (mpimg.imread(filename)[:,:,:3]*255).astype(np.uint8)
        self.source_histogram_equalizer = equalizer.HistogramEqualizer(input_image)
        self.source_data = self.source_histogram_equalizer.get_data("Source")

        self.input_canvas = PlotCanvas(self, width=10, height=15, data= self.source_data)
        self.input_canvas.move(50,50)

    def get_target(self):
        filename = QFileDialog.getOpenFileName(self, 'Open Input', '.')[0]
        target_image = (mpimg.imread(filename)[:,:,:3]*255).astype(np.uint8)
        self.target_histogram_equalizer = equalizer.HistogramEqualizer(target_image)
        self.target_data = self.target_histogram_equalizer.get_data("Target")

        self.target_canvas = PlotCanvas(self,width=10,height=15, data=self.target_data)
        self.target_canvas.move(700,50)
    
    def hist_match(self):
        output_image = self.target_histogram_equalizer.histogram_match(self.source_data, self.target_data)
        self.output_histogram_equalizer = equalizer.HistogramEqualizer(output_image)
        self.output_data = self.output_histogram_equalizer.get_data("Output")
        self.output = PlotCanvas(self,width=10,height=15, data=self.output_data )
        self.output.move(1350,50)
    
    def init_menu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        
        impMenu = QMenu('File', self)

        self.open_input = QAction('Open Input', self)
        self.open_target = QAction('Open Target', self) 
        self.quit = QAction('Exit', self)    
        self.equlize = QAction("Equalize", self)

        self.equlize.triggered.connect(self.hist_match)
        self.open_input.triggered.connect(self.get_input)
        self.open_target.triggered.connect(self.get_target)

        
        fileMenu.addAction(self.equlize)
        fileMenu.addAction(self.open_input)
        fileMenu.addAction(self.open_target)
        fileMenu.addAction(self.quit)



    def init_size_name(self):
        self.resize(1000, 1000)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('Histogram Equalizer')  


class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width = 5, height = 4, data=None, dpi=60):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.data = data
        self.plot()
        self.show()
 
    def plot(self):
        image  = self.figure.add_subplot(411)
        r_hist = self.figure.add_subplot(412)
        g_hist = self.figure.add_subplot(413)
        b_hist = self.figure.add_subplot(414)
        image.imshow(self.data["image"])
        
        r_hist.bar( range(256) , self.data["histograms"][0], color="red" )
        g_hist.bar( range(256) , self.data["histograms"][1], color="green" )
        b_hist.bar( range(256) , self.data["histograms"][2], color="blue" )

        image.set_title("Image {}".format(self.data["name"]))
        
        self.draw()