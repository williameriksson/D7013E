class node():
    def __init__(self, largest_left, l_node = None, r_node = None):
        self.largest_left = largest_left
        self.l_node = l_node
        self.r_node = r_node

class leaf():
    def __init__(self, value):
        self.value = value

def readInputFile():
    f = open('points', 'r')
    pointList = []
    for line in f:
        pointList.append(int(line))
    pointList.sort()
    return pointList

def makeTree(lst):
    if len(lst) == 1:
        return leaf(lst[0])

    if len(lst) == 2:
        return node(lst[0], leaf(lst[0]), leaf(lst[1]))

    midIndex = len(lst) / 2
    rootNode = node(lst[midIndex - 1], makeTree(lst[0:midIndex]), makeTree(lst[midIndex: len(lst)]) )
    return rootNode

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
            print splitNode.value
    else:
        v = splitNode.l_node

        while not isinstance(v, leaf):
            if v1 <= v.largest_left:
                points += getTree(v.r_node)
                v = v.l_node
            else:
                v = v.r_node


        if isinstance(v, leaf):
            if v.value >= v1 and v.value <= v2:
                points.append(v.value)

        v = findSplitNode(n, v1, v2).r_node
        while not isinstance(v, leaf):
            if v2 >= v.largest_left:
                points += getTree(v.l_node)
                v = v.r_node
            else:
                v = v.l_node

        if isinstance(v, leaf):
            if v.value >= v1 and v.value <= v2:
                points.append(v.value)

    return points

def getTree(n, lst = []):
    if isinstance(n, leaf):
        return lst + [n.value]
    if not isinstance(n, leaf):
        return getTree(n.l_node, lst) + getTree(n.r_node, lst)


def main():
    rootNode = makeTree(readInputFile())
    # lst = getTree(rootNode)
    # print lst
    # print '\n'
    # print findSplitNode(rootNode, 10, 30).largest_left
    points = oneDRangeQuery(rootNode, 10, 30)
    print points


if __name__ == '__main__':
    main()
