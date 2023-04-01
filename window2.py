from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel
import sys


class RightWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Right Widget")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


class LeftWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Left Widget")

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.West)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tab_widget.addTab(self.tab1, "Tab 1")
        self.tab_widget.addTab(self.tab2, "Tab 2")
        self.tab_widget.addTab(self.tab3, "Tab 3")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        self.tab_widget.currentChanged.connect(self.tab_changed)

    def tab_changed(self, index):
        if index == 0:
            self.right_widget.label.setText("Tab 1 Selected")
        elif index == 1:
            self.right_widget.label.setText("Tab 2 Selected")
        elif index == 2:
            self.right_widget.label.setText("Tab 3 Selected")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Left and Right Widget Example")

        self.left_widget = LeftWidget()
        self.right_widget = RightWidget()

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.left_widget)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.right_widget)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 1700, 500)
    window.show()
    sys.exit(app.exec_())
