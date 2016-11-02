#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial

In the example, we draw randomly 1000 red points
on the window.

author: Jan Bodnar
website: zetcode.com
last edited: September 2011
"""

import sys, random
from PyQt4 import QtGui, QtCore
from operator import itemgetter


class Example(QtGui.QWidget):
    pointList = []
    lineList = []
    def __init__(self):
        super(Example, self).__init__()
        self.readInputFile()
        QtGui.QWidget.__init__(self)

        self.convexButton = QtGui.QPushButton('Compute', self)
        self.convexButton.clicked.connect(self.convexHandler)

        self.readButton = QtGui.QPushButton('Load', self)
        self.readButton.clicked.connect(self.readHandler)

        self.resetButton = QtGui.QPushButton('Reset', self)
        self.resetButton.clicked.connect(self.resetHandler)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.convexButton)
        layout.addWidget(self.readButton)
        layout.addWidget(self.resetButton)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(layout)
        self.setLayout(vbox)


        self.initUI()

    def leftTurn(self, first, second, third):
        if (first[1] > second[1] and second[1] < third[1]):
            return True
        return False

    def convexHandler(self):
        upper = []
        lower = []
        self.pointList.sort(key=itemgetter(0,1))
        # upper.append(self.pointList[0])
        # upper.append(self.pointList[1])
        # for (i in range(2, self.pointList.len())):
        #     upper.append(self.pointList[i])
        #     while (upper.len() > 2 and self.leftTurn(upper[-2], upper[-1])):
        #         del upper[-2]


        for tup in self.pointList:
            upper.append(tup)
            while (len(upper) > 2 and self.leftTurn(upper[-3], upper[-2], upper[-1])):
                del upper[-2]

        for tup in reversed(self.pointList):
            lower.append(tup)
            while (len(lower) > 2 and self.leftTurn(lower[-3], lower[-2], lower[-1])):
                del lower[-2]

        del lower[0]
        del lower[-1]

        self.lineList = upper + lower


        print self.lineList


    def resetHandler(self):
        self.pointList = []
        self.lineList = []
        QtGui.QWidget.update(self)

    def readHandler(self):
        self.readInputFile()
        QtGui.QWidget.update(self)

    def readInputFile(self):
        f = open('points', 'r')
        for line in f:
            cords = line.split()
            self.pointList.append((int(cords[0]), int(cords[1])))

    def initUI(self):

        self.setGeometry(100, 100, 1000, 800)
        self.setWindowTitle('Convex hull')
        self.show()

    def paintEvent(self, e):
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
            center = QtCore.QPoint(x, y)
            qp.drawEllipse(center, radius, radius)

    def drawLines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        for tup in self.lineList:
            if (self.lineList.index(tup) + 1 != len(self.lineList)):
                nextTup = self.lineList[self.lineList.index(tup) + 1]
                qp.drawLine(tup[0], tup[1], nextTup[0], nextTup[1])
        QtGui.QWidget.update(self)

    def mousePressEvent(self, event):
        self.pointList.append((event.pos().x(), event.pos().y()))
        QtGui.QWidget.update(self)

    # def mouseReleaseEvent(self, QMouseEvent):
    #     cursor =QtGui.QCursor()
    #     print cursor.pos()



def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
