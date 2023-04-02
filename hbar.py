from PyQt5 import QtGui, QtCore, QtWidgets


class HorizontalTabBar(QtWidgets.QTabBar):
    def paintEvent(self, event):

        painter = QtWidgets.QStylePainter(self)
        option = QtWidgets.QStyleOptionTab()
        for index in range(self.count()):
            self.initStyleOption(option, index)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, option)
            painter.drawText(self.tabRect(index),
                             QtCore.Qt.AlignCenter | QtCore.Qt.TextDontClip,
                             self.tabText(index))

    def tabSizeHint(self, index):
        size = QtWidgets.QTabBar.tabSizeHint(self, index)
        if size.width() < size.height():
            size.transpose()
        return size

    #function to add tabicons on the tabs




class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        QtWidgets.QTabWidget.__init__(self, parent)
        self.setTabBar(HorizontalTabBar())




        #set the tab style sheet
        #add style sheet not to children
        #set colur and height
        #add tab icon to the tab


        #self.setStyleSheet("QTabBar::tab:selected { background: #cee7ff; } QTabBar::tab { height: 70px; }")

        #self.setStyleSheet("QTabBar::tab { height: 100px; }, QTabBar::tab:selected { background: #cee7ff  ; }")
        #chnage colur when selected



        #print the height of the tab


