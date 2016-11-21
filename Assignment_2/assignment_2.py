#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, random, math, time
from PyQt4 import QtGui, QtCore
from operator import itemgetter


class Example(QtGui.QWidget):
    pointList = []
    lineList = []
    c_mid = None
    c_radius = None
    wHeight = 800
    wWidth = 1000

    def __init__(self):
        super(Example, self).__init__()
        self.readInputFile()
        QtGui.QWidget.__init__(self)

        self.bruteButton = QtGui.QPushButton('Brute force', self)
        self.bruteButton.clicked.connect(self.bruteHandler)

        self.randomButton = QtGui.QPushButton('Random', self)
        self.randomButton.clicked.connect(self.randomHandler)

        self.readButton = QtGui.QPushButton('Load', self)
        self.readButton.clicked.connect(self.readHandler)

        self.resetButton = QtGui.QPushButton('Reset', self)
        self.resetButton.clicked.connect(self.resetHandler)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.bruteButton)
        layout.addWidget(self.randomButton)
        layout.addWidget(self.readButton)
        layout.addWidget(self.resetButton)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(layout)
        self.setLayout(vbox)

        self.initUI()

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


    def isOutsideThreeP(self, a, b, c):
        x_c = (a[0] + b[0]) / 2
        y_c = (a[1] + b[1]) / 2
        radius = math.sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 ) / 2
        dist =  math.sqrt( (x_c - c[0])**2 + (y_c - c[1])**2 )

        if dist > radius:
            return True
        return False

    def isOutside(self, x, y, r, d):
        dist = math.sqrt((x - d[0])**2 + (y - d[1])**2)

        if dist > r:
            return True
        return False


    # def isOutside(self, a, b, c, d):
    #     adx = a[0] - d[0];
    #     ady = a[1] - d[1];
    #     bdx = b[0] - d[0];
    #     bdy = b[1] - d[1];
    #     cdx = c[0] - d[0];
    #     cdy = c[1] - d[1];
    #     abdet = adx*bdy - bdx*ady;
    #     bcdet = bdx*cdy - cdx*bdy;
    #     cadet = cdx*ady - adx*cdy;
    #     alift = adx*adx + ady*ady;
    #     blift = bdx*bdx + bdy*bdy;
    #     clift = cdx*cdx + cdy*cdy;
    #     sign = alift*bcdet + blift*cadet + clift*abdet;
    #     if sign < 0:
    #         return True
    #     return False

    def smallesCircleThreePoints(self, a, b, c):
        x1 = a[0]
        x2 = b[0]
        x3 = c[0]
        y1 = a[1]
        y2 = b[1]
        y3 = c[1]

        num_x = (x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)
        den_x = 2 * (x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2)

        if den_x != 0:
            cent_x = num_x / den_x

            num_y = (x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)
            cent_y = num_y / den_x

            r = math.sqrt((cent_x - x1)**2 + (cent_y - y1)**2)
            return (cent_x, cent_y, r)

        return (-1, -1, 9000000)


    def newCircleMidPoint(self, a, b):
        c_x = (a[0] + b[0]) / 2
        c_y = (a[1] + b[1]) / 2
        return (c_x, c_y)

    def bruteHandler(self):
        start_time = time.time()
        self.c_mid = None
        self.c_radius = None
        c_min = self.wHeight + self.wWidth
        c_mid = None
        c_radius = None

        for a in self.pointList:
            for b in self.pointList:
                if b == a:
                    continue

                valid = True
                c = math.sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 ) / 2 # radius
                for d in self.pointList:
                    if d == a or d == b:
                        continue

                    if self.isOutsideThreeP(a, b, d):
                        valid = False
                        break

                if c < c_min and valid:
                    c_min = c
                    c_mid = self.newCircleMidPoint(a, b)
                    c_radius = c

        for a in self.pointList:
            for b in self.pointList:
                if b == a:
                    continue

                for c in self.pointList:
                    if c == a or c == b:
                        continue

                    valid = True
                    (cent_x, cent_y, C) = self.smallesCircleThreePoints(a, b, c)
                    for d in self.pointList:
                        if d == a or d == b or d == c:
                            continue

                        # if self.isOutside(a, b, c, d):
                        #     valid = False
                        #     break

                        if self.isOutside(cent_x, cent_y, C, d):
                            valid = False
                            break

                    if C < c_min and valid:
                        c_min = C
                        c_mid = (cent_x, cent_y)
                        c_radius = C



        self.c_mid = c_mid
        self.c_radius = c_radius
        QtGui.QWidget.update(self)
        stop_time = time.time()
        print "It took: " + str(stop_time - start_time) + 'seconds with ' + str(len(self.pointList)) + 'points'

    def randomHandler(self):
        self.resetHandler()
        random.seed()
        self.pointList = [ ( random.randint(5, self.wWidth - 5), random.randint(5, self.wHeight - 50) ) for k in range(56) ]

    def resetHandler(self):
        self.pointList = []
        self.lineList = []
        self.c_mid = None
        self.c_radius = None
        QtGui.QWidget.update(self)

    def readHandler(self):
        self.readInputFile()
        QtGui.QWidget.update(self)

    def readInputFile(self):
        self.pointList = []
        self.lineList = []
        f = open('points', 'r')
        for line in f:
            cords = line.split()
            self.pointList.append((int(cords[0]), int(cords[1])))

    def initUI(self):

        self.setGeometry(100, 100, self.wWidth, self.wHeight)
        self.setWindowTitle('Convex hull')
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        self.drawCircle(qp)
        # self.drawLines(qp)
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
        if len(self.lineList) > 1:
            qp.drawLine(self.lineList[0][0], self.lineList[0][1], self.lineList[-1][0], self.lineList[-1][1])
        QtGui.QWidget.update(self)

    def drawCircle(self, qp):
        if self.c_mid and self.c_radius:
            qp.setPen(QtCore.Qt.red)
            qp.setBrush(QtCore.Qt.NoBrush)
            size = self.size()
            x = self.c_mid[0]
            y = self.c_mid[1]

            center = QtCore.QPoint(x, y)
            qp.drawEllipse(center, self.c_radius, self.c_radius)
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
