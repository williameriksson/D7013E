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


    ratio = 1
    ratio = 1
    smallest_x = float('inf')
    smallest_y = float('inf')
    offset_x = 150 # 10
    offset_y = 150 # 50
    biggest_x = -float('inf')
    biggest_y = -float('inf')

    def __init__(self):
        super(Example, self).__init__()
        self.readInputFile()
        QtGui.QWidget.__init__(self)

        self.bruteButton = QtGui.QPushButton('Brute force', self)
        self.bruteButton.clicked.connect(self.bruteHandler)

        self.miniDiscButton = QtGui.QPushButton('MiniDisc', self)
        self.miniDiscButton.clicked.connect(self.miniDiscHandler)

        self.rectangleButton = QtGui.QPushButton('Rectangle', self)
        self.rectangleButton.clicked.connect(self.rectangleHandler)

        self.randomButton = QtGui.QPushButton('Random', self)
        self.randomButton.clicked.connect(self.randomHandler)

        self.readButton = QtGui.QPushButton('Load', self)
        self.readButton.clicked.connect(self.readHandler)

        self.resetButton = QtGui.QPushButton('Reset', self)
        self.resetButton.clicked.connect(self.resetHandler)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.bruteButton)
        layout.addWidget(self.miniDiscButton)
        layout.addWidget(self.rectangleButton)
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

    def setMaxMin(self):
        for (x, y) in self.pointList:
            x = x * 1.2
            y = y * 1.4
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
        x_ratio = -float('inf')
        y_ratio = -float('inf')

        if (self.biggest_x - self.smallest_x) == 0:
            x_ratio = 1
        else:
            x_ratio = float(self.wWidth - self.offset_x) / (float(self.biggest_x) - float(self.smallest_x))

        if (self.biggest_y - self.smallest_y) == 0:
            y_ratio = 1
        else:
            y_ratio = float(self.wHeight - self.offset_y) / (float(self.biggest_y) - float(self.smallest_y))

        self.ratio = x_ratio if x_ratio < y_ratio else y_ratio

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

    def angleThreePoints(self, p1, p2, p3):
        # Angle between the lines from middle point to the others
        a = (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2
        b = (p2[0]-p3[0])**2 + (p2[1]-p3[1])**2
        c = (p3[0]-p1[0])**2 + (p3[1]-p1[1])**2

        num =  (a + b - c)
        den = math.sqrt(4 * a * b)
        if den != 0:
            fraction = num / den
            if fraction < -1:
                fraction = -1
            if fraction > 1:
                fraction = 1

            res = math.acos( fraction )
            return res
        return 2*math.pi

    def rotatePoint(self, p, c_p, a):
        sin_a = math.sin(-a);
        cos_a = math.cos(-a);
        p = list(p)

        p[0] -= c_p[0];
        p[1] -= c_p[1];

        new_x = p[0] * cos_a - p[1] * sin_a;
        new_y = p[0] * sin_a + p[1] * cos_a;

        p[0] = new_x + c_p[0];
        p[1] = new_y + c_p[1];
        return p;

    def rectArea(self, a, b, c):
        s1 = math.sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 )
        s2 = math.sqrt( (b[0] - c[0])**2 + (b[1] - c[1])**2 )
        return s1 * s2

    def rectangleHandler(self):
        self.convexHandler()

        x_min = float('inf')
        x_max = -float('inf')
        y_min = float('inf')
        y_max = -float('inf')

        # Indices of current evaluation points
        i_p1 = None
        i_p2 = None
        i_p3 = None
        i_p4 = None

        # Get the max and min values, and find the starting supporting points.
        for i in xrange(0, len(self.lineList)):
            p = self.lineList[i]
            x_min = p[0] if p[0] < x_min else x_min
            x_max = p[0] if p[0] > x_max else x_max
            y_min = p[1] if p[1] < y_min else y_min
            y_max = p[1] if p[1] > y_max else y_max

            i_p1 = i if p[0] == x_min else i_p1
            i_p2 = i if p[1] == y_max else i_p2
            i_p3 = i if p[0] == x_max else i_p3
            i_p4 = i if p[1] == y_min else i_p4

        # Define the first rectangle.
        p1_rect = (x_min, y_max)
        p2_rect = (x_max, y_max)
        p3_rect = (x_max, y_min)
        p4_rect = (x_min, y_min)

        # Find the middle point of the rectangle
        cent_r = (x_min + (x_max - x_min) / 2, y_min + (y_max - y_min) / 2)

        total_angle = 0
        smallest_rect = [p1_rect, p2_rect, p3_rect, p4_rect]
        smallest_area = self.rectArea(p1_rect, p2_rect, p3_rect)

        while total_angle < math.pi / 2:
            # Find next index for each supporting point
            i_succ_p1 = i_p1 + 1 if i_p1 + 1 < len(self.lineList) else 0
            i_succ_p2 = i_p2 + 1 if i_p2 + 1 < len(self.lineList) else 0
            i_succ_p3 = i_p3 + 1 if i_p3 + 1 < len(self.lineList) else 0
            i_succ_p4 = i_p4 + 1 if i_p4 + 1 < len(self.lineList) else 0

            angle1 = self.angleThreePoints(p1_rect, self.lineList[i_p1], self.lineList[i_succ_p1])
            angle2 = self.angleThreePoints(p2_rect, self.lineList[i_p2], self.lineList[i_succ_p2])
            angle3 = self.angleThreePoints(p3_rect, self.lineList[i_p3], self.lineList[i_succ_p3])
            angle4 = self.angleThreePoints(p4_rect, self.lineList[i_p4], self.lineList[i_succ_p4])

            smallest_angle = min(angle1, angle2, angle3, angle4)
            total_angle += smallest_angle

            p1 = self.lineList[i_p1]
            p2 = self.lineList[i_p2]
            p3 = self.lineList[i_p3]
            p4 = self.lineList[i_p4]

            # Simulate rotation of the supporting points to baseline counter-clockwise
            temp_p1 = self.rotatePoint(p1, cent_r, -total_angle)
            temp_p2 = self.rotatePoint(p2, cent_r, -total_angle)
            temp_p3 = self.rotatePoint(p3, cent_r, -total_angle)
            temp_p4 = self.rotatePoint(p4, cent_r, -total_angle)

            temp_lst = [temp_p1, temp_p2, temp_p3, temp_p4]

            x_min = float('inf')
            x_max = -float('inf')
            y_min = float('inf')
            y_max = -float('inf')

            # Find the new extreme points, considering only the pseudo supporting points
            for p in temp_lst:
                x_min = p[0] if p[0] < x_min else x_min
                x_max = p[0] if p[0] > x_max else x_max
                y_min = p[1] if p[1] < y_min else y_min
                y_max = p[1] if p[1] > y_max else y_max

            # Define the new rectangle from the new extreme points of the pseudo supporting points
            p1_rect = (x_min, y_max)
            p2_rect = (x_max, y_max)
            p3_rect = (x_max, y_min)
            p4_rect = (x_min, y_min)

            # Rotate the rectangle to its real position clockwise
            p1_rect = self.rotatePoint(p1_rect, cent_r, total_angle)
            p2_rect = self.rotatePoint(p2_rect, cent_r, total_angle)
            p3_rect = self.rotatePoint(p3_rect, cent_r, total_angle)
            p4_rect = self.rotatePoint(p4_rect, cent_r, total_angle)

            # Check which supporting point that should move clockwise and change it
            if angle1 == smallest_angle:
                i_p1 = i_p1 + 1 if i_p1 + 1 <= len(self.lineList) - 1 else 0
            elif angle2 == smallest_angle:
                i_p2 = i_p2 + 1 if i_p2 + 1 <= len(self.lineList) - 1 else 0
            elif angle3 == smallest_angle:
                i_p3 = i_p3 + 1 if i_p3 + 1 <= len(self.lineList) - 1 else 0
            elif angle4 == smallest_angle:
                i_p4 = i_p4 + 1 if i_p4 + 1 <= len(self.lineList) - 1 else 0

            if self.rectArea(p1_rect, p2_rect, p3_rect) < smallest_area:
                smallest_rect = [p1_rect, p2_rect, p3_rect, p4_rect]

        self.lineList = smallest_rect



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

    def minimalDiscTwoPoints(self, a, b):
        c_x = (a[0] + b[0]) / 2
        c_y = (a[1] + b[1]) / 2
        r = math.sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 ) / 2
        return (c_x, c_y, r)

    def outside(self, c_x, c_y, r, p):
        dist = math.sqrt( (c_x - p[0])**2 + (c_y - p[1])**2 )
        if dist > r:
            return True
        return False

    def miniDiscHandler(self):
        start_time = time.time()
        random.shuffle(self.pointList)

        (c_x, c_y, r) = self.minimalDiscTwoPoints(self.pointList[0], self.pointList[1])

        for i in xrange(2, len(self.pointList)):
            p = self.pointList[i]

            if self.outside(c_x, c_y, r, p):
                (c_x, c_y, r) = self.miniDiscWithPoint(self.pointList[0:i], p)

        self.c_mid = (c_x, c_y)
        self.c_radius = r
        stop_time = time.time()
        print "It took: " + str(stop_time - start_time) + 'seconds with ' + str(len(self.pointList)) + 'points'
        QtGui.QWidget.update(self)

    def miniDiscWithPoint(self, lst, q):
        # Need random shuffle lst here? must make copy of list in caller in that case?
        p1 = lst[0]
        (c_x, c_y, r) = self.minimalDiscTwoPoints(p1, q)

        for i in xrange(1, len(lst)):
            p = lst[i]

            if self.outside(c_x, c_y, r, p):
                (c_x, c_y, r) = self.miniDiscWith2Points(self.pointList[0:i], p, q)

        return (c_x, c_y, r)

    def miniDiscWith2Points(self, lst, q1, q2):
        (c_x, c_y, r) = self.minimalDiscTwoPoints(q1, q2)

        for i in xrange(0, len(lst)):
            p = lst[i]

            if self.outside(c_x, c_y, r, p):
                (c_x, c_y, r) = self.smallesCircleThreePoints(q1, q2, p)

        return (c_x, c_y, r)

    def randomHandler(self):
        self.resetHandler()
        random.seed()
        self.pointList = [ ( random.randint(5, self.wWidth - 5), random.randint(5, self.wHeight - 50) ) for k in range(100000) ]

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
        self.resetValues()
        self.setMaxMin()
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        self.drawCircle(qp)
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
            center = QtCore.QPoint(x * self.ratio + self.offset_x, y * self.ratio + self.offset_y)
            qp.drawEllipse(center, radius, radius)

    def drawLines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        s_x = self.smallest_x
        s_y = self.smallest_y
        for tup in self.lineList:
            if (self.lineList.index(tup) + 1 != len(self.lineList)):
                nextTup = self.lineList[self.lineList.index(tup) + 1]
                x_1 = (tup[0]) * self.ratio + self.offset_x
                y_1 = (tup[1]) * self.ratio + self.offset_y
                x_2 = (nextTup[0]) * self.ratio + self.offset_x
                y_2 = (nextTup[1]) * self.ratio + self.offset_y
                qp.drawLine(x_1, y_1, x_2, y_2)
        if len(self.lineList) > 1:
            x_1 = (self.lineList[0][0]) * self.ratio + self.offset_x
            y_1 = (self.lineList[0][1]) * self.ratio + self.offset_y
            x_2 = (self.lineList[-1][0]) * self.ratio + self.offset_x
            y_2 = (self.lineList[-1][1]) * self.ratio + self.offset_y
            qp.drawLine(x_1, y_1, x_2, y_2)
        QtGui.QWidget.update(self)

    def drawCircle(self, qp):
        if self.c_mid and self.c_radius:
            qp.setPen(QtCore.Qt.red)
            qp.setBrush(QtCore.Qt.NoBrush)

            s_x = self.smallest_x
            s_y = self.smallest_y
            x = (self.c_mid[0]) * self.ratio + self.offset_x
            y = (self.c_mid[1]) * self.ratio + self.offset_y

            center = QtCore.QPoint(x, y)
            qp.drawEllipse(center, self.c_radius * self.ratio, self.c_radius * self.ratio)
            QtGui.QWidget.update(self)

    # def mousePressEvent(self, event):
    #     self.pointList.append((event.pos().x(), event.pos().y()))
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
