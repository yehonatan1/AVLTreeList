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

    def __str__(self): return 'virtual: ' + str(not self.isRealNode()) + ',\tval: ' + str(self.value) + ',\theight: ' + str(self.height) + ',\tsize: ' + str(self.size) + '.'
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

	@rtype: AVLNode
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
            print("Can't get the amount of sons of a virtual node")
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
        # assert 0 <= i < self.size
        index = self.left.getSize()  # The size of the node
        if index == i:
            return self
        if index > i:
            return self.left.retrieve_node(i)
        else:
            return self.right.retrieve_node(i - index - 1)


    """
    @return the successor of self in a node
    """

    def getSuccessor(self):
        if self.isRealNode():
            index = self.getIndex()
            if index + 1 == self.getRoot().getSize():
                print("Error can't get the successor of the maximum value")
                return -1
            else:
                return self.retrieve_node(self.getIndex() + 1)

        print("Error can't get the successor of a virtual node")
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
        node = self
        while not node.isRoot(): node = node.parent
        return node

    """"disconnect self from parent"""

    def disconnectParent(self):
        if not self.isRoot() and self.isRealNode():
            if self.parent.left is self:
                self.parent.left = AVLNode(None, True)
                self.parent.left.parent = self.parent
            else:
                self.parent.right = AVLNode(None, True)
                self.parent.right.parent = self.parent

            self.parent.fix()
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

    """sets right child
    
    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
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

    """fix node's height and size for all nodes from self upwards and return the number of heights changes
    @rtype: int
    @returns: the number of height changes
    
    """

    def fix(self):
        if self.isRealNode():
            height = max(self.right.getHeight(), self.left.getHeight()) + 1
            size = self.left.getSize() + self.right.getSize() + 1
            if height == self.height and size == self.size: return 0
            cnt = int(height != self.height)
            self.setHeight(height)
            self.setSize(size)
            return cnt + self.parent.fix()
        return 0

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

    def __init__(self):
        self.root = AVLNode(None, True)

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

    """rotate right
    @type node: AVLNode
    @pre: node.right.IsRealNode()
    
    """

    def RightRotion(self, node):
        if node.parent.isRealNode():
            right = node.parent.right is node
            if node.parent.left is node:
                node.parent.left = node.left
            else:
                node.parent.right = node.left
        node.left.parent = node.parent
        node.setLeft(node.left.right)
        if not node.parent.right is node:
            if right:
                node.parent.right.parent = node.parent
                node.parent.right.right = node
                node.parent = node.parent.right
            else:
                node.parent.left.parent = node.parent
                node.parent.left.right = node
                node.parent = node.parent.left

        node.fix()

    """rotate left
    @type node: AVLNode
    @pre: node.left.IsRealNode()
    
    """

    def LeftRotion(self, node):
        if node.parent.isRealNode():
            left = node.parent.left is node
            if node.parent.left is node:
                node.parent.left = node.right
            else:
                node.parent.right = node.right
        node.right.parent = node.parent
        node.setRight(node.right.left)
        if not node.parent.left is node:
            if left:
                node.parent.left.parent = node.parent
                node.parent.left.left = node
                node.parent = node.parent.left
            else:
                node.parent.right.parent = node.parent
                node.parent.right.left = node
                node.parent = node.parent.right

        node.fix()

    """chose wich rotate id needed and rotate, returns the number of rotion needed
    @type node: AVLNode
    @pre: |node.getBF()| = 2
    @rtype: int
    @returns: the number of rotions
    
    """

    def Rotion(self, node):
        count = 1
        if node.getBF() == 2:
            if node.left.getBF() == -1:
                self.LeftRotion(node.left)
                count = 2
            self.RightRotion(node)
        else:
            if node.right.getBF() == 1:
                self.RightRotion(node.right)
                count = 2
            self.LeftRotion(node)

        if node is self.root: self.root = node.parent
        return count

    """fix the tree node's hieghts and sizes, balance the tree with atmost 1 rotions from node upwards, and return the number of rotions needed
    @type node: AVLNode
    @rtype: int
    @returns: the number of rotions needed
    
    """

    def fix1(self, node):
        while node.isRealNode():
            if abs(node.getBF()) == 2: return self.Rotion(node)
            node = node.parent
        return 0

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
        return node.parent.fix() + self.fix1(node)

    """deletes the i'th item in the list
    
    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i):
        def fix(node):
            number_of_rotations = 0
            while node.isRealNode():
                bf = node.getBF()
                if abs(bf) < 2:
                    node = node.parent
                else:
                    number_of_rotations += self.Rotion(node)
                    node = node.parent
            return number_of_rotations

        node = self.retrieve_node(i)
        parent = node.getParent()

        if not node.isRealNode():
            print("Can't delete a virtual node")
            return -1

        if node is self.root:
            if node.isLeaf():
                self.root = AVLNode(None, True)
                return 0
            elif node.numberOfSons() == 1:
                if self.root.left.isRealNode():
                    self.root = self.root.left
                    return 0
                else:
                    self.root = self.root.right
                    return 0
            else:
                successor = node.getSuccessor()
                x = successor.parent
                successor.parent = AVLNode(None, True)
                if x.right is successor:
                    x.right = AVLNode(None, True)
                    x.right.parent = x
                else:
                    x.left = AVLNode(None, True)
                    x.left.parent = x
                x = x.left
                successor.left = self.root.left
                successor.left.parent = successor
                self.root.left = AVLNode(None, True)
                successor.right = self.root.right
                successor.right.parent = successor
                self.root.right = AVLNode(None, True)
                self.root = successor
                x = x.parent
                n = x.fix()
                return n + fix(x)


        tmp = node.parent

        if node.isLeaf():
            node.disconnectParent()
        elif node.numberOfSons() == 1:
            if parent.getRight() is node:
                if node.right.isRealNode():
                    parent.right = node.getLeft()
                    node.getLeft().setParent(parent)
                else:
                    parent.right = node.getLeft()
                    node.getLeft().setParent(parent)
            else:
                if node.right.isRealNode():
                    parent.left = node.getLeft()
                    node.getLeft().setParent(parent)
                else:
                    parent.left = node.getLeft()
                    node.getLeft().setParent(parent)
        else:
            successor = node.getSuccessor()
            tmp = successor.parent
            if parent.getRight() is node:
                parent.right = successor
                successor.setParent(parent)
            else:
                parent.left = successor
                successor.setParent(parent)

            successor.right = node.right
            successor.left = node.left
            successor.setSize(successor.left.getSize() + successor.right.getSize() + 1)
            successor.setHeight(max(successor.left.getHeight(), successor.right.getHeight()) + 1)

        n = tmp.fix()
        return n + fix(parent)

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
        index = self.root.left.getSize()
        try:
            arr[index] = self.root
        except IndexError:
            print(self.length(), index)
            print('IndexError')
            quit()
        rec(self.root, index, arr)
        return [node.getValue() for node in arr]

    """returns the size of the list 

    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return self.root.getSize()

    """
    @pre T1,T2,x are nodes 
    @pre T1 < x < T2
    @return the root of the tree of join T1,x,T2
    """

    def join(self, T1, T2, x):
        x.disconnect()
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
                if node.getHeight() == height or node.getHeight() == height - 1:
                    return node
                if node.right.isRealNode():
                    Node = rec(node.right)
                    if Node is not None: return Node

            return rec(T1)

        """"
            Find the left most subtree of T1 which has a height of height(T2)
            @pre T1 < T2
            @pre Height(T1) > Height(T2)
        """

        def findHeightOfLeft(T1, T2):
            height = T2.getHeight()

            def rec(node):
                if node.getHeight() == height or node.getHeight() == height - 1:
                    return node
                if node.right.isRealNode():
                    Node = rec(node.left)
                    if Node is not None: return Node

            return rec(T1)

        if abs(T1.getHeight() - T2.getHeight()) <= 1:
            parent1 = T1.getParent()
            if parent1.isRealNode():
                if parent1.right is T1:
                    parent1.setRight(AVLNode(None, True))
                else:
                    parent1.setLeft(AVLNode(None, True))
            T1.setParent(AVLNode(None, True))

            x.setLeft(T1)
            parent2 = T2.getParent()
            if parent2.isRealNode():
                if parent2.right is T2:
                    parent2.setRight(AVLNode(None, True))
                else:
                    parent2.setLeft(AVLNode(None, True))
            T2.setParent(AVLNode(None, True))
            x.setRight(T2)
            x.fix()
        elif T1.getHeight() > T2.getHeight():
            y = findHeightOfRight(T1, T2)
            x.setLeft(y)

            parent = T2.getParent()
            if parent.isRealNode():
                if parent.right is T2:
                    parent.setRight(AVLNode(None, True))
                else:
                    parent.setLeft(AVLNode(None, True))

            T2.setParent(AVLNode(None, True))
            x.setRight(T2)
            x.fix()
            self.fix1(x)

        else:
            y = findHeightOfLeft(T2, T1)
            x.setLeft(y)

            parent = T2.getParent()
            if parent.isRealNode():
                if parent.right is T1:
                    parent.setRight(AVLNode(None, True))
                else:
                    parent.setLeft(AVLNode(None, True))

            T2.setParent(AVLNode(None, True))
            x.setRight(T1)
            x.fix()
            self.fix1(x)
            return x.getRoot()

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
            if self.root.left.isRealNode(): L = self.root.left
            else: L = AVLNode(None, True)
            left = AVLTreeList()
            left.root = L

            if self.root.right.isRealNode(): R = self.root.right
            else: R = AVLNode(None, True)
            right = AVLTreeList()
            right.root = R

            return [left, self.root.getValue(), right]

        node = self.retrieve_node(i)
        val = node.getValue()
        L = node.left
        R = node.right
        L.disconnectParent()
        R.disconnectParent()
        parent = node.parent
        right = parent.right is node
        while not node.isRoot():
            node = parent
            parent = parent.parent
            r = parent.right is node
            if right: L = self.join(node.left, L, node)
            else: R = self.join(R, node.right, node)
            right = r

        left = AVLTreeList()
        left.root = L
        right = AVLTreeList()
        right.root = R

        return [left, val, right]

    """concatenates lst to self
    
    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        i = self.length() - 1
        node = self.retrive_node(i)
        self.delete(i)
        root = self.join(self.root, lst.root, node)
        result = AVLTreeList()
        result.root = root
        return result

    """searches for a *value* in the list
    
    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        lst = self.listToArray()
        try: return lst.index(val)
        except ValueError: return -1


    """returns the root of the tree representing the list
    
    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        return self.root
