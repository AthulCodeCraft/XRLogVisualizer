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


class WIP_Panel_Tab1(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        layout = QHBoxLayout()
        #create a lable for work in pgrogress
        self.messagebox = QLabel("Coming soon, Work in progress")
        layout.addWidget(self.messagebox)
        self.messagebox.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)


class WIP_Panel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.wip_panel_tab1 = WIP_Panel_Tab1(self)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.wip_panel_tab1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

class WIP(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        wip_widget = QTabWidget()
        self.setStyleSheet("QTabBar::tab { height: 30px; }")
        wip_widget.setTabPosition(QTabWidget.North)

        ####################################Add the panels here###################################################
        wip_widget.addTab(WIP_Panel(self), "Sub Tab")
        ##########################################################################################################
        main_layout = QVBoxLayout()
        main_layout.addWidget(wip_widget)
        self.setLayout(main_layout)


