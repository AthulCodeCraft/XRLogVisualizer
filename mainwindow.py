import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
import pyqtgraph as pg
import log_read as lr
import hbar as hb
from PyQt5.QtGui import QDrag
from PyQt5.QtCore import QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QLabel, QApplication





class Scan_n_Edit(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.toggle_flag = False  # initial value of toggle flag
        button_layout = QHBoxLayout()
        self.colour_flag = False
        scan_button = QPushButton("Scan File", self)
        scan_button.setMinimumSize(160, 40)
        scan_button.setMaximumSize(160, 40)
        toggle_button = QToolButton(self)
        toggle_button.setFixedSize(40, 40)
        toggle_button.setCheckable(True)
        # Set custom icon for toggle button
        toggle_button.setIcon(QIcon(r"C:\Users\athul\PycharmProjects\Log_Analyser\thumbnail\img123.png"))
        toggle_button.setIconSize(QSize(30, 30))
        toggle_button.setStyleSheet(
            """
            QToolButton {
                background-color: #bbb;
                border: none;
                border-radius: 15px;
            }
            QToolButton:checked {
                background-color: #27ae60;
            }
            """
        )
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        scan_button.clicked.connect(self.run_scan_function)
        toggle_button.clicked.connect(self.toggle_display)
        button_layout.addWidget(toggle_button)
        button_layout.addWidget(scan_button)
        button_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setLayout(button_layout)

    def toggle_display(self, checked):
        self.toggle_flag = checked
        if self.toggle_flag:
            self.colour_flag = True
        else:
            self.colour_flag = False

    def run_scan_function(self):
        print("Scan function action")
        #clear the teext_label in the right pane
        self.parent.parent.right_pane.text_label.setText("")
        tag_list=[]
        tag_colour_list_box=[]
        # to check the satus of the check box in the filter block
        self.colour_list=["red","blue","green","yellow","orange","pink","purple","brown","grey","black","white","cyan","magenta","lime"]
        for checkbox in self.parent.filter_block.filter_element.checkbox_list:
            if checkbox.isChecked():
                tag_list.append(checkbox.text())
        self.parent.parent.parent.log_read_object.read_file_execute(self.parent.parent.parent.file_loaded_to_gui)
        self.parent.parent.parent.log_read_object.read_logs_with_tags(tag_list)
        filtered_logs=self.parent.parent.parent.log_read_object.return_filtered_logs()
        filter_log_colured=[]

        if(self.colour_flag):
            for line in filtered_logs:
                # create a for i loop for tag in tag_list
                for i in range(len(tag_list)):
                    tag=tag_list[i]

                    if tag in line:
                        colured_line=f"<font color={self.colour_list[i]}>{line}</font><br>"
                filter_log_colured.append(colured_line)
            text_to_display = '\n'.join(filter_log_colured)
            self.parent.parent.right_pane.text_label.setText(text_to_display)
        else:
            text_to_display = '\n'.join(filtered_logs)
            self.parent.parent.right_pane.text_label.setText(text_to_display)

class Filter_Block(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.filter_element = Filter_tag(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setWidget(self.filter_element)
        layout = QHBoxLayout(self)
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)
        self.setMinimumSize(204, 640)
        self.setMaximumSize(204, 640)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

class Filter_tag(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.checkbox_layout = QVBoxLayout()
        self.checkbox_list=[]
        self.textbox_list=[]
        checkbox_layout_list=[]
        #create a dictionary with key as the tag and value as the colour
        self.tag_colour_list_box={}

        for checkbox in range (0,14):
            self.checkbox_list.append(QCheckBox(self))
            self.textbox_list.append(QLineEdit(self))
            self.textbox_list[-1].setText("")
            self.textbox_list[-1].textChanged.connect(lambda text, checkbox=self.checkbox_list[-1], textbox=self.textbox_list[-1]: checkbox.setText(textbox.text()))

            checkbox_layout_list.append(QHBoxLayout())
            checkbox_layout_list[-1].addWidget(self.checkbox_list[-1])
            # comment out the next line to remove the textbox from the layout
            checkbox_layout_list[-1].addWidget(self.textbox_list[-1])
            self.checkbox_layout.addLayout(checkbox_layout_list[-1])

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.checkbox_layout)
        self.main_layout.setAlignment(Qt.AlignLeft)
        self.setMinimumSize(180, 620)
        self.setMaximumSize(180, 620)



class Pannel1_Left(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.filter_block = Filter_Block(self)
        self.scan_edit = Scan_n_Edit(self)
        vbox = QVBoxLayout(self)

        vbox.addWidget(self.filter_block)
        vbox.addWidget(self.scan_edit)
        vbox.setContentsMargins(20, 0, 0, 0)
        vbox.setSpacing(11)
        self.setLayout(vbox)
class Pannel1_Right(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # set the background color of the widget
        self.setStyleSheet("background-color: white;")
        # create a QTextEdit widget and set its stylesheet
        self.text_label = QTextBrowser()
        self.text_label.setStyleSheet("background-color: lightblue;")
        # create a scroll area and set the text label as its widget
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.text_label)
        # create a custom scrollbar stylesheet

        scrollbar_stylesheet = """
        QScrollBar:vertical {
            background: transparent;
            width: 12px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background-color: #BDBDBD;
            border-radius: 6px;
            min-height: 20px;
        }
        QScrollBar::handle:hover {
            background-color: #9E9E9E;
        }
        QScrollBar::add-line:vertical {
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            height: 0px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical {
            background-color: transparent;
        }
        QScrollBar::add-page:vertical {
            margin: 0px;
        }
        QScrollBar::sub-page:vertical {
            margin: 0px;
        }
        """

        # set the custom stylesheet to the scrollbar
        self.scroll_area.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)

        # create a layout for the widget
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        hbox.addWidget(self.scroll_area)
        self.setMinimumWidth(1600)
        self.setMaximumWidth(1600)
        self.setLayout(hbox)
        hbox.setAlignment(Qt.AlignTop | Qt.AlignLeft)


class Panel1(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.left_pane = Pannel1_Left(self)
        self.right_pane = Pannel1_Right(self)
        hbox = QHBoxLayout()
        hbox.addWidget(self.left_pane, 1)  # horizontal stretch factor of 1/3
        hbox.addWidget(self.right_pane, 2)  # horizontal stretch factor of 2/3
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        self.setLayout(vbox)


class FPS(QWidget):
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
        file_data = self.parent.parent.log_read_object

        file_data.read_file_execute(self.parent.parent.file_loaded_to_gui)
        file_data.read_file_execute_fps()
        self.x_data = file_data.timestamp_list
        self.y_data = file_data.fps_list

        if not (len(self.y_data)) == 0:
            # add data to plot
            self.plot.plot(self.x_data, self.y_data)
            # set fixed limits on x and y axes

            self.plot.setLimits(xMin=self.x_data[0], xMax=self.x_data[-1], yMin=0, yMax=100)
            #self.plot.setMouseEnabled(x=False, y=False)
            #set plot to display as an image (no scrollbars)


class Panel2(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.fps_widget = FPS(self)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.fps_widget)
        vbox.addLayout(hbox)
        self.setLayout(vbox)


class Battery_Level(QWidget):
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
        file_data = self.parent.parent.log_read_object

        file_data.read_file_execute(self.parent.parent.file_loaded_to_gui)
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


class Panel3(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.battery_level = Battery_Level(self)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.battery_level)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
class Tab3Panels(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        tab_widget3 = QTabWidget()
        tab_widget3.setTabPosition(QTabWidget.North)


        tab_widget3.addTab(Panel2(self), "Headpose")
        tab_widget3.addTab(Panel3(self), "Tracking Camera FPS")
        tab_widget3.addTab(Panel3(self), "RGB Camera FPS")


        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget3)
        self.setLayout(main_layout)
class Tab1Panels(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        tab_widget1 = QTabWidget()
        tab_widget1.setTabPosition(QTabWidget.North)


        tab_widget1.addTab(Panel2(self), "FPS")
        tab_widget1.addTab(Panel2(self), "Battery")
        tab_widget1.addTab(Panel3(self), "ISO Gain")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget1)
        self.setLayout(main_layout)
class Tab2Panels(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        tab_widget2 = QTabWidget()
        tab_widget2.setTabPosition(QTabWidget.North)


        tab_widget2.addTab(Panel1(self), "Validate Data")


        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget2)
        self.setLayout(main_layout)





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_loaded_to_gui=""
        self.log_read_object=lr.ReadFile()
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

        tab_widget=hb.TabWidget()
        tab_widget.setTabPosition(QTabWidget.West)

        #change tab button width to 300



        print("abcd")



        tab_widget.addTab(Tab2Panels(self),"Data")
        tab_widget.addTab(Tab1Panels(self),"Mulitmedia")
        tab_widget.addTab(Tab3Panels(self),"QVR")

        tab_widget.tabBar().setStyleSheet("QTabBar::tab { width: 200px; }")

        #self.dragndrop = Pannel_Data_DragnDrop(self)

        #main_layout.addWidget(self.dragndrop)

        main_layout.addWidget(tab_widget)


        # Set the maximum size of the panels
        desktop = QApplication.desktop()
        desktop_rect = desktop.geometry()
        desktop_width = desktop_rect.width()
        desktop_height = desktop_rect.height()

        self.setAcceptDrops(True)

        # Create the overlay label
        self.overlay_label2 = QLabel(central_widget)
        pixmap = QPixmap(r"C:\Users\athul\PycharmProjects\Log_Analyser\thumbnail\dd.bmp")
        # set the QPixmap instance as the label's image
        self.overlay_label2.setPixmap(pixmap)

        self.overlay_label2.setScaledContents(True)
        self.overlay_label2.setAlignment(Qt.AlignCenter)
        self.overlay_label2.setStyleSheet("QLabel { background-color: rgba(255, 255, 255, 128); }")
        self.overlay_label2.setGeometry(0, 0, desktop_width, desktop_height)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.5)
        self.overlay_label2.setGraphicsEffect(opacity_effect)

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

        self.overlay_label2.hide()
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
        self.overlay_label2.hide()

        self.overlay_label.hide()
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            for url in event.mimeData().urls():
                self.file_loaded_to_gui = str(url.toLocalFile())
                self.local_filename=self.file_loaded_to_gui
                print(self.file_loaded_to_gui)

                with open(self.local_filename, 'r', encoding='utf-8') as f:
                    text = f.read()
                    self.data_loaded_to_gui = text
                    #self.parent.parent.right_pane.text_label.setText(text)

        else:
            event.ignore()


    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        self.file_loaded_to_gui=file_path

        if file_path:
            self.overlay_label2.hide()

            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                self.data_loaded_to_gui = text
                #self.parent.parent.right_pane.text_label.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    # Set the window's size to the screen size
    desktop = QApplication.desktop()
    screen = QApplication.primaryScreen()
    screen_rect = screen.geometry()
    window.setGeometry(screen_rect)
    scroll_area = QScrollArea()
    scroll_area.setWidget(window)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scroll_area.show()
    sys.exit(app.exec_())