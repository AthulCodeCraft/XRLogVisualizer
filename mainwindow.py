import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
import pyqtgraph as pg
import log_read as lr
from PyQt5.QtGui import QTransform

import hbar as hb
from PyQt5.QtGui import QDrag
from PyQt5.QtCore import QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QTabWidget, QWidget
import data_tab

import multimedia_tab as multimedia_tab
import data_tab as data_tab
import pvr_tab as pvr_tab


from PyQt5 import QtCore, QtGui, QtWidgets


class TabBar(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt);
            #aalign text to left

            painter.restore()



class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QtWidgets.QTabWidget.West)

class ProxyStyle(QtWidgets.QProxyStyle):
    def drawControl(self, element, opt, painter, widget):
        if element == QtWidgets.QStyle.CE_TabBarTabLabel:
            ic = self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            r = QtCore.QRect(opt.rect)
            w =  0 if opt.icon.isNull() else opt.rect.width() + self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            r.setHeight(opt.fontMetrics.width(opt.text) + w)
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QtWidgets.QProxyStyle.drawControl(self, element, opt, painter, widget)








class HorizontalTabBar(QtWidgets.QTabBar):
    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        option = QtWidgets.QStyleOptionTab()
        for index in range(self.count()):
            print(index)
            self.initStyleOption(option, index)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, option)
            painter.drawText(self.tabRect(index),
                             QtCore.Qt.AlignCenter | QtCore.Qt.TextDontClip,
                             self.tabText(index))
            if index == 0:
                painter.drawImage(QtCore.QRectF(10, 40, 16, 16), QtGui.QImage("1.jpg"))
            elif index == 1:
                painter.drawImage(QtCore.QRectF(10, 140, 16, 16), QtGui.QImage("1.jpg"))


    def tabSizeHint(self, index):
        size = QtWidgets.QTabBar.tabSizeHint(self, index)
        size.setHeight=50
        size.setWidth=200
        if size.width() < size.height():
            size.transpose()
        return size


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        QtWidgets.QTabWidget.__init__(self, parent)
        self.setTabBar(HorizontalTabBar())
        self.setStyleSheet("QTabBar ::tab { SetAlignment(Qt.AlignLeft); }")




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_loaded_to_gui=""
        self.log_read_object=lr.ReadFile(self)
        self.setWindowTitle("Multi-Screen GUI")
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        self.setAcceptDrops(True)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)


        tab_widget = TabWidget()
        tab_widget.setTabPosition(QTabWidget.West)
        tab_widget.setTabShape(QTabWidget.Rounded)


        widget1=data_tab.Data_tab(self)
        widget2=(multimedia_tab.Multimedia_tab(self))
        widget3=(pvr_tab.PVR_tab(self))

        widget4 = (pvr_tab.PVR_tab(self))
        widget5 = (pvr_tab.PVR_tab(self))
        widget6 = (pvr_tab.PVR_tab(self))
        widget7 = (pvr_tab.PVR_tab(self))
        widget8 = (pvr_tab.PVR_tab(self))
        widget9 = (pvr_tab.PVR_tab(self))



        tab_widget.addTab(widget1, "Data")
        tab_widget.addTab(widget2, "Multimedia")
        tab_widget.addTab(widget3, "PVR")
        tab_widget.addTab(widget4, "6DoF")
        tab_widget.addTab(widget5, "OpenXR")
        tab_widget.addTab(widget6, "Errors")
        tab_widget.addTab(widget7, "Memory")
        tab_widget.addTab(widget8, "CPU/GP")
        
        tab_widget.addTab(widget9, "Usecases")



            #provide colur for seletc tabs nd height ,width
        tab_widget.setStyleSheet("QTabBar::tab { height: 100px; width: 200px; } QTabBar::tab:selected { background: #cee7ff;  }QTabBar ::tab { SetAlignment(Qt.AlignLeft); }    ")


        #allignntext to left




        main_layout.addWidget(tab_widget)

        #aalign tge textt o ;eft

        #increase rth tab icon size


        #self.dragndrop = Pannel_Data_DragnDrop(self)

        #main_layout.addWidget(self.dragndrop)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignCenter)

        self.progress_bar.setStyleSheet("QProgressBar::chunk {background-color: #6767ff;}")

        self.progress_bar_read =  QProgressBar()
        self.progress_bar_read.setRange(0, 100)
        self.progress_bar_read.setValue(0)
        self.progress_bar_read.setAlignment(Qt.AlignCenter)
        self.progress_bar.setStyleSheet("QProgressBar::chunk {background-color: #6767ff;}")


        #adjust the heighty
        self.progress_bar.setFixedHeight(5)
        self.progress_bar_read.setFixedHeight(5)
        #remove the percentage from the progress bar
        self.progress_bar.setTextVisible(False)
        self.progress_bar_read.setTextVisible(False)
        #change colur to blue



        main_layout.addWidget(self.progress_bar_read)
        main_layout.addWidget(self.progress_bar)


        # Set the maximum size of the panels
        desktop = QApplication.desktop()
        desktop_rect = desktop.geometry()
        desktop_width = desktop_rect.width()
        desktop_height = desktop_rect.height()

        self.setAcceptDrops(True)

        # Create the overlay label


        # self.overlay_label.raise_()

        self.overlay_label = QLabel(central_widget)
        pixmap2 = QPixmap(r"C:\Users\athul\PycharmProjects\Log_Analyser\thumbnail\drop.bmp")
        self.overlay_label.setPixmap(pixmap2)


        self.overlay_label.setScaledContents(True)
        self.overlay_label.setAlignment(Qt.AlignCenter)
        self.overlay_label.setStyleSheet("QLabel { background-color: rgba(255, 255, 255, 128); }")
        self.overlay_label.setGeometry(0, 0, desktop_width, desktop_height)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.5)
        self.overlay_label.setGraphicsEffect(opacity_effect)
        self.overlay_label.hide()
        #self.overlay_label.raise_()

    def dragEnterEvent(self, event):


        self.overlay_label.show()

        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.overlay_label.hide()
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            for url in event.mimeData().urls():
                self.file_loaded_to_gui = str(url.toLocalFile())
                self.local_filename=self.file_loaded_to_gui
                print(self.file_loaded_to_gui)

                with open(self.local_filename, 'r', encoding='utf-8') as f:
                    self.progress_bar.setStyleSheet("QProgressBar::chunk {background-color: #6767ff;}")
                    total_size = os.path.getsize(self.local_filename)
                    read_size = 0
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        read_size += len(data)
                        progress = int(read_size / total_size * 100)
                        self.progress_bar.setValue(progress)


                    self.progress_bar.setValue(100)

                    self.progress_bar.setStyleSheet("QProgressBar::chunk {background-color: ##67ff67;}")



                    self.data_loaded_to_gui = data


        else:
            event.ignore()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        self.file_loaded_to_gui = file_path

        if file_path:
            self.overlay_label2.hide()

            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                self.data_loaded_to_gui = text
                # self.parent.parent.right_pane.text_label.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    # Set the window's size to the screen size
    desktop = QApplication.desktop()
    screen = QApplication.primaryScreen()
    screen_rect = screen.geometry()
    print(screen_rect)
    window.setGeometry(screen_rect.left(), screen_rect.top(), int(.99*screen_rect.width()), int(.9*screen_rect.height()))
    scroll_area = QScrollArea()
    scroll_area.setWidget(window)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scroll_area.show()
    sys.exit(app.exec_())