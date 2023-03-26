import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QScrollArea, QWidget, QLabel, QVBoxLayout, QFileDialog, \
    QAction, \
    QTabWidget, QHBoxLayout, QCheckBox, QFrame, QPushButton, QSizePolicy, QScrollBar

from PySide2.QtGui import QPixmap


class Scan_n_Edit(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        button_layout = QHBoxLayout()

        scan_button = QPushButton("Scan File", self)
        edit_button = QPushButton("Edit", self)

        scan_button.setMinimumSize(165, 40)

        scan_button.setMaximumSize(165, 40)
        edit_button.setMinimumSize(40, 40)
        edit_button.setMaximumSize(40, 40)

        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)

        button_layout.addWidget(edit_button)
        button_layout.addWidget(scan_button)

        button_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Set the layout of the widget to the button layout
        self.setLayout(button_layout)


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
        # self.setStyleSheet("border: 2px solid black")
        self.parent = parent
        self.checkbox_layout = QVBoxLayout()
        self.checkbox_layout.addWidget(QCheckBox("FPS", self))
        self.checkbox_layout.addWidget(QCheckBox("Battery Level", self))
        self.checkbox_layout.addWidget(QCheckBox("Frame Repeat", self))
        self.checkbox_layout.addWidget(QCheckBox("Bit Rate", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 2", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 3", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 1", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 2", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 3", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 1", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 2", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 3", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 1", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 2", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 3", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 1", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 2", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 3", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 1", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 2", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 3", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 1", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 2", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 3", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 1", self))
        self.checkbox_layout.addWidget(QCheckBox("Option 2", self))
        self.checkbox_layout.addWidget(QCheckBox("Wifi Speed", self))

        # create button and add it to new layout

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.checkbox_layout)

        self.main_layout.setAlignment(Qt.AlignLeft)
        self.setMinimumSize(204, 640)
        self.setMaximumSize(204, 640)


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
                file_path = str(url.toLocalFile())

                # read the contents of the file and set the text of the parent's right_pane QLabel widget
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    self.parent.parent.right_pane.text_label.setText(text)

                # update the filename in the parent's left_pane QLabel widget
                filename = file_path.split('/')[-1]
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
        self.text_label.setStyleSheet("background-color: lightgreen")

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




class Panel2(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        panels = []
        for i in range(6):
            panel = QWidget()
            panel.setStyleSheet(f"background-color: rgb({i * 20}, {255 - i * 20}, {i * 40})")
            layout = QVBoxLayout()
            layout.addWidget(QLabel(f"Panel {i + 1}"))
            panel.setLayout(layout)
            panels.append(panel)

        vbox = QVBoxLayout()
        for i in range(2):
            hbox = QHBoxLayout()
            hbox.addWidget(panels[i * 3])
            hbox.addWidget(panels[i * 3 + 1])
            hbox.addWidget(panels[i * 3 + 2])
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