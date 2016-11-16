#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, random
from PyQt4 import QtGui, QtCore
from operator import itemgetter


class Example(QtGui.QWidget):
    pointList = []
    lineList = []
    ratio_x = 1
    ratio_y = 1
    smallest_x = float('inf')
    smallest_y = float('inf')
    wHeight = 800
    wWidth = 1000
    offset_x = 10
    offset_y = 50
    biggest_x = -float('inf')
    biggest_y = -float('inf')

    def __init__(self):
        super(Example, self).__init__()
        self.readInputFile()
        QtGui.QWidget.__init__(self)

        self.convexButton = QtGui.QPushButton('Compute', self)
        self.convexButton.clicked.connect(self.convexHandler)

        self.randomButton = QtGui.QPushButton('Random', self)
        self.randomButton.clicked.connect(self.randomHandler)

        self.readButton = QtGui.QPushButton('Load', self)
        self.readButton.clicked.connect(self.readHandler)

        self.resetButton = QtGui.QPushButton('Reset', self)
        self.resetButton.clicked.connect(self.resetHandler)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.convexButton)
        layout.addWidget(self.randomButton)
        layout.addWidget(self.readButton)
        layout.addWidget(self.resetButton)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(layout)
        self.setLayout(vbox)

        self.initUI()

    def resetValues(self):
        self.smallest_y = float('inf')
        self.smallest_x = float('inf')
        self.biggest_x = -float('inf')
        self.biggest_y = -float('inf')

    def leftTurn(self, f, s, t):
        res = (s[0] - f[0]) * (t[1] - f[1]) - (s[1] - f[1]) * (t[0] - f[0])
        if res > 0:
            return True
        return False

    def convexHandler(self):
        upper = []
        lower = []
        self.pointList.sort(key=itemgetter(0,1))

        lastTup = None
        for tup in self.pointList:
            if tup != lastTup:
                upper.append(tup)
                while (len(upper) > 2 and self.leftTurn(upper[-3], upper[-2], upper[-1])):
                    del upper[-2]
            lastTup = tup

        lastTup = None
        for tup in reversed(self.pointList):
            if tup != lastTup:
                lower.append(tup)
                while (len(lower) > 2 and self.leftTurn(lower[-3], lower[-2], lower[-1])):
                    del lower[-2]
            lastTup = tup

        del lower[0]
        del lower[-1]

        self.lineList = upper + lower


    def randomHandler(self):
        self.resetHandler()
        random.seed()
        self.pointList = [ ( random.randint(5, self.wWidth - 5), random.randint(5, self.wHeight - 50) ) for k in range(1000) ]

    def resetHandler(self):
        self.pointList = []
        self.lineList = []
        QtGui.QWidget.update(self)

    def readHandler(self):
        self.readInputFile()
        QtGui.QWidget.update(self)

    def setMaxMin(self):
        for (x, y) in self.pointList:
            if x < self.smallest_x:
                self.smallest_x = x

            if x > self.biggest_x:
                self.biggest_x = x

            if y < self.smallest_y:
                self.smallest_y = y

            if y > self.biggest_y:
                self.biggest_y = y

        self.calcRatios()


    def calcRatios(self):
        if (self.biggest_x - self.smallest_x) == 0:
            self.ratio_x = 1
        else:
            self.ratio_x = float(self.wWidth - self.offset_x) / (float(self.biggest_x) - float(self.smallest_x))

        if (self.biggest_y - self.smallest_y) == 0:
            self.ratio_y = 1
        else:
            self.ratio_y = float(self.wHeight - self.offset_y) / (float(self.biggest_y) - float(self.smallest_y))

    def readInputFile(self):
        self.pointList = []
        self.lineList = []
        f = open('points', 'r')
        for line in f:
            cords = line.split()
            cords[0] = float(cords[0])
            cords[1] = float(cords[1])
            self.pointList.append((float(cords[0]), float(cords[1])))



    def initUI(self):

        self.setGeometry(100, 100, self.wWidth + self.offset_x + 5, self.wHeight + self.offset_y + 5)
        self.setWindowTitle('Convex hull')
        self.show()

    def paintEvent(self, e):
        self.resetValues()
        self.setMaxMin()
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        self.drawLines(qp)
        qp.end()

    def drawPoints(self, qp):
        qp.setPen(QtCore.Qt.red)
        qp.setBrush(QtCore.Qt.red)
        size = self.size()
        radius = 3

        for pointTuple in self.pointList:
            x = pointTuple[0]
            y = pointTuple[1]
            center = QtCore.QPoint((x - self.smallest_x) * self.ratio_x + self.offset_x, (y - self.smallest_y) * self.ratio_y + self.offset_y)
            qp.drawEllipse(center, radius, radius)

    def drawLines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        s_x = self.smallest_x
        s_y = self.smallest_y
        for tup in self.lineList:
            if (self.lineList.index(tup) + 1 != len(self.lineList)):
                nextTup = self.lineList[self.lineList.index(tup) + 1]
                x_1 = (tup[0] - s_x) * self.ratio_x + self.offset_x
                y_1 = (tup[1] - s_y) * self.ratio_y + self.offset_y
                x_2 = (nextTup[0] - s_x) * self.ratio_x + self.offset_x
                y_2 = (nextTup[1] - s_y) * self.ratio_y + self.offset_y
                qp.drawLine(x_1, y_1, x_2, y_2)
        if len(self.lineList) > 1:
            x_1 = (self.lineList[0][0] - s_x) * self.ratio_x + self.offset_x
            y_1 = (self.lineList[0][1] - s_y) * self.ratio_y + self.offset_y
            x_2 = (self.lineList[-1][0] - s_x) * self.ratio_x + self.offset_x
            y_2 = (self.lineList[-1][1] - s_y) * self.ratio_y + self.offset_y
            qp.drawLine(x_1, y_1, x_2, y_2)
        QtGui.QWidget.update(self)

    # def mousePressEvent(self, event):
    #     s_x = abs(self.smallest_x)
    #     s_y = abs(self.smallest_y)
    #     self.pointList.append(((event.pos().x() - s_x) * self.ratio_x + self.offset_x , (event.pos().y() - s_y) * self.ratio_y + self.offset_y ))
    #     QtGui.QWidget.update(self)

    # def mouseReleaseEvent(self, QMouseEvent):
    #     cursor =QtGui.QCursor()
    #     print cursor.pos()



def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
