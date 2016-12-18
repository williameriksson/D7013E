import random
from operator import itemgetter

class node():
    def __init__(self, largest_left, l_node = None, r_node = None, nrOfPoints = None, maxWeight = None):
        self.largest_left = largest_left
        self.l_node = l_node
        self.r_node = r_node
        self.nrOfPoints = nrOfPoints
        self.maxWeight = maxWeight

class leaf():
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
        self.nrOfPoints = 1
        self.maxWeight = weight # Ugly AF :P

def readInputFile():
    f = open('points', 'r')
    pointList = []
    for line in f:
        pointList.append(int(line))
    pointList.sort()
    return pointList

def makeTree(lst):
    lst.sort(key=itemgetter(0))

    def makeTreeInternal(lst):

        if len(lst) == 1:
            value = lst[0][0]
            weight = lst[0][1]
            return leaf(value, weight)

        if len(lst) == 2:
            l_value = lst[0][0]
            l_weight = lst[0][1]
            r_value = lst[1][0]
            r_weight = lst[1][1]
            return node(l_value, leaf(l_value, l_weight), leaf(r_value, r_weight), 2, max(l_weight, r_weight))

        midIndex = len(lst) / 2
        maxWeight = lst[0][1]

        for (value, weight) in lst:
             maxWeight = max(maxWeight, weight)

        rootNode = node(lst[midIndex - 1][0], makeTreeInternal(lst[0:midIndex]), makeTreeInternal(lst[midIndex: len(lst)]), len(lst), maxWeight)
        return rootNode

    rootn = makeTreeInternal(lst)
    return rootn


def findSplitNode(n, v1, v2):
    while not isinstance(n, leaf) and (v2 <= n.largest_left or v1 > n.largest_left):
        if v2 <= n.largest_left:
            n = n.l_node
        else:
            n = n.r_node
    return n

def oneDRangeQuery(n, v1, v2):
    points = []
    splitNode = findSplitNode(n, v1, v2)

    if isinstance(splitNode, leaf):
        if splitNode.value <= v1 and splitNode.value >= v2:
            points.append((splitNode.value, splitNode.weight))
    else:
        v = splitNode.l_node

        while not isinstance(v, leaf):
            if v1 <= v.largest_left:
                points = getTree(v.r_node) + points
                v = v.l_node
            else:
                v = v.r_node


        if isinstance(v, leaf):
            if v.value >= v1 and v.value <= v2:
                points = [(v.value, v.weight)] + points

        v = findSplitNode(n, v1, v2).r_node
        while not isinstance(v, leaf):
            if v2 >= v.largest_left:
                points += getTree(v.l_node)
                v = v.r_node
            else:
                v = v.l_node

        if isinstance(v, leaf):
            if v.value >= v1 and v.value <= v2:
                points.append((v.value, v.weight))

    return points

def oneDNumberInRange(n, v1, v2):
    splitNode = findSplitNode(n, v1, v2)
    nr = 0
    if isinstance(splitNode, leaf):
        nr = 1

    else:
        v = splitNode.l_node
        nr = splitNode.nrOfPoints
        while not isinstance(v, leaf):
            if v1 <= v.largest_left:
                v = v.l_node
            else:
                nr -= v.l_node.nrOfPoints
                v = v.r_node

        if isinstance(v, leaf):
            if v.value >= v1:
                nr -= 1

        v = findSplitNode(n, v1, v2).r_node
        while not isinstance(v, leaf):
            if v2 >= v.largest_left:
                v = v.r_node
            else:
                nr -= v.r_node.nrOfPoints
                v = v.l_node

        if isinstance(v, leaf):
            if v.value <= v2:
                nr -= 1

    return nr

def oneDMaxWeightInRange(n, v1, v2):
    splitNode = findSplitNode(n, v1, v2)

    if isinstance(splitNode, leaf):
        return splitNode.weight

    def leftHelper(n, v1, v2, maxWeight):
        if isinstance(n, leaf):
            return max(n.weight, maxWeight)

        if v1 <= n.largest_left:
            maxWeight = max(maxWeight, n.r_node.maxWeight)
            return max(maxWeight, leftHelper(n.l_node, v1, v2, maxWeight))

        return leftHelper(n.r_node, v1, v2, maxWeight)

    def rightHelper(n, v1, v2, maxWeight):
        if isinstance(n, leaf):
            if n.value <= v2:
                return max(n.weight, maxWeight)
            return maxWeight

        if v2 >= n.largest_left:
            maxWeight = max(maxWeight, n.l_node.maxWeight)
            return max(maxWeight, rightHelper(n.r_node, v1, v2, maxWeight))

        return rightHelper(n.l_node, v1, v2, maxWeight)

    maxLeft = leftHelper(splitNode.l_node, v1, v2, -float('inf'))
    maxRight = rightHelper(splitNode.r_node, v1, v2, -float('inf'))
    print 'maxLeft', maxLeft
    print 'maxRight', maxRight

    return max(maxLeft, maxRight)

def getTree(n, lst = []):
    if isinstance(n, leaf):
        return lst + [(n.value, n.weight)]
    if not isinstance(n, leaf):
        return getTree(n.l_node, lst) + getTree(n.r_node, lst)


def bruteForceOneDRangeQuery(lst, v1, v2):
    points = []
    lst.sort()

    for x in lst:
        if x >= v1 and x <= v2:
            points.append(x)

    return points

def testSuite():
    i = 1
    while i <= 100:
        lowerRange = 0
        upperRange = 100 * i
        pointList = [random.randint(lowerRange, upperRange) for k in range(10 * i) ]
        v1 = random.randint(lowerRange, upperRange / 2)
        v2 = random.randint(upperRange / 2, upperRange)
        brutePoints = bruteForceOneDRangeQuery(pointList, v1, v2)
        binaryTreePoints = oneDRangeQuery(makeTree(pointList), v1, v2)

        if brutePoints != binaryTreePoints:
            print "FAILURE oneDRangeQuery"
            print brutePoints
            print binaryTreePoints
            return
        i+=1


def main():
    rootNode = makeTree([(10, 0.1), (11, 0.3), (15, 0.2), (18, 0.9), (19, 1.5), (20, 2.4), (25, 0.5), (30, 1.3)])
    # lst = getTree(rootNode)
    # print lst
    # print '\n'
    # print findSplitNode(rootNode, 10, 30).nrOfPoints
    # points = oneDRangeQuery(rootNode, 10, 30)
    # print points
    # testSuite()
    # print oneDNumberInRange(rootNode, 11, 25)
    print oneDMaxWeightInRange(rootNode, 10, 30)
if __name__ == '__main__':
    main()
