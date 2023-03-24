from PySide2.QtCore import Qt, QThread, Signal
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFileDialog, QAction, QProgressBar, \
    QMenuBar, QHBoxLayout, QScrollArea
import time
import sys


class FileReader(QThread):
    progressChanged = Signal(int)
    textChanged = Signal(str)

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path

    def run(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            file_size = len(f.read())
            f.seek(0)  # reset the file pointer to the beginning of the file
            chunk_size = 1024
            progress = 0

            while True:
                chunk = f.read(chunk_size)

                if not chunk:
                    break
                    print("completed")

                self.textChanged.emit(chunk)
                progress += len(chunk)
                self.progressChanged.emit(progress)




class LeftPane(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # store the instance of DragDrop class as an instance variable

        self.setAcceptDrops(True)

        self.label = QLabel("Drag and drop files here")
        self.label.setAlignment(Qt.AlignCenter)

        self.setMinimumWidth(200)
        self.setMaximumWidth(200)

        self.label.setMinimumWidth(200)
        self.label.setMaximumWidth(200)
        self.label.setStyleSheet("background-color: lightblue")

        self.progress_bar = QProgressBar(self)

        self.progress_bar.setMinimumWidth(200)
        self.progress_bar.setMaximumWidth(200)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.progress_bar)

        self.setLayout(vbox)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = str(url.toLocalFile())

            self.progress_bar.setMaximum(0)
            self.progress_bar.setValue(0)

            reader = FileReader(file_path, self)
            reader.progressChanged.connect(self.progress_bar.setValue)
            reader.textChanged.connect(lambda text: self.parent.right_pane.text_label.setText(
                self.parent.right_pane.text_label.text() + text))

            reader.start()

            filename = file_path.split('/')[-1]
            self.parent.left_pane.label.setText(filename)

        print("done")


class RightPane(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.text_label = QLabel()

        self.text_label.setMinimumWidth(1000)
        self.text_label.setMaximumWidth(1000)
        self.text_label.setStyleSheet

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