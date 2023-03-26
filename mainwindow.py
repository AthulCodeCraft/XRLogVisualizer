import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QScrollArea, QWidget, QLabel, QVBoxLayout, QFileDialog, \
    QAction, \
    QTabWidget, QHBoxLayout, QCheckBox, QFrame, QPushButton, QSizePolicy, QScrollBar,QLineEdit

from PySide2.QtGui import QPixmap

import pyqtgraph as pg
import log_read as lr

class Scan_n_Edit(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        button_layout = QHBoxLayout()

        scan_button = QPushButton("Scan File", self)


        scan_button.setMinimumSize(204, 40)

        scan_button.setMaximumSize(204, 40)


        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)

        print("Scan use")
        scan_button.clicked.connect(self.run_scan_function)
        print("Scan done")



        button_layout.addWidget(scan_button)

        button_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Set the layout of the widget to the button layout
        self.setLayout(button_layout)



    def run_scan_function(self):
        print("Scan function action")
        #clear the teext_label in the right pane
        self.parent.parent.right_pane.text_label.setText("")
        tag_list=[]
        # to check the satus of the check box in the filter block
        for checkbox in self.parent.filter_block.filter_element.checkbox_list:
            if checkbox.isChecked():
                tag_list.append(checkbox.text())


        print(tag_list)
        self.parent.parent.parent.log_read_object.read_file_execute(self.parent.parent.parent.file_loaded_to_gui)
        self.parent.parent.parent.log_read_object.read_logs_with_tags(tag_list)
        filtered_logs=self.parent.parent.parent.log_read_object.return_filtered_logs()
        
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

        # controll the expanding or fixed scaling behiour of the cchild widget


class Filter_tag(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.checkbox_layout = QVBoxLayout()
        self.checkbox_list=[]
        self.textbox_list=[]
        checkbox_layout_list=[]

        for checkbox in range (0,14):
            self.checkbox_list.append(QCheckBox(self))
            self.textbox_list.append(QLineEdit(self))
            self.textbox_list[-1].setText("Tag")
            self.textbox_list[-1].textChanged.connect(lambda text, checkbox=self.checkbox_list[-1]: checkbox.setText(text))

            checkbox_layout_list.append(QHBoxLayout())
            checkbox_layout_list[-1].addWidget(self.checkbox_list[-1])
            checkbox_layout_list[-1].addWidget(self.textbox_list[-1])
            self.checkbox_layout.addLayout(checkbox_layout_list[-1])

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.checkbox_layout)
        self.main_layout.setAlignment(Qt.AlignLeft)
        self.setMinimumSize(180, 620)
        self.setMaximumSize(180, 620)

class Pannel_Data_DragnDrop(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.setStyleSheet("border: 2px solid black")

        self.text_label = QLabel()

        # create a QPixmap object with the image file
        pixmap = QPixmap(r'C:\Users\athul\PycharmProjects\Log_Analyser\thumbnail\img.png')

        # set the background image for the QLabel
        self.text_label.setPixmap(pixmap)

        # set the alignment of the label to center
        self.text_label.setAlignment(Qt.AlignLeft)

        # create a vertical box layout and add the label to it
        vbox = QVBoxLayout()

        # set the alignment of the vbox to the top
        vbox.setAlignment(Qt.AlignLeft)

        # set the layout of the widget to the vertical box layout

        # set the widget's minimum size to the size of the pixmap
        self.setMinimumSize(pixmap.size())

        # allow the widget to accept drops
        self.setAcceptDrops(True)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        vbox.addWidget(self.text_label)
        vbox.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setLayout(vbox)

    def dragEnterEvent(self, event):
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
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            for url in event.mimeData().urls():
                self.parent.parent.parent.file_loaded_to_gui = str(url.toLocalFile())
                self.local_filename=self.parent.parent.parent.file_loaded_to_gui
                print(self.parent.parent.parent.file_loaded_to_gui)
                print("File is saved in memory")

                # read the contents of the file and set the text of the parent's right_pane QLabel widget
                with open(self.local_filename, 'r', encoding='utf-8') as f:
                    text = f.read()
                    self.parent.parent.parent.data_loaded_to_gui = text
                    #self.parent.parent.right_pane.text_label.setText(text)


                # update the filename in the parent's left_pane QLabel widget
                filename = self.local_filename.split('/')[-1]
                #self.parent.left_pane.label.setText(filename)
        else:
            event.ignore()


class Pannel1_Left(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.dragndrop = Pannel_Data_DragnDrop(self)
        self.filter_block = Filter_Block(self)
        self.scan_edit = Scan_n_Edit(self)

        vbox = QVBoxLayout(self)

        vbox.addWidget(self.dragndrop)
        vbox.addWidget(self.filter_block)
        vbox.addWidget(self.scan_edit)

        vbox.setContentsMargins(20, 0, 0, 0)
        vbox.setSpacing(11)

        self.setLayout(vbox)


class Pannel1_Right(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # border
        self.setStyleSheet("border: 1px solid black;")

        self.parent = parent

        self.text_label = QLabel()
        self.text_label.setStyleSheet("background-color: lightblue")

        # create a scroll area and set the text label as its widget







        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.text_label)

        style = """
        QScrollBar:vertical {
            border: none;
            background: #f5f5f5;
            width: 10px;
            margin: 16px 0 16px 0;
        }

        QScrollBar::handle:vertical {
            background: #c2c2c2;
            min-height: 20px;
        }

        QScrollBar::add-line:vertical {
            border: none;
            background: none;
        }

        QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        """

        scroll_bar_style_sheet = QScrollBar().styleSheet() + style
        self.scroll_area.verticalScrollBar().setStyleSheet(scroll_bar_style_sheet)





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
        print(self.parent.parent.file_loaded_to_gui)
        file_data.read_file_execute(self.parent.parent.file_loaded_to_gui)
        file_data.read_file_execute_fps()
        self.x_data = file_data.timestamp_list

        self.y_data = file_data.fps_list



        # add data to plot
        self.plot.plot(self.x_data, self.y_data)

        # set fixed limits on x and y axes
        print(self.x_data[0])
        print(self.x_data[-1])
        self.plot.setLimits(xMin=self.x_data[0], xMax=self.x_data[-1], yMin=0, yMax=100)



        #self.plot.setMouseEnabled(x=False, y=False)

        # set plot to display as an image (no scrollbars)


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


class Panel3(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        panels = []
        for i in range(4):
            panel = QWidget()
            panel.setStyleSheet(f"background-color: rgb({i * 60}, {255 - i * 40}, {i * 80})")
            layout = QVBoxLayout()
            layout.addWidget(QLabel(f"Panel {i + 1}"))
            panel.setLayout(layout)
            panels.append(panel)

        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(panels[0])
        hbox1.addWidget(panels[1])
        vbox.addLayout(hbox1)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(panels[2])
        hbox2.addWidget(panels[3])
        vbox.addLayout(hbox2)

        self.setLayout(vbox)


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

        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        self.panel1 = Panel1(self)
        tab_widget.addTab(self.panel1, "Panel 1")

        desktop = QApplication.desktop()
        desktop_rect = desktop.geometry()

        desktop_width = desktop_rect.width()
        desktop_height = desktop_rect.height()

        self.panel2 = Panel2(self)
        tab_widget.addTab(self.panel2, "Panel 2")

        self.panel3 = Panel3(self)
        tab_widget.addTab(self.panel3, "Panel 3")

        self.panel1.setMaximumSize(desktop_width - 50, desktop_height - 150)
        self.panel2.setMaximumSize(desktop_width - 50, desktop_height - 150)
        self.panel3.setMaximumSize(desktop_width - 50, desktop_height - 150)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")

        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                self.panel1.left_pane.text_label.setText(text)
                filename = file_path.split('/')[-1]
                self.panel1.right_pane.text_label.setText(filename)


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