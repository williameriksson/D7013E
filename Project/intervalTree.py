from operator import itemgetter
class node():
    def __init__(self, xMid, iMidLeft, iMidRight, lNode = None, rNode = None):
        self.xMid = xMid
        self.lNode = lNode
        self.rNode = rNode
        self.iMidLeft = iMidLeft
        self.iMidRight = iMidRight


def makeTree(lst):
    if len(lst) == 0:
        return None

    xMidIndex = len(lst) / 2 - 1
    xMid = lst[xMidIndex][0]

    iMid = []
    iLeft = []
    iRight = []
    for (start, end) in lst:
        if start <= xMid and end >= end:
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


root = makeTree([(1,8), (2,4), (3,9), (9,12), (10, 14), (16, 20)])
# print root.xMid
print queryTreeFromPoint(root, 3)
