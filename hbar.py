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
                painter.drawImage(QtCore.QRectF(10, 15,40, 40), QtGui.QImage("thumbnail/Img/img1.webp"))
            elif index == 1:
                painter.drawImage(QtCore.QRectF(10, 85, 40, 40), QtGui.QImage("thumbnail/Img/img2.webp"))
            elif index == 2:
                painter.drawImage(QtCore.QRectF(10, 155, 40, 40), QtGui.QImage("thumbnail/Img/img3.webp"))
            elif index == 3:
                painter.drawImage(QtCore.QRectF(10, 220, 40, 40), QtGui.QImage("thumbnail/Img/img4.png"))
            elif index == 4:
                painter.drawImage(QtCore.QRectF(10, 300, 40, 40), QtGui.QImage("thumbnail/Img/img5.png"))
            elif index == 5:
                painter.drawImage(QtCore.QRectF(10, 365, 40, 40), QtGui.QImage("thumbnail/Img/img6.png"))
            elif index == 6:
                painter.drawImage(QtCore.QRectF(10, 440, 40, 40), QtGui.QImage("thumbnail/Img/img7.webp"))
            elif index == 7:
                painter.drawImage(QtCore.QRectF(10, 505, 40, 40), QtGui.QImage("thumbnail/Img/img8.png"))
            elif index == 8:
                painter.drawImage(QtCore.QRectF(10, 572, 40, 40), QtGui.QImage("thumbnail/Img/img9.png"))
            elif index == 9:
                painter.drawImage(QtCore.QRectF(10, 643, 40, 40), QtGui.QImage("thumbnail/Img/img10.png"))
            elif index == 10:
                painter.drawImage(QtCore.QRectF(10, 715, 40, 40), QtGui.QImage("thumbnail/Img/img11.png"))


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
