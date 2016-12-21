import sys, random
from PyQt4 import QtGui, QtCore
from operator import itemgetter

class node():
    def __init__(self, xMid, iMidLeft, iMidRight, lNode = None, rNode = None):
        self.xMid = xMid
        self.lNode = lNode
        self.rNode = rNode
        self.iMidLeft = iMidLeft
        self.iMidRight = iMidRight

class Example(QtGui.QWidget):
    intervalList = []
    inIntervalList = []
    offset = 50
    width = 1000
    height = 1000
    x = -100

    def __init__(self, root, intervals):
        self.root = root
        self.intervalList = intervals
        super(Example, self).__init__()
        QtGui.QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, self.width, self.height)
        self.setWindowTitle('Intervals')
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawIntervals(qp)
        qp.end()


    def mousePressEvent(self, event):
        x = event.pos().x()
        self.x = x
        # print x
        # event.pos().y()
        # print queryTreeFromPoint(self.root, x - self.offset, [])
        self.inIntervalList = queryTreeFromPoint(self.root, self.x - self.offset, [])
        QtGui.QWidget.update(self)

    def drawIntervals(self, qp):
        black_pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        green_pen = QtGui.QPen(QtCore.Qt.green, 2, QtCore.Qt.SolidLine)
        red_pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
        n = 0
        # print self.inIntervalList
        for (start, end) in self.intervalList:
            if (start, end) in self.inIntervalList:
                qp.setPen(green_pen)
            else:
                qp.setPen(black_pen)

            qp.drawLine(start + self.offset, self.offset + n - 5, start + self.offset, self.offset + n + 5)
            qp.drawLine(start + self.offset, self.offset + n, end + self.offset, self.offset + n)
            qp.drawLine(end + self.offset, self.offset + n - 5, end + self.offset, self.offset + n + 5)
            n += 10

        qp.setPen(red_pen)
        qp.drawLine(self.x, self.offset - 20, self.x, self.offset + n + 10)



def makeTree(lst):
    if len(lst) == 0:
        return None

    xMidIndex = len(lst) / 2 - 1
    xMid = lst[xMidIndex][0]

    iMid = []
    iLeft = []
    iRight = []
    for (start, end) in lst:
        if start <= xMid and end >= xMid:
            iMid.append((start, end))
        elif end < xMid:
            iLeft.append((start, end))
        elif start > xMid:
            iRight.append((start, end))

    iMidLeft = iMid
    iMidRight = list(iMid)
    iMidLeft.sort(key=itemgetter(0))
    iMidRight.sort(key=itemgetter(1))

    return node(xMid, iMidLeft, iMidRight, makeTree(iLeft), makeTree(iRight))

def queryTreeFromPoint(v, p, lst = []):
    if v == None:
        return lst

    if p < v.xMid:
        for (start, end) in v.iMidLeft:
            if start <= p and end >= p:
                lst.append((start, end))
            else:
                break
        return queryTreeFromPoint(v.lNode, p, lst)
    else:
        for (start, end) in reversed(v.iMidRight): # Optimize by using indices instead, moving backwards
            if start <= p and end >= p:
                lst.append((start, end))
            else:
                break
        return queryTreeFromPoint(v.rNode, p, lst)

def randomIntervals(start, end, n):
    random.seed()
    startNumbers = [random.randint(start, end - 100) for k in range(n)]
    intervals = []
    for i in startNumbers:
        intervals.append( (i, random.randint(i + 10, end)) )
    return intervals

def main():
    # intervals = [(100,300), (50,200), (250,600), (650, 800), (500, 850), (400, 900)]
    intervals = randomIntervals(0, 900, 40)
    root = makeTree(intervals)
    # print root.xMid
    # print queryTreeFromPoint(root, 3)
    app = QtGui.QApplication(sys.argv)
    ex = Example(root, intervals)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
