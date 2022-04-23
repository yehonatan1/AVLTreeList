# username - yehonatanr
# id1      - 328137385
# name1    - Yehonatan Rokach
# id2      - 209861806
# name2    - Uri Ben Dor


"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

	@type value: str
	@param value: data of your node
	"""

    def __init__(self, value, vir=False):
        self.value = value
        if not vir:
            self.left = AVLNode(None, True)
            self.right = AVLNode(None, True)
            self.parent = AVLNode(None, True)
            self.left.setParent(self)
            self.right.setParent(self)
            self.height = 0
            self.size = 1
        else:
            self.left = None
            self.right = None
            self.parent = None
            self.height = -1
            self.size = 0

    def __str__(self):
        return 'virtual: ' + str(not self.isRealNode()) + ',\tval: ' + str(self.value) + ',\theight: ' + str(
            self.height) + ',\tsize: ' + str(self.size) + '.'

    """returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child
	"""

    def getLeft(self):
        if self.left.isRealNode(): return self.left
        return None

    """returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child
	"""

    def getRight(self):
        if self.right.isRealNode(): return self.right
        return None

    """returns the parent 

x	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""

    def getParent(self):
        if self.parent.isRealNode(): return self.parent
        return None

    """return the value

	@rtype: str
	@returns: the value of self, None if the node is virtual
	"""

    def getValue(self):
        return self.value

    """returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""

    def getHeight(self):
        return self.height

    """returns the size

	@rtype: int
	@returns: the size of self, 0 if the node is virtual
	"""

    def getSize(self):
        return self.size

    """returns the index

	@rtype: int
	@returns: the index of self
	"""

    def getIndex(self):
        if not self.isRealNode(): return -1
        index = self.left.getSize()
        node = self
        while node.parent.isRealNode():
            if node.parent.right is node: index += node.parent.left.getSize() + 1
            node = node.parent
        return index

    """
    @returns: the number of suns that a node has
    """

    def numberOfSons(self):
        if not self.isRealNode():
            # print("Can't get the amount of sons of a virtual node")
            return -1

        Sum = 0
        if self.left.isRealNode(): Sum += 1
        if self.right.isRealNode(): Sum += 1
        return Sum

    """retrieves the node i'th node in the sub tree

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: AVLNode
    @returns: the i'th node in the sub tree
    """

    def retrieve_node(self, i):
        if not 0 <= i < self.size:
            # print("Retrieve Index out of range")
            return AVLNode(None, True)
        index = self.left.getSize()  # The size of the node
        if index == i:
            return self
        if index > i:
            return self.left.retrieve_node(i)
        else:
            return self.right.retrieve_node(i - index - 1)

    """
    @returns the minimum (the most left node) index on a tree
    """

    def getMinimum(self):
        if not self.isRealNode():
            # print("Can't get the minimum of a virtual node")
            return -1
        Min = self
        while Min.left.isRealNode():
            Min = Min.left
        return Min

    """
    @return the successor of self in a node
    """

    def getSuccessor(self):
        if self.isRealNode():
            if self.right.isRealNode():
                return self.right.getMinimum()
            else:
                parent = self.parent
                while parent.isRealNode() and self is parent.right:
                    self = parent
                    parent = self.parent
                if parent.isRealNode():
                    return parent
                else:
                    # print("Error can't get the successor of the maximum value")
                    return -1

        # print("Error can't get the successor of a virtual node")
        return -1


    """returns the balance factor
    
    @rtype: int
    @returns: the balance factor of self
    """


    def getBF(self) -> int:
        if not self.isRealNode(): return 0
        return self.left.getHeight() - self.right.getHeight()


    """returns the root of the tree
    
    @rtype: AVLNode
    @returns: the root of the tree
    """


    def getRoot(self):
        if not self.isRealNode():
            # print("GET ROOT ERROR")
            return self
        node = self
        while not node.isRoot(): node = node.parent
        return node


    """"disconnect self from parent"""


    def disconnectParent(self, fixParent=True):
        if not self.isRoot() and (self.isRealNode() or not self.parent is None):
            if self.parent.left is self:
                self.parent.left = AVLNode(None, True)
                self.parent.left.parent = self.parent
            else:
                self.parent.right = AVLNode(None, True)
                self.parent.right.parent = self.parent

            if fixParent: self.parent.fix()
            self.parent = AVLNode(None, True)


    """"disconnect self from tree"""


    def disconnect(self):
        self.disconnectParent()

        if self.left.isRealNode(): self.left.parent = AVLNode(None, True)
        self.left = AVLNode(None, True)
        self.left.parent = self

        if self.right.isRealNode(): self.right.parent = AVLNode(None, True)
        self.right = AVLNode(None, True)
        self.right.parent = self


    """sets left child
    
        @type node: AVLNode
        @param node: a node
        """


    def setLeft(self, node):
        self.left.disconnectParent(False)
        node.disconnectParent(False)
        self.left = node
        node.setParent(self)


    """sets right child
    
    @type node: AVLNode
    @param node: a node
    """


    def setRight(self, node):
        self.right.disconnectParent(False)
        node.disconnectParent(False)
        self.right = node
        node.setParent(self)


    """pushes self between node and node.parent and set nodes as self left child
    
    @type node: AVLNode
    @param node: a node
    """


    def pushLeft(self, node):
        if self.left.isRealNode():
            self.left.parent = AVLNode(None, True)
        else:
            self.left.parent = None
        self.left = node
        if node.parent.isRealNode() and not self.parent.isRealNode():
            if node.parent.left is node:
                node.parent.left = self
            else:
                node.parent.right = self
            self.parent = node.parent
        node.setParent(self)


    """pushes self between node and node.parent and set nodes as self right child
    
    @type node: AVLNode
    @param node: a node
    """


    def pushRight(self, node):
        if self.right.isRealNode():
            self.right.parent = AVLNode(None, True)
        else:
            self.right.parent = None
        self.right = node
        if node.parent.isRealNode() and not self.parent.isRealNode():
            if node.parent.left is node:
                node.parent.left = self
            else:
                node.parent.right = self
            self.parent = node.parent
        node.setParent(self)


    """sets parent
    
    @type node: AVLNode
    @param node: a node
    """


    def setParent(self, node):
        self.parent = node


    """fix node's size for all nodes from self upwards
    @rtype: int
    @returns: the number of height changes
    
    """


    def fix(self):
        if self.isRealNode():
            size = self.left.getSize() + self.right.getSize() + 1
            if self.size == size: return
            self.setSize(size)
            self.parent.fix()


    """sets value
    
    @type value: str
    @param value: data
    """


    def setValue(self, value):
        self.value = value


    """sets the height of the node
    
    @type h: int
    @param h: the height
    """


    def setHeight(self, h):
        self.height = h


    """sets the size of the node
    
        @type s: int
        @param s: the size
    """


    def setSize(self, s):
        self.size = s


    """returns whether self is not a virtual node 
    
    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """


    def isRealNode(self):
        return self.height != -1


    """returns whether self is a leaf 
    
    @rtype: bool
    @returns: true iff self is a leaf and self isn't a virtual node
    """


    def isLeaf(self):
        return self.isRealNode() and not (self.left.isRealNode() or self.right.isRealNode())


    """returns whether self is the root
    
    @rtype: bool
    @returns: true iff self is a root and self isn't a virtual node
    """


    def isRoot(self):
        return self.isRealNode() and not self.parent.isRealNode()


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
	Constructor, you are allowed to add more fields.

	"""

    def __init__(self, root = AVLNode(None, True)):
        self.root = root

    # add your fields here

    """returns whether the list is empty

	@rtype: bool
	@returns: True if the list is empty, False otherwise
	"""

    def empty(self):
        return self.length() == 0

    """retrieves the node i'th node in the tree

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: AVLNode
    @returns: the i'th node in the tree
    """

    def retrieve_node(self, i):
        return self.root.retrieve_node(i)

    """retrieves the value of the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the value of the i'th item in the list
    """

    def retrieve(self, i):
        return self.retrieve_node(i).value

    """inserts val at position i in the list

    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, i, val):
        if self.length() == 0:
            if i != 0: raise IndexError
            self.root = AVLNode(val)
            return 0
        node = AVLNode(val)
        if i < self.length():
            tmp = self.retrieve_node(i)
            if not tmp.left.isRealNode():
                tmp.setLeft(node)
            else:
                tmp = tmp.left
                while tmp.right.isRealNode(): tmp = tmp.right
                tmp.setRight(node)
        elif i == self.length():
            tmp = self.root
            while tmp.right.isRealNode(): tmp = tmp.right
            tmp.setRight(node)
        else:
            return -1
        node.parent.fix()
        balan =  fix1(node.parent)
        self.root = node.getRoot()
        return balan

    """deletes the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i):
        if not self.root.isRealNode() or not 0 <= i < self.length():
            return -1

        node = self.retrieve_node(i)
        parent = node.getParent()

        if not node.isRealNode():
            # print("Can't delete a virtual node")
            return -1

        if node is self.root:
            if node.isLeaf():
                self.root.disconnect()
                self.root = AVLNode(None, True)
                return 0
            elif node.numberOfSons() == 1:
                node.setHeight(0)
                node.setSize(1)
                if self.root.left.isRealNode():
                    self.root = self.root.left
                    self.root.disconnectParent()
                    return 0
                else:
                    self.root = self.root.right
                    self.root.disconnectParent()
                    return 0
            else:
                successor = node.getSuccessor()
                n = self.delete(successor.getIndex())
                if not node.isRoot(): node.parent.setRight(successor)
                successor.setLeft(node.left)
                successor.setRight(node.right)
                successor.setSize(node.getSize())
                successor.setHeight(node.getHeight())
                node.setHeight(0)
                node.setSize(1)
                self.root = successor.getRoot()
                return n
                # x = successor.parent
                # successor.parent = AVLNode(None, True)
                # if x.right is successor:
                #     x.right = AVLNode(None, True)
                #     x.right.parent = x
                # else:
                #     x.left = AVLNode(None, True)
                #     x.left.parent = x
                # x = x.left
                # successor.left = self.root.left
                # successor.left.parent = successor
                # self.root.left = AVLNode(None, True)
                # successor.right = self.root.right
                # successor.right.parent = successor
                # self.root.right = AVLNode(None, True)
                # self.root = successor
                # x = x.parent
                # n = x.fix()
                # return n + fix(x)

        if node.isLeaf():
            node.disconnectParent()
        elif node.numberOfSons() == 1:
            if parent.getRight() is node:
                if node.right.isRealNode():
                    parent.setRight(node.right)
                else:
                    parent.setRight(node.left)
            else:
                if node.right.isRealNode():
                    parent.setLeft(node.right)
                else:
                    parent.setLeft(node.left)
        else:
            successor = node.getSuccessor()
            n = self.delete(successor.getIndex())
            successor.setLeft(node.left)
            successor.setRight(node.right)
            parent = node.parent
            if parent.getRight() is node:
                parent.setRight(successor)
            else:
                parent.setLeft(successor)
            successor.setHeight(node.getHeight())
            successor.setSize(node.getSize())
            node.setHeight(0)
            node.setSize(1)
            return n
            # tmp = successor.parent
            # if parent.getRight() is node:
            #     parent.setRight(successor)
            # else:
            #     parent.setLeft(successor)
            #
            # successor.setRight(node.right)
            # successor.setLeft(node.left)
            # successor.setSize(successor.left.getSize() + successor.right.getSize() + 1)
            # successor.setHeight(max(successor.left.getHeight(), successor.right.getHeight()) + 1)

        parent.fix()
        balan = fix(parent)
        self.root = parent.getRoot()
        return balan

    """returns the value of the first item in the list

    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        if self.empty():
            return None
        return self.retrieve(0)

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        if self.empty():
            return None
        return self.retrieve(self.length() - 1)

        """returns an array representing list 

        @rtype: list
        @returns: a list of strings representing the data structure
        """

    def listToArray(self):
        arr = []
        if self.empty():
            return arr

        def rec(node, index, array):
            if node.left.isRealNode():
                array[index - node.left.right.getSize() - 1] = node.left
                rec(node.left, index - node.left.right.getSize() - 1, array)
            if node.right.isRealNode():
                array[index + node.right.left.getSize() + 1] = node.right
                rec(node.right, index + node.right.left.getSize() + 1, array)

        arr = [None for i in range(self.length())]
        index = self.root.getIndex()
        arr[index] = self.root
        rec(self.root, index, arr)
        return [node.getValue() for node in arr]

    """returns the size of the list 

    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return self.root.getSize()

    """splits the list at the i'th index

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list according to whom we split
    @rtype: list
    @returns: a list [left, val, right], where left is an AVLTreeList representing the list until index i-1,
    right is an AVLTreeList representing the list from index i+1, and val is the value at the i'th index.
    """

    def split(self, i):
        if self.root.getIndex() == i:
            if self.root.left.isRealNode():
                L = self.root.left
            else:
                L = AVLNode(None, True)
            L.disconnectParent()
            left = AVLTreeList(L)

            if self.root.right.isRealNode():
                R = self.root.right
            else:
                R = AVLNode(None, True)
            R.disconnectParent()
            right = AVLTreeList(R)

            return [left, self.root.getValue(), right]

        node = self.retrieve_node(i)
        val = node.getValue()
        L = node.left
        R = node.right
        L.disconnectParent()
        R.disconnectParent()
        parent = node.parent
        right = parent.right is node
        node = parent
        while not node.isRoot():
            parent = node.parent
            r = parent.right is node
            if right:
                L = join(node.left, L, node)
            else:
                R = join(R, node.right, node)
            right = r
            node = parent
        if right:
            L = join(node.left, L, node)
        else:
            R = join(R, node.right, node)

        left = AVLTreeList(L)
        right = AVLTreeList(R)

        return [left, val, right]

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        if self.empty():
            self.root = lst.root
            return self.root.getHeight() + 1
        result = abs(self.root.getHeight() - lst.root.getHeight())
        i = self.length() - 1
        node = self.retrieve_node(i)
        self.delete(i)
        self.root = join(self.root, lst.root, node)
        return result

    """searches for a *value* in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        lst = self.listToArray()
        try:
            return lst.index(val)
        except ValueError:
            return -1

    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        if self.root.isRealNode(): return self.root
        return None

    ######################################## Put these functions ########################################
    ##################################### inside AVLTreeList class ######################################

    """Checks if the AVL tree properties are consistent

    @rtype: boolean 
    @returns: True if the AVL tree properties are consistent
    """

    def check(self):
        if not self.isAVL():
            print("The tree is not an AVL tree!")
        if not self.isSizeConsistent():
            print("The sizes of the tree nodes are inconsistent!")
        if not self.isHeightConsistent():
            print("The heights of the tree nodes are inconsistent!")
        if not self.isRankConsistent():
            print("The ranks of the tree nodes are inconsistent!")

    """Checks if the tree is an AVL

    @rtype: boolean 
    @returns: True if the tree is an AVL tree
    """

    def isAVL(self):
        return self.isAVLRec(self.getRoot())

    """Checks if the subtree is an AVL
    @type x: AVLNode
    @param x: The root of the subtree
    @rtype: boolean 
    @returns: True if the subtree is an AVL tree
    """

    def isAVLRec(self, x):
        # If x is a virtual node return True
        if x is None or not x.isRealNode():
            return True
        # Check abs(balance factor) <= 1
        bf = x.getBF()
        if bf > 1 or bf < -1:
            return False
        # Recursive calls
        return self.isAVLRec(x.getLeft()) and self.isAVLRec(x.getRight())

    """Checks if sizes of the nodes in the tree are consistent

    @rtype: boolean 
    @returns: True if sizes of the nodes in the tree are consistent
    """

    def isSizeConsistent(self):
        return self.isSizeConsistentRec(self.getRoot())

    """Checks if sizes of the nodes in the subtree are consistent

    @type x: AVLNode
    @param x: The root of the subtree
    @rtype: boolean 
    @returns: True if sizes of the nodes in the subtree are consistent
    """

    def isSizeConsistentRec(self, x):
        # If x is a virtual node return True
        if x is None or not x.isRealNode():
            return True
        # Size of x should be x.left.size + x.right.size + 1
        if x.getSize() != (x.getLeft().getSize() + x.getRight().getSize() + 1):
            return False
        # Recursive calls
        return self.isSizeConsistentRec(x.getLeft()) and self.isSizeConsistentRec(x.getRight())

    """Checks if heights of the nodes in the tree are consistent

    @rtype: boolean 
    @returns: True if heights of the nodes in the tree are consistent
    """

    def isHeightConsistent(self):
        return self.isHeightConsistentRec(self.getRoot())

    """Checks if heights of the nodes in the subtree are consistent

    @type x: AVLNode
    @param x: The root of the subtree
    @rtype: boolean 
    @returns: True if heights of the nodes in the subtree are consistent
    """

    def isHeightConsistentRec(self, x):
        # If x is a virtual node return True
        if x is None or not x.isRealNode():
            return True
        # Height of x should be maximum of children heights + 1
        if x.getHeight() != max(x.getLeft().getHeight(), x.getRight().getHeight()) + 1:
            return False
        # Recursive calls
        return self.isHeightConsistentRec(x.getLeft()) and self.isHeightConsistentRec(x.getRight())

    """Checks if the ranks of the nodes in the tree are consistent

    @returns: True if the ranks of the nodes in the tree are consistent
    """

    def isRankConsistent(self):
        root = self.getRoot()
        for i in range(1, root.getSize()):
            if i != self.rank(self.select(i)):
                return False
        nodesList = self.nodes()
        for node in nodesList:
            if node != self.select(self.rank(node)):
                return False
        return True

    """Returns a list of the nodes in the tree sorted by index in O(n)

    @rtype: list
    @returns: A list of the nodes in the tree sorted by index
    """

    def nodes(self):
        lst = []
        self.nodesInOrder(self.getRoot(), lst)
        return lst

    """Adds the nodes in the subtree to the list
     following an in-order traversal in O(n)

    @type x: AVLNode
    @type lst: list
    @param x: The root of the subtree
    @param lst: The list
    """

    def nodesInOrder(self, x, lst):
        if x is None or not x.isRealNode():
            return
        self.nodesInOrder(x.getLeft(), lst)
        lst.append(x)
        self.nodesInOrder(x.getRight(), lst)

    def append(self, val): return self.insert(self.length(), val)


###################################################### printree ######################################################
###################################################### function ######################################################

def printree(t, bykey=False):
    """Print a textual representation of t
    bykey=True: show keys instead of values"""
    return trepr(t, t.getRoot(), bykey)

def trepr(t, node, bykey=False):
    """Return a list of textual representations of the levels in t
    bykey=True: show keys instead of values"""
    if node is None or not node.isRealNode():  # You might want to change this, depending on your implementation
        return ["#"]  # Hashtag marks a virtual node

    thistr = str(node.getValue())

    return conc(trepr(t, node.getLeft(), bykey), thistr, trepr(t, node.getRight(), bykey))

def conc(left, root, right):
    """Return a concatenation of textual representations of
    a root node, its left node, and its right node
    root is a string, and left and right are lists of strings"""

    lwid = len(left[-1])
    rwid = len(right[-1])
    rootwid = len(root)

    result = [(lwid + 1) * " " + root + (rwid + 1) * " "]

    ls = leftspace(left[0])
    rs = rightspace(right[0])
    result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

    for i in range(max(len(left), len(right))):
        row = ""
        if i < len(left):
            row += left[i]
        else:
            row += lwid * " "

        row += (rootwid + 2) * " "

        if i < len(right):
            row += right[i]
        else:
            row += rwid * " "

        result.append(row)

    return result

def leftspace(row):
    """helper for conc"""
    # row is the first row of a left node
    # returns the index of where the second whitespace starts
    i = len(row) - 1
    while row[i] == " ":
        i -= 1
    return i + 1

def rightspace(row):
    """helper for conc"""
    # row is the first row of a right node
    # returns the index of where the first whitespace ends
    i = 0
    while row[i] == " ":
        i += 1
    return i

##################################################################################################
##################################################################################################


def checkPointers(lst):
    if  lst.getRoot() is None: return True
    if not lst.getRoot() is lst.getRoot().getRoot():
        print('Root Error')
        return False
    def rec(node):
        if node is None: return True
        if not node.left.getParent() is node:
            print('Left Child Error')
            print('Parent:\t' + str(node.getValue()) + '\t\tChild:\t' + str(node.getLeft().getValue()) + '\t\tChild parent:\t' + str(node.getLeft().getParent().getValue()))
            return False
        if not node.right.getParent() is node:
            print('Right Child Error')
            print('Parent:\t' + str(node.getValue()) + '\t\tChild:\t' + str(node.getRight().getValue()) + '\t\tChild parent:\t' + str(node.getRight().getParent().getValue()))
            return False
        return rec(node.getLeft()) and rec(node.getRight())

    return rec(lst.getRoot())

def checkTree(lst):
    if lst.getRoot() is None: return True
    if not (checkPointers(lst) and lst.isAVL()):
        if not lst.isAVL: print("AVL ERROR")
        return False
    def rec(node):
        if not node.isRealNode(): return node.getSize() == 0 and node.getHeight() == -1
        if node.getSize() != node.left.getSize() + node.right.getSize() + 1:
            print("SIZE ERROR")
            print('Parent:\t' + str(node.getValue()) + '\t\tLeft Child:\t' + str(node.getLeft().getValue()) + '\t\tRight Child:\t' + str(node.getRight().getValue()))
            return False
        if node.getHeight() != max(node.left.getHeight(), node.right.getHeight()) + 1:
            print("HEIGHT ERROR")
            print('Parent:\t' + str(node.getValue()) + '\t\tLeft Child:\t' + str(node.getLeft().getValue()) + '\t\tRight Child:\t' + str(node.getRight().getValue()))
            return False
        return rec(node.left) and rec(node.right)
    return rec(lst.getRoot())

##################################################################################################
##################################################################################################

"""rotate right
@type node: AVLNode
@pre: node.right.IsRealNode()

"""

def RightRotation(node):
    son = node.left
    node.setLeft(son.right)
    if node.isRoot(): son.setRight(node)
    else:
        parent = node.parent
        if parent.right is node: parent.setRight(son)
        else: parent.setLeft(son)
        son.setRight(node)

    node.setSize(node.left.getSize() + node.right.getSize() + 1)
    node.setHeight(max(node.left.getHeight(), node.right.getHeight()) + 1)
    parent = node.parent
    parent.setSize(parent.left.getSize() + parent.right.getSize() + 1)
    parent.setHeight(max(parent.left.getHeight(), parent.right.getHeight()) + 1)
    # node.fix()

"""rotate left
@type node: AVLNode
@pre: node.left.IsRealNode()

"""

def LeftRotation(node):
    son = node.right
    node.setRight(son.left)
    if node.isRoot(): son.setLeft(node)
    else:
        parent = node.parent
        if parent.right is node: parent.setRight(son)
        else: parent.setLeft(son)
        son.setLeft(node)

    node.setSize(node.left.getSize() + node.right.getSize() + 1)
    node.setHeight(max(node.left.getHeight(), node.right.getHeight()) + 1)
    parent = node.parent
    parent.setSize(parent.left.getSize() + parent.right.getSize() + 1)
    parent.setHeight(max(parent.left.getHeight(), parent.right.getHeight()) + 1)
    # node.fix()


"""chose wich rotate id needed and rotate, returns the number of rotation needed
@type node: AVLNode
@pre: |node.getBF()| = 2
@rtype: int
@returns: the number of rotations

"""

def Rotation(node):
    count = 1
    if node.getBF() == 2:
        if node.left.getBF() == -1:
            LeftRotation(node.left)
            count = 2
        RightRotation(node)
    else:
        if node.right.getBF() == 1:
            RightRotation(node.right)
            count = 2
        LeftRotation(node)

    # if node is self.root: self.root = node.parent
    return count

"""balance the tree with atmost 1 rotations from node upwards, and return the number of balance oparation needed
@type node: AVLNode
@rtype: int
@returns: the number of balance oparation needed

"""

def fix1(node):
    balan = 0
    while node.isRealNode():
        height = node.getHeight()
        node.setHeight(max(node.left.getHeight(), node.right.getHeight()) + 1)
        if abs(node.getBF()) == 2:
            return balan + Rotation(node)
        else:
            if height != node.getHeight(): balan += 1
            # else: return balan
        node = node.parent
    return balan

"""balance the tree from node upwards, and return the number of balance oparation needed
@type node: AVLNode
@rtype: int
@returns: the number of balance oparation needed

"""

def fix(node):
    balan = 0
    while node.isRealNode():
        height = node.getHeight()
        node.setHeight(max(node.left.getHeight(), node.right.getHeight()) + 1)
        bf = node.getBF()
        if abs(bf) < 2:
            if height != node.getHeight(): balan += 1
        else:
            balan += Rotation(node)
        node = node.parent
    return balan

"""
@pre T1,T2,x are nodes 
@pre T1 < x < T2
@return the root of the tree of join T1,x,T2
"""

def join(T1, T2, x):
    x.disconnect()
    x.setHeight(0)
    x.setSize(1)
    T1.disconnectParent()
    T2.disconnectParent()

    """"
        Find the right most subtree of T1 which has a height of height(T2)
        @pre T1 < T2
        @pre Height(T1) > Height(T2)
    """

    def findHeightOfRight(T1, T2):
        height = T2.getHeight()

        def rec(node):
            if node.getHeight() <= height:
                return node
            if node.right != None:
                Node = rec(node.right)
                if Node is not None: return Node

        return rec(T1)

    """"
        Find the left most subtree of T2 which has a height of height(T1)
        @pre T1 < T2
        @pre Height(T1) < Height(T2)
    """

    def findHeightOfLeft(T1, T2):
        height = T1.getHeight()

        def rec(node):
            if node.getHeight() <= height:
                return node
            if node.left != None:
                Node = rec(node.left)
                if Node is not None: return Node

        return rec(T2)

    if abs(T1.getHeight() - T2.getHeight()) <= 1:
        x.setLeft(T1)
        x.setRight(T2)
        x.setSize(T1.getSize() + T2.getSize() + 1)
        x.setHeight(max(T1.getHeight(), T2.getHeight()) + 1)
    elif T1.getHeight() > T2.getHeight():
        if not T2.isRealNode():
            tmp = T1
            while tmp.right.isRealNode(): tmp = tmp.right
            tmp.setRight(x)
            # tmp.setSize(tmp.getSize() + 1)
            tmp.setHeight(max(tmp.getHeight(), 1))
            tmp.fix()
            fix1(tmp)
            return x.getRoot()
        y = findHeightOfRight(T1, T2)
        x.pushLeft(y)
        x.setRight(T2)
        x.fix()
        fix(x)
    else:
        if not T1.isRealNode():
            tmp = T2
            while tmp.left.isRealNode(): tmp = tmp.left
            tmp.setLeft(x)
            # tmp.setSize(tmp.getSize() + 1)
            tmp.setHeight(max(tmp.getHeight(), 1))
            tmp.fix()
            fix1(tmp)
            return x.getRoot()
        y = findHeightOfLeft(T1, T2)
        x.pushRight(y)
        x.setLeft(T1)
        x.fix()
        fix(x)
    return x.getRoot()