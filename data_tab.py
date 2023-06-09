
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
import time


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
        self.setMinimumWidth(220)
        self.setMaximumWidth(220)


    def toggle_display(self, checked):
        self.toggle_flag = checked
        if self.toggle_flag:
            self.colour_flag = True
        else:
            self.colour_flag = False

    def run_scan_function(self):
        print("Scan function action")
        #clear the teext_label in the right pane
        self.parent.parent.right_panel.text_label.setText("")
        tag_list=[]
        tag_colour_list_box=[]
        # to check the satus of the check box in the filter block
        self.colour_list=["red","blue","green","yellow","orange","pink","purple","brown","grey","black","white","cyan","magenta","lime"]
        for checkbox in self.parent.filter_block.filter_element.checkbox_list:
            if checkbox.isChecked():
                tag_list.append(checkbox.text())
        self.parent.parent.parent.parent.log_read_object.read_file_execute(self.parent.parent.parent.parent.file_loaded_to_gui)
        self.parent.parent.parent.parent.log_read_object.read_logs_with_tags(tag_list)
        filtered_logs=self.parent.parent.parent.parent.log_read_object.return_filtered_logs()
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
            self.parent.parent.right_panel.text_label.setText(text_to_display)
        else:
            #add time record start time here
            start_time = time.time()

            text_to_display = '\n'.join(filtered_logs)
            #i only need to display a chunk of filters logs a point of time and if i scroll i need the next chunk of logs to be displayed
            #so i need to create a function that will display the logs in chunks

            print(len(text_to_display))
            #split the text to display into 10000 line each





            self.parent.parent.right_panel.text_label.setText(text_to_display)
            stop_time = time.time()
            print("Time taken to display the logs is ", stop_time - start_time)
class Filter_block(QLabel):
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



class Data_panel_left(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.filter_block = Filter_block(self)
        self.scan_edit = Scan_n_Edit(self)
        vbox = QVBoxLayout(self)

        vbox.addWidget(self.filter_block)
        vbox.addWidget(self.scan_edit)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(11)
        self.setLayout(vbox)
        self.setMinimumWidth(230)
        self.setMaximumWidth(230)
        #allgin the left panel to the left
        vbox.setAlignment(Qt.AlignTop | Qt.AlignLeft)



class Data_panel_right(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # set the background color of the widget
        self.setStyleSheet("background-color: white;")
        # create a QTextEdit widget and set its stylesheet
        self.text_label = QTextBrowser()
        self.text_label.setStyleSheet("background-color: #cee7ff;")
        # create a scroll area and set the text label as its widget

        # create a custom scrollbar stylesheet



        # create a layout for the widget
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(1)
        self.setMinimumWidth(1400)
        self.setMaximumWidth(1400)
        hbox.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        hbox.addWidget(self.text_label)
        #add scroll bars
        self.scrollbar = QScrollBar(self)
        self.scrollbar.setOrientation(Qt.Vertical)
        self.scrollbar2 = QScrollBar(self)
        self.scrollbar2.setOrientation(Qt.Horizontal)
        self.setLayout(hbox)

class Data_panel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.left_panel = Data_panel_left(self)
        self.right_panel = Data_panel_right(self)
        hbox = QHBoxLayout()
        hbox.addWidget(self.left_panel)  # horizontal stretch factor of 1/3
        hbox.addWidget(self.right_panel)  # horizontal stretch factor of 2/3
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        self.setLayout(vbox)
        #allign
        vbox.setAlignment(Qt.AlignTop | Qt.AlignLeft)


class Data_tab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        data_tab_widget = QTabWidget()
        data_tab_widget.setTabPosition(QTabWidget.North)
        self.setStyleSheet("QTabBar::tab { height: 30px; }")


        data_tab_widget.addTab(Data_panel(self), " Log Filter")


        main_layout = QVBoxLayout()
        main_layout.addWidget(data_tab_widget)
        self.setLayout(main_layout)
        #allgin
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)


