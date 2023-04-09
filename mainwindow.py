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
from datetime import datetime
import multimedia_tab as multimedia_tab
import data_tab as data_tab
import pvr_tab as pvr_tab
import q6dof_tab as q6dof_tab
import wip as wip_tab



from PyQt5 import QtCore, QtGui, QtWidgets

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_loaded_to_gui=""

        self.log_read_object=lr.ReadFile(self)
        self.setWindowTitle("Multi-Screen GUI")
        menu_bar = self.menuBar()
        self.log_window = Log_Window(self)
        file_menu = menu_bar.addMenu("File")
        open_action = QAction("Open", self)
        #width of the open command is less
        open_action.setShortcut("Ctrl+O")


        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)


        app_log_action = QAction("APP Logs", self)
        app_log_action.setShortcut("Ctrl+L")
        app_log_action.triggered.connect(self.open_app_log)
        file_menu.addAction(app_log_action)





        self.setAcceptDrops(True)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)


        tab_widget = hb.TabWidget()
        tab_widget.setTabPosition(QTabWidget.West)
        tab_widget.setTabShape(QTabWidget.Rounded)


        widget1=data_tab.Data_tab(self)
        widget2=(multimedia_tab.Multimedia_tab(self))
        widget3=(pvr_tab.PVR_tab(self))
        widget4=(q6dof_tab.Q6DOF_tab(self))

        widget5 = (wip_tab.WIP(self))
        widget6 = (wip_tab.WIP(self))
        widget7 = (wip_tab.WIP(self))
        widget8 = (wip_tab.WIP(self))
        widget9 = (wip_tab.WIP(self))
        widget10 = (wip_tab.WIP(self))
        widget11 = (wip_tab.WIP(self))






        tab_widget.addTab(widget1, "Data")
        tab_widget.addTab(widget2, "Multimedia")
        tab_widget.addTab(widget3, "PVR")
        tab_widget.addTab(widget4, "6DoF")
        tab_widget.addTab(widget5, "OpenXR")
        tab_widget.addTab(widget6, "Errors")
        tab_widget.addTab(widget7, "Memory")
        tab_widget.addTab(widget8, "GPU")
        tab_widget.addTab(widget9, "Wi-Fi")
        tab_widget.addTab(widget10, "Usecases")
        tab_widget.addTab(widget11, "Controllers")



            #provide colur for seletc tabs nd height ,width
        tab_widget.setStyleSheet("QTabBar { font-size: 16px; font-family: Calibri; } QTabBar::tab { height: 70px; width: 200px; font-size: 14px; font-family: Calibri; } QTabBar::tab:selected { background: #cee7ff; } QTabBar::tab { SetAlignment(Qt.AlignLeft); }")

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
        log_marking = "["+str(datetime.now())+"]"+"[" + self.__class__.__name__ + "][" + self.__init__.__name__ + "]" +"[INFO]"+ "[Main Window init is completed" + "]"
        self.log_window.addlogs(log_marking)

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

    def exit_file(self):
        #close the full pgm
        sys.exit()
    def open_app_log(self):
        #show all print statements of this code in this function in a new gui window

        self.log_window.show()





    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        self.file_loaded_to_gui = file_path

        if file_path:


            with open(self.file_loaded_to_gui, 'r', encoding='utf-8') as f:
                self.progress_bar.setStyleSheet("QProgressBar::chunk {background-color: #6767ff;}")
                total_size = os.path.getsize(self.file_loaded_to_gui)
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
                # self.parent.parent.right_pane.text_label.setText(text)
                #get the name of the class

                log_marking="["+str(datetime.now())+"]"+"["+self.__class__.__name__+"]["+self.open_file.__name__+"]"+"[INFO]"+"["+"File is loaded to GUI"+"]"
                self.log_window.addlogs(log_marking)


class Log_Window(QMainWindow):
    def __init__(self,parent):
        super().__init__()
        self.parent=parent
        self.setWindowTitle("Log Window")
        self.setGeometry(0, 0, 500, 500)
        self.tablelogs = QTableWidget()
        self.tablelogs.setColumnCount(5)
        self.tablelogs.setHorizontalHeaderLabels(["Time","Class", "Function","Type", "Message"])
        self.tablelogs.setRowCount(0)
        #lock the edit
        self.tablelogs.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #lock the resize


        self.tablelogs.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)




        #print the current time



        self.addlogs("["+str(datetime.now())+"]"+"[][][][Welcome to XRLogVisualizer!!]")

    def addlogs(self, text):
        #append logs to text browser

        #add a new row
        rowPosition = self.tablelogs.rowCount()
        self.tablelogs.insertRow(rowPosition)
        #add the text to the new row
        self.tablelogs.setItem(rowPosition , 0, QTableWidgetItem(text.split("]")[0].split("[")[1]))
        self.tablelogs.setItem(rowPosition , 1, QTableWidgetItem(text.split("]")[1].split("[")[1]))
        self.tablelogs.setItem(rowPosition , 2, QTableWidgetItem(text.split("]")[2].split("[")[1]))
        self.tablelogs.setItem(rowPosition , 3, QTableWidgetItem(text.split("]")[3].split("[")[1]))
        self.tablelogs.setItem(rowPosition , 4, QTableWidgetItem(text.split("]")[4].split("[")[1]))

        self.tablelogs.resizeColumnsToContents()
        self.tablelogs.resizeRowsToContents()
        self.setCentralWidget(self.tablelogs)







if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    # Set the window title



    window.setWindowTitle("XRLogVisualizer")
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