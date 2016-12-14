class node():
    def __init__(self, largest_left, l_node = None, r_node = None, l_leaf = None, r_leaf = None):
        self.largest_left = largest_left
        self.l_node = l_node
        self.r_node = r_node
        self.l_leaf = l_leaf
        self.r_leaf = r_leaf

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
        return node(lst[0], None, None, leaf(lst[0]), None)

    if len(lst) == 2:
        return node(lst[0], None, None, leaf(lst[0]), leaf(lst[1]))

    midIndex = len(lst) / 2
    rootNode = node(lst[midIndex - 1], makeTree(lst[0:midIndex]), makeTree(lst[midIndex: len(lst)]) )
    return rootNode

def findSplitNode(n, v1, v2):
    while (not n.l_leaf) and (v2 <= n.largest_left or v1 > n.largest_left):
        if v2 <= n.largest_left:
            n = n.l_node
        else:
            n = n.r_node
    return n

def oneDRangeQuery(n, v1, v2):
    splitNode = findSplitNode(n, v1, v2)
    if splitNode.l_leaf:
        if splitNode.l_leaf <= v1:
            print splitNode.l_leaf.value
        if splitNode.r_leaf:
            if splitNode.r_leaf >= v2:
                print splitNode.r_leaf.value
    else:
        v = splitNode.l_node
        orig_v = v
        while v.l_leaf == None:
            if v1 <= v.largest_left:
                printTree(v.r_node)
                v = v.l_node
            else:
                v = v.r_node

        if v.l_leaf:
            if v.l_leaf.value <= v1:
                print v.l_leaf.value

        if v.r_leaf:
            if v.r_leaf.value >= v2:
                print v.r_leaf.value

        v = orig_v
        while v.r_leaf == None:
            if v2 > v.largest_left:
                printTree(v.l_node)
                v = v.r_node
            else:
                v = v.l_node

        if v.l_leaf:
            if v.l_leaf.value <= v1:
                print v.l_leaf.value

        if v.r_leaf:
            if v.r_leaf.value >= v2:
                print v.r_leaf.value



def printTree(n):
    # print 'N', n.largest_left
    if n.l_leaf:
        print n.l_leaf.value
    if n.r_leaf:
        print n.r_leaf.value
    if n.l_node:
        printTree(n.l_node)
    if n.r_node:
        printTree(n.r_node)

def main():
    rootNode = makeTree(readInputFile())
    # printTree(rootNode)
    # print '\n'
    # print findSplitNode(rootNode, 10, 11).largest_left
    oneDRangeQuery(rootNode, 10, 30)

if __name__ == '__main__':
    main()
