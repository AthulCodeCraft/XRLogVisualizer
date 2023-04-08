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
from PyQt5.QtGui import QFont
from matplotlib.widgets import Cursor


class PVR_Tracking_Cam_FPS(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.plot = pg.PlotWidget()
        self.plot.setBackground('w')  # set background color to white
        self.plot.setLabel('left', 'Y Axis Label')
        self.plot.setLabel('bottom', 'X Axis Label')
        font = QFont('Calibri', 11, QFont.Bold)
        self.plot.getAxis('bottom').setTickFont(font)
        self.plot.getAxis('left').setTickFont(font)
        self.plot.getAxis('bottom').setLabel(text='Timestamp', font=font, color='k')
        self.plot.getAxis('left').setLabel(text='Tracking camera FPS', font=font, color='k')

        # set line color and marker color for plotted data
        self.pen = pg.mkPen(color=(0, 112, 192), width=5)  # red line with width of 2
        self.brush = pg.mkBrush(color=(0, 112, 192))  # blue marker





        # create button to plot data
        self.hbox= QVBoxLayout()
        self.plot_button = QPushButton('Plot Data')
        self.messagebox = QLabel('No data to plot')
        #font colur should be red
        self.messagebox.setStyleSheet("QLabel { color : red; }")
        #add width for hbox
        self.hbox.setContentsMargins(5, 0, 0, 0)
        self.messagebox.hide()
        self.hbox.addWidget(self.plot_button)
        self.hbox.addWidget(self.messagebox)
        self.hbox.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        #create a qlabel below the pus hbutton
        self.plot_button.clicked.connect(self.plot_data)
        # add plot widget and button to layout
        layout = QHBoxLayout()
        layout.addWidget(self.plot)
        layout.addLayout(self.hbox)
        self.setLayout(layout)

    def plot_data(self):
        self.plot.clear()
        file_data = self.parent.parent.parent.log_read_object
        file_data.read_file_execute(self.parent.parent.parent.file_loaded_to_gui)
        file_data.read_meta_info_xml()
        self.x_data = file_data.metainfo_timestamp_list
        self.y_data = file_data.tracking_camera_fps_list

        if not (len(self.x_data)) == 0:

            self.messagebox.hide()
            self.plot.addLegend()
            self.plot.plot(self.x_data, self.y_data, pen=self.pen, brush=self.brush, name='isoGain')

            self.plot.setLimits(xMin=self.x_data[0], xMax=self.x_data[-1], yMin=-100, yMax=200)
            font = QFont('Calibri', 10, QFont.Bold)
            self.legend.setStyle(font=font, textColor='k')

        else:
            self.messagebox.show()
class Tracking_Cam_FPS_panel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.tracking_Cam_fps_panel = PVR_Tracking_Cam_FPS(self)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.tracking_Cam_fps_panel)
        vbox.addLayout(hbox)
        self.setLayout(vbox)


class PVR_isoGain(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.plot = pg.PlotWidget()
        self.plot.setBackground('w')  # set background color to white
        self.plot.setLabel('left', 'Y Axis Label')
        self.plot.setLabel('bottom', 'X Axis Label')
        font = QFont('Calibri', 11, QFont.Bold)
        self.plot.getAxis('bottom').setTickFont(font)
        self.plot.getAxis('left').setTickFont(font)
        self.plot.getAxis('bottom').setLabel(text='Timestamp', font=font, color='k')
        self.plot.getAxis('left').setLabel(text='isoGain', font=font, color='k')

        # set line color and marker color for plotted data
        self.pen = pg.mkPen(color=(0, 112, 192), width=5)  # red line with width of 2
        self.brush = pg.mkBrush(color=(0, 112, 192))  # blue marker





        # create button to plot data
        self.hbox= QVBoxLayout()
        self.plot_button = QPushButton('Plot Data')
        self.messagebox = QLabel('No data to plot')
        #font colur should be red
        self.messagebox.setStyleSheet("QLabel { color : red; }")
        #add width for hbox
        self.hbox.setContentsMargins(5, 0, 0, 0)
        self.messagebox.hide()
        self.hbox.addWidget(self.plot_button)
        self.hbox.addWidget(self.messagebox)
        self.hbox.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        #create a qlabel below the pus hbutton
        self.plot_button.clicked.connect(self.plot_data)
        # add plot widget and button to layout
        layout = QHBoxLayout()
        layout.addWidget(self.plot)
        layout.addLayout(self.hbox)
        self.setLayout(layout)

    def plot_data(self):
        self.plot.clear()
        file_data = self.parent.parent.parent.log_read_object
        file_data.read_file_execute(self.parent.parent.parent.file_loaded_to_gui)
        file_data.read_meta_info_xml()
        self.x_data = file_data.metainfo_timestamp_list
        self.y_data = file_data.isogain_list

        if not (len(self.x_data)) == 0:

            self.messagebox.hide()
            self.plot.addLegend()
            self.plot.plot(self.x_data, self.y_data, pen=self.pen, brush=self.brush, name='isoGain')

            self.plot.setLimits(xMin=self.x_data[0], xMax=self.x_data[-1], yMin=file_data.metainfo_iso_gain_minimum_value, yMax=file_data.metainfo_iso_gain_maximum_value)
            font = QFont('Calibri', 10, QFont.Bold)
            self.legend.setStyle(font=font, textColor='k')

        else:
            self.messagebox.show()
class IsoGain_panel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.iso_gain_panel = PVR_isoGain(self)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.iso_gain_panel)
        vbox.addLayout(hbox)
        self.setLayout(vbox)




class PVR_ExposureNs(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.plot = pg.PlotWidget()
        self.plot.setBackground('w')  # set background color to white
        self.plot.setLabel('left', 'Y Axis Label')
        self.plot.setLabel('bottom', 'X Axis Label')
        font = QFont('Calibri', 11, QFont.Bold)
        self.plot.getAxis('bottom').setTickFont(font)
        self.plot.getAxis('left').setTickFont(font)
        self.plot.getAxis('bottom').setLabel(text='Timestamp', font=font, color='k')
        self.plot.getAxis('left').setLabel(text='ExposureNs', font=font, color='k')

        # set line color and marker color for plotted data
        self.pen = pg.mkPen(color=(0, 112, 192), width=5)  # red line with width of 2
        self.brush = pg.mkBrush(color=(0, 112, 192))  # blue marker





        # create button to plot data
        self.hbox= QVBoxLayout()
        self.plot_button = QPushButton('Plot Data')
        self.messagebox = QLabel('No data to plot')
        #font colur should be red
        self.messagebox.setStyleSheet("QLabel { color : red; }")
        #add width for hbox
        self.hbox.setContentsMargins(5, 0, 0, 0)
        self.messagebox.hide()
        self.hbox.addWidget(self.plot_button)
        self.hbox.addWidget(self.messagebox)
        self.hbox.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        #create a qlabel below the pus hbutton
        self.plot_button.clicked.connect(self.plot_data)
        # add plot widget and button to layout
        layout = QHBoxLayout()
        layout.addWidget(self.plot)
        layout.addLayout(self.hbox)
        self.setLayout(layout)

    def plot_data(self):
        self.plot.clear()
        file_data = self.parent.parent.parent.log_read_object
        file_data.read_file_execute(self.parent.parent.parent.file_loaded_to_gui)
        file_data.read_meta_info_xml()
        self.x_data = file_data.metainfo_timestamp_list
        self.y_data = file_data.exposure_ns_list



        if not (len(self.x_data)) == 0:

            self.messagebox.hide()
            self.plot.addLegend()
            self.plot.plot(self.x_data, self.y_data, pen=self.pen, brush=self.brush, name='ExposureNs')




            self.plot.setLimits(xMin=self.x_data[0], xMax=self.x_data[-1], yMin=file_data.metainfo_exposure_minimum_value, yMax=file_data.metainfo_exposure_maximum_value)
            font = QFont('Calibri', 10, QFont.Bold)
            self.legend.setStyle(font=font, textColor='k')

        else:
            self.messagebox.show()


class ExposureNS_panel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.exposure_ns_panel = PVR_ExposureNs(self)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.exposure_ns_panel)
        vbox.addLayout(hbox)
        self.setLayout(vbox)



####################################################################################################################################################################
class PVR_EulerAngle(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.plot = pg.PlotWidget()
        self.plot.setBackground('w')  # set background color to white
        self.plot.setLabel('left', 'Y Axis Label')
        self.plot.setLabel('bottom', 'X Axis Label')
        font = QFont('Calibri', 11, QFont.Bold)
        self.plot.getAxis('bottom').setTickFont(font)
        self.plot.getAxis('left').setTickFont(font)
        self.plot.getAxis('bottom').setLabel(text='Timestamp', font=font, color='k')
        self.plot.getAxis('left').setLabel(text='Euler Angle', font=font, color='k')

        # set line color and marker color for plotted data
        self.pen_1 = pg.mkPen(color=(0, 112, 192), width=5)  # red line with width of 2
        self.brush_1 = pg.mkBrush(color=(0, 112, 192))  # blue marker

        #create pemn 2 for red colur
        self.pen_2 = pg.mkPen(color=(255, 0, 0), width=5)  # red line with width of 2
        self.brush_2 = pg.mkBrush(color=(255, 0, 0))  # blue marker

        #create green pen foe pen3
        self.pen_3 = pg.mkPen(color=(0, 255, 0), width=5)  # red line with width of 2
        self.brush_3 = pg.mkBrush(color=(0, 255, 0))  # blue marker



        # create button to plot data
        self.hbox= QVBoxLayout()
        self.plot_button = QPushButton('Plot Data')
        self.messagebox = QLabel('No data to plot')
        #font colur should be red
        self.messagebox.setStyleSheet("QLabel { color : red; }")
        #add width for hbox
        self.hbox.setContentsMargins(5, 0, 0, 0)
        self.messagebox.hide()
        self.hbox.addWidget(self.plot_button)
        self.hbox.addWidget(self.messagebox)
        self.hbox.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        #create a qlabel below the pus hbutton
        self.plot_button.clicked.connect(self.plot_data)
        # add plot widget and button to layout
        layout = QHBoxLayout()
        layout.addWidget(self.plot)
        layout.addLayout(self.hbox)
        self.setLayout(layout)

    def plot_data(self):
        self.plot.clear()
        file_data = self.parent.parent.parent.log_read_object
        file_data.read_file_execute(self.parent.parent.parent.file_loaded_to_gui)
        file_data.read_head_tracking_pose_xml()
        self.x_data = file_data.htp_timestamp_list
        self.y_data_1 = file_data.htp_pitch_list
        self.y_data_2 = file_data.htp_yaw_list
        self.y_data_3 = file_data.htp_roll_list


        if not (len(self.x_data)) == 0:

            self.messagebox.hide()
            self.plot.addLegend()
            self.plot.plot(self.x_data, self.y_data_1, pen=self.pen_1, brush=self.brush_1, name='Pitch')
            self.plot.plot(self.x_data, self.y_data_2, pen=self.pen_2, brush=self.brush_2, name='Yaw')
            self.plot.plot(self.x_data, self.y_data_3, pen=self.pen_3, brush=self.brush_3, name='Roll')



            self.plot.setLimits(xMin=self.x_data[0], xMax=self.x_data[-1], yMin=-180, yMax=180)
            font = QFont('Calibri', 10, QFont.Bold)
            self.legend.setStyle(font=font, textColor='k')

        else:
            self.messagebox.show()


class EulerAngle_panel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.euler_angle_panel = PVR_EulerAngle(self)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.euler_angle_panel)
        vbox.addLayout(hbox)
        self.setLayout(vbox)


class PVR_Headpose(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.plot = pg.PlotWidget()
        self.plot.setBackground('w')  # set background color to white
        self.plot.setLabel('left', 'Y Axis Label')
        self.plot.setLabel('bottom', 'X Axis Label')
        font = QFont('Calibri', 11, QFont.Bold)
        self.plot.getAxis('bottom').setTickFont(font)
        self.plot.getAxis('left').setTickFont(font)
        self.plot.getAxis('bottom').setLabel(text='Timestamp', font=font, color='k')
        self.plot.getAxis('left').setLabel(text='FPS', font=font, color='k')

        # set line color and marker color for plotted data
        self.pen_1 = pg.mkPen(color=(0, 112, 192), width=5)  # red line with width of 2
        self.brush_1 = pg.mkBrush(color=(0, 112, 192))  # blue marker

        #create pemn 2 for red colur
        self.pen_2 = pg.mkPen(color=(255, 0, 0), width=5)  # red line with width of 2
        self.brush_2 = pg.mkBrush(color=(255, 0, 0))  # blue marker

        #create green pen foe pen3
        self.pen_3 = pg.mkPen(color=(0, 255, 0), width=5)  # red line with width of 2
        self.brush_3 = pg.mkBrush(color=(0, 255, 0))  # blue marker

        #create a pen4 with doted line
        self.pen_4 = pg.mkPen(color=(255, 255, 0), width=5, style=Qt.DotLine)  # red line with width of 2
        self.brush_4 = pg.mkBrush(color=(255, 255, 0))  # blue marker


        # create button to plot data
        self.hbox= QVBoxLayout()
        self.plot_button = QPushButton('Plot Data')
        self.messagebox = QLabel('No data to plot')
        #font colur should be red
        self.messagebox.setStyleSheet("QLabel { color : red; }")
        #add width for hbox
        self.hbox.setContentsMargins(5, 0, 0, 0)
        self.messagebox.hide()
        self.hbox.addWidget(self.plot_button)
        self.hbox.addWidget(self.messagebox)
        self.hbox.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        #create a qlabel below the pus hbutton
        self.plot_button.clicked.connect(self.plot_data)
        # add plot widget and button to layout
        layout = QHBoxLayout()
        layout.addWidget(self.plot)
        layout.addLayout(self.hbox)
        self.setLayout(layout)

    def plot_data(self):
        self.plot.clear()
        file_data = self.parent.parent.parent.log_read_object
        file_data.read_file_execute(self.parent.parent.parent.file_loaded_to_gui)
        file_data.read_head_tracking_pose_xml()
        self.x_data = file_data.htp_timestamp_list
        self.y_data_1 = file_data.htp_x_list
        self.y_data_2 = file_data.htp_y_list
        self.y_data_3 = file_data.htp_z_list
        self.y_data_4 = [((file_data.htp_maximum_value+file_data.htp_minimum_value)/4) if x <= 0.700000 else ((file_data.htp_maximum_value+file_data.htp_minimum_value)/2) for x in file_data.htp_technique_list]



        if not (len(self.x_data)) == 0:

            self.messagebox.hide()
            self.plot.addLegend()
            self.plot.plot(self.x_data, self.y_data_1, pen=self.pen_1, brush=self.brush_1, name='X Headpose')
            self.plot.plot(self.x_data, self.y_data_2, pen=self.pen_2, brush=self.brush_2, name='Y Headpose')
            self.plot.plot(self.x_data, self.y_data_3, pen=self.pen_3, brush=self.brush_3, name='Z Headpose')
            self.plot.plot(self.x_data, self.y_data_4, pen=self.pen_4, brush=self.brush_4, name='Technique')


            self.plot.setLimits(xMin=self.x_data[0], xMax=self.x_data[-1], yMin=file_data.htp_minimum_value, yMax=file_data.htp_maximum_value)
            font = QFont('Calibri', 10, QFont.Bold)
            self.legend.setStyle(font=font, textColor='k')\

        else:
            self.messagebox.show()


class Headpose_panel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.headpose_panel = PVR_Headpose(self)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.headpose_panel)
        vbox.addLayout(hbox)
        self.setLayout(vbox)


class PVR_tab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        pvr_tab_widget = QTabWidget()
        self.setStyleSheet("QTabBar::tab { height: 30px; }")
        pvr_tab_widget.setTabPosition(QTabWidget.North)

        ####################################Add the panels here###################################################
        pvr_tab_widget.addTab(Headpose_panel(self), "Headpose")
        pvr_tab_widget.addTab(EulerAngle_panel(self), "Euler Angle")
        pvr_tab_widget.addTab(ExposureNS_panel(self), "ExposureNS")
        pvr_tab_widget.addTab(IsoGain_panel(self), "ISO Gain")
        pvr_tab_widget.addTab(Tracking_Cam_FPS_panel(self), "Tracking camera FPS")

        ##########################################################################################################

        main_layout = QVBoxLayout()
        main_layout.addWidget(pvr_tab_widget)
        self.setLayout(main_layout)


