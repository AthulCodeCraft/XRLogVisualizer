import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFileDialog, QAction,QProgressBar, QMenuBar, \
    QHBoxLayout, QScrollArea


class LeftPane(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # store the instance of DragDrop class as an instance variable
        #comment

        self.setAcceptDrops(True)

        self.label = QLabel("Drag and drop files here")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMaximumWidth(200)
        self.label.setStyleSheet("background-color: lightblue")

        hbox = QHBoxLayout()
        hbox.addWidget(self.label)
        self.setLayout(hbox)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = str(url.toLocalFile())

            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                print("read")
                filename = file_path.split('/')[-1]

                self.parent.right_pane.text_label.setText(text)
                self.parent.left_pane.label.setText(filename)



class RightPane(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.text_label = QLabel()

        self.text_label.setMinimumWidth(1000)
        self.text_label.setMaximumWidth(1000)
        self.text_label.setStyleSheet("background-color: lightgreen")


        # create a scroll area and set the text label as its widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.text_label)

        hbox = QHBoxLayout()
        hbox.addWidget(scroll_area)
        self.setLayout(hbox)



class DragDrop(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop")
        self.setGeometry(10, 30, 1000, 600)

        self.left_pane = LeftPane(self)
        self.right_pane = RightPane(self)

        hbox = QHBoxLayout()
        hbox.addWidget(self.left_pane)
        hbox.addWidget(self.right_pane)

        vbox = QVBoxLayout()
        menu_bar = QMenuBar(self)
        vbox.addWidget(menu_bar)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.create_menu(menu_bar)

    def create_menu(self, menu_bar):
        file_menu = menu_bar.addMenu("File")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)

        file_menu.addAction(open_action)

    def open_file(self):

        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")

        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                self.right_pane.text_label.setText(text)
                filename = file_path.split('/')[-1]
                self.left_pane.label.setText(filename)




if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = DragDrop()

    scroll_area = QScrollArea()
    scroll_area.setWidget(window)
    scroll_area.setWidgetResizable(True)
    scroll_area.setMinimumSize(1000, 600)
    scroll_area.setMaximumSize(1000, 600)
    scroll_area.show()

    sys.exit(app.exec_())