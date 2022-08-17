# Copyright 2020 Vincent A Cicirello.  All rights reserved.
#
# License:
# This file is licensed for use by students in
# Stockton University course CSCI 4104 in semester
# of enrollment only.  All other use prohibited.
# Redistribution is prohibited.

class DisjointIntegerSets :
    """Disjoint Set Forests of Integers: Representation of disjoint sets.

    Disjoint sets of the integers from [0,n) represented as disjoint set forest.
    This implementation uses both the union by rank heuristic, as well as
    path compression.
    """

    __slots__ = ["_nodes"]

    def __init__(self, n) :
        """Initializes disjoint set forest.

        If n >= 1, initializes disjoint sets of the integers in interval [0..n-1].
        Each integer from 0 to n - 1 is initially in a set by itself.

        Keyword arguments:
        n -- number of elements in disjoint set forest.
        """

        self._nodes = [ self.makeset(i) for i in range(n) ]


    def makeset(self,x) :
        """Creates a set containing only element x, adding set to forest.

        
        Keyword arguments:
        x -- an element of any hashable type
        """
        class _DJSetNode :
            __slots__ = ['p','rank']

        node = _DJSetNode()
        node.p = x
        node.rank = 0
        return node
        

    def union(self,x,y) :
        """Computes the union of the sets containing x and y.

        Uses union by rank heuristic in computing union of sets containing x and y.
        the "shorter" tree is added as child of "taller" tree.  Though heights are
        approximate since ranks are upper bounds only.

        Keyword arguments:
        x -- an element
        y -- an element
        """
        self._link(self.findset(x), self.findset(y))


    def findset(self,x) :
        """Finds the set for a given element, and performs path compression.

        Finds the set for a given element, returning the integer at the root of its
        tree in the forest.  The find also performs path compression, resetting the parents
        of all nodes along path to root to point directly to root.  Path compression does not
        reset ranks, thus ranks are upper bounds only.

        Returns a representative member of the set, namely the root of the set's tree.
        Subsequent calls to the union method may change which element is root, but otherwise
        no other method change the root elements.

        Keyword arguments:
        x -- the element whose set we want to find
        """
        # perform path compression during the find
        if x != self._nodes[x].p :
            self._nodes[x].p = self.findset(self._nodes[x].p)
        return self._nodes[x].p
             
    def _link(self, x, y) :
        # union by rank heuristic: attach approximately "shorter" tree as child of approximately "taller" tree
        if self._nodes[x].rank > self._nodes[y].rank :
            self._nodes[y].p = x
        else :
            self._nodes[x].p = y
            if self._nodes[x].rank == self._nodes[y].rank :
                self._nodes[y].rank += 1


