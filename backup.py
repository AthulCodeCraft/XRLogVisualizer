import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QGroupBox, QGridLayout, QPushButton

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window GUI')

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Create left part
        left_part = QWidget()
        left_layout = QVBoxLayout()
        left_part.setLayout(left_layout)

        # Create label
        label = QLabel('Left Part')
        left_layout.addWidget(label)

        # Create tab widget
        tab_widget = QTabWidget()

        # Create tab 1
        tab1 = QWidget()
        tab1_layout = QGridLayout()
        tab1.setLayout(tab1_layout)

        # Create planes for tab 1
        plane1 = QPushButton('Plane 1')
        plane2 = QPushButton('Plane 2')
        plane3 = QPushButton('Plane 3')
        plane4 = QPushButton('Plane 4')

        # Add planes to tab 1
        tab1_layout.addWidget(plane1, 0, 0)
        tab1_layout.addWidget(plane2, 0, 1)
        tab1_layout.addWidget(plane3, 1, 0)
        tab1_layout.addWidget(plane4, 1, 1)

        # Add tab 1 to tab widget
        tab_widget.addTab(tab1, 'Tab 1')

        # Create tab 2
        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        tab2.setLayout(tab2_layout)

        # Create planes for tab 2
        plane5 = QPushButton('Plane 5')
        plane6 = QPushButton('Plane 6')

        # Add planes to tab 2
        tab2_layout.addWidget(plane5)
        tab2_layout.addWidget(plane6)

        # Add tab 2 to tab widget
        tab_widget.addTab(tab2, 'Tab 2')

        # Create tab 3 and 4 in the same way as tab 1 and 2

        # Add tab widget to left layout
        left_layout.addWidget(tab_widget)

        # Add left part to main layout
        main_layout.addWidget(left_part)

        # Create right part
        right_part = QWidget()
        right_layout = QVBoxLayout()
        right_part.setLayout(right_layout)

        # Add group box for displaying tab content
        group_box = QGroupBox('Selected Tab Content')
        group_box_layout = QVBoxLayout()
        group_box.setLayout(group_box_layout)

        # Add label for displaying selected tab
        selected_tab_label = QLabel('No Tab Selected')
        group_box_layout.addWidget(selected_tab_label)

        # Add label for displaying selected plane
        selected_plane_label = QLabel('No Plane Selected')
        group_box_layout.addWidget(selected_plane_label)

        # Add group box to right layout
        right_layout.addWidget(group_box)

        # Add right part to main layout
        main_layout.addWidget(right_part)

        # Connect signals and slots
        tab_widget.currentChanged.connect(lambda: self.tab_changed(tab_widget, selected_tab_label))
        plane1.clicked.connect(lambda: self.plane_clicked('Plane 1', selected_plane_label))
        plane2.clicked.connect(lambda: self.plane_clicked('Plane 2', selected_plane_label))

        plane3.clicked.connect(lambda: self.plane_clicked('Plane 3', selected_plane_label))
        plane4.clicked.connect(lambda: self.plane_clicked('Plane 4', selected_plane_label))
        plane5.clicked.connect(lambda: self.plane_clicked('Plane 5', selected_plane_label))
        plane6.clicked.connect(lambda: self.plane_clicked('Plane 6', selected_plane_label))

        def tab_changed(self, tab_widget, selected_tab_label):
            """
            Slot for tab widget currentChanged signal
            """
            selected_tab_label.setText(f'Selected Tab: {tab_widget.currentWidget().title()}')

        def plane_clicked(self, plane_name, selected_plane_label):
            """
            Slot for plane button clicked signal
            """
            selected_plane_label.setText(f'Selected Plane: {plane_name}')


if name == 'main':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
