from PyQt5 import QtGui, QtCore, QtWidgets


class ProxyStyle(QtWidgets.QProxyStyle):
    def drawControl(self, element, opt, painter, widget):
        if element == QtWidgets.QStyle.CE_TabBarTabLabel:
            ic = self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            r = QtCore.QRect(opt.rect)
            w = 0 if opt.icon.isNull() else opt.rect.width() + self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            r.setHeight(opt.fontMetrics.width(opt.text) + w)
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QtWidgets.QProxyStyle.drawControl(self, element, opt, painter, widget)


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
            if index == 0:
                painter.drawImage(QtCore.QRectF(10, 20, 30, 30), QtGui.QImage("thumbnail/1i.webp"))
            elif index == 1:
                painter.drawImage(QtCore.QRectF(10, 90, 30, 30), QtGui.QImage("thumbnail/2i.webp"))
            elif index == 2:
                painter.drawImage(QtCore.QRectF(10, 160, 30, 30), QtGui.QImage("thumbnail/3i.webp"))
            elif index == 3:
                painter.drawImage(QtCore.QRectF(10, 230, 30, 30), QtGui.QImage("thumbnail/4i.png"))
            elif index == 4:
                painter.drawImage(QtCore.QRectF(10, 300, 30, 30), QtGui.QImage("thumbnail/5i.png"))
            elif index == 5:
                painter.drawImage(QtCore.QRectF(10, 370, 30, 30), QtGui.QImage("thumbnail/6i.png"))
            elif index == 6:
                painter.drawImage(QtCore.QRectF(10, 440,30, 30), QtGui.QImage("thumbnail/7i.webp"))
            elif index == 7:
                painter.drawImage(QtCore.QRectF(10, 510, 30, 30), QtGui.QImage("thumbnail/8i.png"))
            elif index == 8:
                painter.drawImage(QtCore.QRectF(10, 580, 30, 30), QtGui.QImage("thumbnail/9i.png"))
            elif index == 9:
                painter.drawImage(QtCore.QRectF(10, 650, 30, 30), QtGui.QImage("thumbnail/10i.png"))
            elif index == 10:
                painter.drawImage(QtCore.QRectF(10, 720, 30, 30), QtGui.QImage("thumbnail/11i.png"))


    def tabSizeHint(self, index):
        size = QtWidgets.QTabBar.tabSizeHint(self, index)
        size.setHeight = 50
        size.setWidth = 200
        if size.width() < size.height():
            size.transpose()
        return size


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        QtWidgets.QTabWidget.__init__(self, parent)
        self.setTabBar(HorizontalTabBar())
        self.setStyleSheet("QTabBar ::tab { SetAlignment(Qt.AlignLeft); }")
