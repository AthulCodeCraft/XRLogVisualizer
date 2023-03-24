
import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFileDialog, QAction, QMenuBar, QMenu, \
    QHBoxLayout, QScrollArea


class DragDrop(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop")
        self.setGeometry(10, 30, 600, 600)


        self.label = QLabel("Drag and drop files here")
        self.label.setAlignment(Qt.AlignCenter)

        self.text_label = QLabel()
        self.label.setStyleSheet("background-color: lightblue")
        self.text_label.setStyleSheet("background-color: lightgreen")



        self.label.setMaximumWidth(200)


        self.text_label.setMaximumWidth(800)



        hbox = QHBoxLayout()
        hbox.addWidget(self.label)
        hbox.addWidget(self.text_label)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setAcceptDrops(True)

        self.create_menu()

    def create_menu(self):

        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu("File")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)

        file_menu.addAction(open_action)

    def open_file(self):

z        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")

        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                self.text_label.setText(text)
                filename = file_path.split('/')[-1]
                self.label.setText(filename)
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
                filename = file_path.split('/')[-1]

                self.text_label.setText(text)
                self.label.setText(filename)


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
