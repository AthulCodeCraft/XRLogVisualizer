import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
import pyqtgraph as pg
#import QBrush
from PyQt5.QtGui import QBrush

#import QFont
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QDrag
from PyQt5.QtCore import QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QLabel, QApplication
class FPS(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # create plot widget
        self.plot = pg.PlotWidget()
        self.plot.setBackground('w')  # set background color to white
        self.plot.setLabel('left', 'Y Axis Label')
        self.plot.setLabel('bottom', 'X Axis Label')
        # set font for axis labels
        font = QFont('Calibri', 11, QFont.Bold)
        self.plot.getAxis('bottom').setTickFont(font)
        self.plot.getAxis('left').setTickFont(font)

        self.plot.getAxis('bottom').setLabel(text='Timestamp', font=font, color='k')
        self.plot.getAxis('left').setLabel(text='FPS', font=font, color='k')
        # set line color and marker color for plotted data
        self.pen = pg.mkPen(color=(0, 112, 192), width=5)  # red line with width of 2
        self.brush = pg.mkBrush(color=(0, 112, 192))  # blue marker
        # create button to plot data
        self.plot_button = QPushButton('Plot Data')
        self.plot_button.clicked.connect(self.plot_data)
        # add plot widget and button to layout
        layout = QHBoxLayout()
        layout.addWidget(self.plot)
        layout.addWidget(self.plot_button)
        self.setLayout(layout)



    def plot_data(self):
        # clear existing plot data
        self.plot.clear()
        file_data = self.parent.parent.parent.log_read_object

        file_data.read_file_execute(self.parent.parent.parent.file_loaded_to_gui)
        file_data.read_file_execute_fps()
        self.x_data = file_data.timestamp_list
        self.y_data = file_data.fps_list

        if not (len(self.y_data)) == 0:
            # add data to plot
            self.plot.addLegend()
            self.plot.plot(self.x_data, self.y_data, pen=self.pen, brush=self.brush, name='FPS')
            # set fixed limits on x and y axes

            self.plot.setLimits(xMin=self.x_data[0], xMax=self.x_data[-1], yMin=0, yMax=100 )
            font = QFont('Calibri', 10, QFont.Bold)
            self.legend.setStyle(font=font, textColor='k')
            #self.plot.setMouseEnabled(x=False, y=False)
            #set plot to display as an image (no scrollbars)``

class FPS_panel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.fps_panel = FPS(self)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.fps_panel)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

class Encoder(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # create plot widget
        self.plot = pg.PlotWidget()
        self.plot.setLabel('left', 'Y Axis Label')
        self.plot.setLabel('bottom', 'X Axis Label')
        # create button to plot data
        self.plot_button = QPushButton('Plot Data')
        self.plot_button.clicked.connect(self.plot_data)
        # add plot widget and button to layout
        layout = QHBoxLayout()
        layout.addWidget(self.plot)
        layout.addWidget(self.plot_button)
        self.setLayout(layout)

    def plot_data(self):
        # clear existing plot data
        self.plot.clear()
        file_data = self.parent.parent.parent.log_read_object

        file_data.read_file_execute(self.parent.parent.parent.file_loaded_to_gui)
        file_data.read_file_execute_batterylevel()
        self.x_data = file_data.timestamp_list
        self.y_data = file_data.battery_level_list

        if len(self.y_data) == 0:
            # add a text item to the plot if y_data is empty
            pass


        else:
            # add data to plot
            self.plot.plot(self.x_data, self.y_data)
            # set fixed limits on x and y axes
            self.plot.setLimits(xMin=self.x_data[0], xMax=self.x_data[-1], yMin=0, yMax=200)
            # self.plot.setMouseEnabled(x=False, y=False)
            # set plot to display as an image (no scrollbars)


class Encoder_panel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.encoder_panel = Encoder(self)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.encoder_panel)
        vbox.addLayout(hbox)
        self.setLayout(vbox)


class Decoder(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # create plot widget
        self.plot = pg.PlotWidget()
        self.plot.setLabel('left', 'Y Axis Label')
        self.plot.setLabel('bottom', 'X Axis Label')
        # create button to plot data
        self.plot_button = QPushButton('Plot Data')
        self.plot_button.clicked.connect(self.plot_data)
        # add plot widget and button to layout
        layout = QHBoxLayout()
        layout.addWidget(self.plot)
        layout.addWidget(self.plot_button)
        self.setLayout(layout)

    def plot_data(self):
        # clear existing plot data
        self.plot.clear()
        file_data = self.parent.parent.parent.log_read_object

        file_data.read_file_execute(self.parent.parent.parent.file_loaded_to_gui)
        file_data.read_file_execute_batterylevel()
        self.x_data = file_data.timestamp_list
        self.y_data = file_data.battery_level_list

        if len(self.y_data) == 0:
            # add a text item to the plot if y_data is empty
            pass


        else:
            # add data to plot
            self.plot.plot(self.x_data, self.y_data)
            # set fixed limits on x and y axes
            self.plot.setLimits(xMin=self.x_data[0], xMax=self.x_data[-1], yMin=0, yMax=200)
            # self.plot.setMouseEnabled(x=False, y=False)
            # set plot to display as an image (no scrollbars)


class Decoder_panel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.decoder_panel = Decoder(self)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.decoder_panel)
        vbox.addLayout(hbox)
        self.setLayout(vbox)


class Multimedia_tab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        multimedia_tab_widget = QTabWidget()
        self.setStyleSheet("QTabBar::tab { height: 30px; }")
        multimedia_tab_widget.setTabPosition(QTabWidget.North)

        ####################################Add the panels here###################################################
        multimedia_tab_widget.addTab(FPS_panel(self), "FPS")
        multimedia_tab_widget.addTab(Decoder_panel(self), "Decoder")
        multimedia_tab_widget.addTab(Encoder_panel(self), "Encoder")
        ##########################################################################################################

        main_layout = QVBoxLayout()
        main_layout.addWidget(multimedia_tab_widget)
        self.setLayout(main_layout)


