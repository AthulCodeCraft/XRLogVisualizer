import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
import pyqtgraph as pg
from PyQt5.QtGui import QDrag
from PyQt5.QtCore import QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QLabel, QApplication
import numpy as np
import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QMainWindow, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation
import datetime as dt
class Headpose(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        file_data = self.parent.parent.parent.log_read_object
        self.hbox = QVBoxLayout()

        layout = QHBoxLayout()

        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvas(self.fig)
        self.x = []
        self.y = []
        self.z = []
        self.timestamps = []
        # Animate the plot widget
        self.plot_widget = QTabWidget()

        self.plot_button = QPushButton('Plot Data')
        #set the size
        self.plot_button.setFixedWidth(100)


        self.messagebox = QLabel('No data to plot')
        #font colur should be red
        self.messagebox.setFixedWidth(100)
        self.messagebox.setFixedHeight(20)

        self.messagebox.setStyleSheet("QLabel { color : red; }")
        #add width for hbox
        self.hbox.setContentsMargins(5, 0, 0, 0)
        self.messagebox.hide()
        self.hbox.addWidget(self.plot_button)
        self.hbox.addWidget(self.messagebox)
        self.hbox.setAlignment(Qt.AlignVCenter)

        self.plot_button.clicked.connect(self.plot_data)
        layout.addWidget(self.canvas)
        layout.addLayout(self.hbox)
        self.setLayout(layout)
        self.animation = FuncAnimation(self.fig, self.animate,frames=0, interval=10)
    def add_data(self, x_list, y_list, z_list, timestamps_list):
        self.x.extend(x_list)
        self.y.extend(y_list)
        self.z.extend(z_list)
        self.timestamps.extend(timestamps_list)


        

    def animate(self, i):

        if i >= len(self.timestamps) - 1:
            self.animation.event_source.stop()

        elif i < len(self.timestamps):
            self.ax.clear()
            self.ax.plot(self.x[:i+1], self.y[:i+1], self.z[:i+1])
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.set_zlabel('Z')

            self.ax.set_xlim([ self.canvas_limit_min, self.canvas_limit_max])
            self.ax.set_ylim([self.canvas_limit_min, self.canvas_limit_max])
            self.ax.set_zlim([self.canvas_limit_min, self.canvas_limit_max])

            '''

            xx, yy = np.meshgrid(np.arange(-1, 1, 0.01), np.arange(-1, 1, 0.01))
            zz = np.zeros_like(xx)
            self.ax.plot_surface(xx, yy, zz, alpha=0.2, color='grey')

            # add grey plane at z=1
            zz = np.ones_like(xx)
            self.ax.plot_surface(xx, yy, zz, alpha=0.2, color='grey')
            
            '''

            self.ax.set_title('Timestamp: {}'.format(self.timestamps[i]))
            self.canvas.draw()

    def plot_data(self):
        # clear existing plot data
        self.x = []
        self.y = []
        self.z = []
        self.timestamps = []

        file_data = self.parent.parent.parent.log_read_object
        file_data.read_file_execute(self.parent.parent.parent.file_loaded_to_gui)
        file_data.read_file_execute_headpose()
        self.add_data(file_data.x_list, file_data.y_list, file_data.z_list, file_data.timestamp_list)


        if len(file_data.x_list) == 0:
            # add a text item to the plot if x_data is empty
            self.messagebox.show()


        else:
            # update plot data
            self.canvas_limit_max = file_data.headpose_6dof_maximum_value
            self.canvas_limit_min = file_data.headpose_6dof_minimum_value
            self.animation = FuncAnimation(self.fig, self.animate,
                                           frames=len(self.timestamps), interval=1)
            #ADD A COLUR TO THE FLOOR OF THE CANVAS

            self.canvas.draw()



class Headpose_panel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.headpose_panel = Headpose(self)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.headpose_panel)
        vbox.addLayout(hbox)
        self.setLayout(vbox)


class Q6DOF_tab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        q6dof_tab_widget = QTabWidget()
        self.setStyleSheet("QTabBar::tab { height: 30px; }")
        q6dof_tab_widget.setTabPosition(QTabWidget.North)

        ####################################Add the panels here###################################################
        q6dof_tab_widget.addTab(Headpose_panel(self), "Headpose")

        ##########################################################################################################

        main_layout = QVBoxLayout()
        main_layout.addWidget(q6dof_tab_widget)
        self.setLayout(main_layout)


