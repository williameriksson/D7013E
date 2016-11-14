#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, random, math
from PyQt4 import QtGui, QtCore
from operator import itemgetter


class Example(QtGui.QWidget):
    pointList = []
    lineList = []
    firstCircleP = None
    secondCircleP = None
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
        x_c = abs(a[0] - b[0])
        y_c = abs(a[1] - b[1])
        radius = math.sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 ) / 2
        dist =  math.sqrt( (x_c - c[0])**2 + (y_c - c[1])**2 ) / 2

        if dist > radius:
            return True
        return False

    def isOutside(self, a, b, c, d):
        adx = a[0] - d[0];
        ady = a[1] - d[1];
        bdx = b[0] - d[0];
        bdy = b[1] - d[1];
        cdx = c[0] - d[0];
        cdy = c[1] - d[1];
        abdet = adx*bdy - bdx*ady;
        bcdet = bdx*cdy - cdx*bdy;
        cadet = cdx*ady - adx*cdy;
        alift = adx*adx + ady*ady;
        blift = bdx*bdx + bdy*bdy;
        clift = cdx*cdx + cdy*cdy;
        sign = alift*bcdet + blift*cadet + clift*abdet;
        if sign < 0:
            return True
        return False

    def smallesCircleThreePoints(self, a, b, c):
        ab = math.sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 )
        ac = math.sqrt( (a[0] - c[0])**2 + (a[1] - c[1])**2 )
        bc = math.sqrt( (b[0] - c[0])**2 + (b[1] - c[1])**2 )
        if not self.isOutsideThreeP(a, b, c) and ab <= ac and ab <= bc:
            # print a
            # print b
            # print '\n'
            return [a, b]

        if not self.isOutsideThreeP(a, c, b) and ac <= ab and ac <= bc:
            # print a
            # print c
            # print '\n'
            return [a, c]

        # print b
        # print c
        # print '\n'
        return [b, c]

    def bruteHandler(self):
        c_min = self.wHeight + self.wWidth
        point_a = None
        point_b = None

        for a in self.pointList:
            for b in self.pointList:
                if b == a:
                    continue

                c = math.sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 ) / 2 # radius
                for d in self.pointList:
                    if d == a or d == b:
                        continue

                    if self.isOutsideThreeP(a, b, d):
                        print "OUTSIDE"
                        break

                if c < c_min:
                    c_min = c
                    point_a = a
                    point_b = b

        for a in self.pointList:
            for b in self.pointList:
                if b == a:
                    continue

                for c in self.pointList:
                    if c == a or c == b:
                        continue

                tempPoints = self.smallesCircleThreePoints(a, b, c)
                t_first = tempPoints[0]
                t_second = tempPoints[1]
                C = math.sqrt( (t_first[0] - t_second[0])**2 + (t_first[1] - t_second[1])**2 ) / 2

                for d in self.pointList:
                    if d == a or d == b or d == c:
                        continue

                    if self.isOutside(a, b, c, d):
                        print "OUTSIDE2"
                        break

                if C < c_min: # The points are always equal...
                    point_a = t_first
                    point_b = t_second
                    print point_a
                    print point_b
                    print '\n'
                    c_min = C


        self.firstCircleP = point_a
        self.secondCircleP = point_b

    def randomHandler(self):
        self.resetHandler()
        random.seed()
        self.pointList = [ ( random.randint(5, self.wWidth - 5), random.randint(5, self.wHeight - 50) ) for k in range(1000) ]

    def resetHandler(self):
        self.pointList = []
        self.lineList = []
        self.firstCircleP = None
        self.secondCircleP = None
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

    def drawCircle(self, gp):
        if self.firstCircleP and self.secondCircleP:
            gp.setPen(QtCore.Qt.red)
            size = self.size()
            a = self.firstCircleP
            b = self.secondCircleP
            radius = math.sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 ) / 2

            x = abs(a[0] - b[0])
            y = abs(a[1] - b[1])

            center = QtCore.QPoint(x, y)
            gp.drawEllipse(center, radius, radius)
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
