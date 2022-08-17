# Copyright 2020 Vincent A Cicirello.  All rights reserved.
#
# License:
# This file is licensed for use by students in
# Stockton University course CSCI 4104 in semester
# of enrollment only.  All other use prohibited.
# Redistribution is prohibited.


class PQInts :

    __slots__ = [ '_minheap', '_index' ]
    
    def __init__(self, n) :
        """Initializes an empty PQ, but configured to support
        integers in the interval [0,n) as the elements."""
        self._index = [ -1 for x in range(n) ]
        self._minheap = []

    def size(self) :
        """Size of the PQ."""
        return len(self._minheap)

    def isEmpty(self) :
        """Returns True if PQ is empty and False otherwise."""
        return len(self._minheap) == 0

    def insert(self, element, value) :
        """Adds an element to the PQ with a specified priority.

        Adds the element to the PQ provided PQ doesn't already contain it.
        Does nothing if the PQ already contains the element.

        Returns True if element added and False if already present.

        Keyword arguments:
        element -- The element to add.
        value -- The priority of the element.
        """
        if self._index[element] >= 0 :
            return False
        position = len(self._minheap)
        self._minheap.append((element, value))
        self._percolate_up(position)
        return True

    def insertAll(self, pairs) :
        """Adds a list of (element, value) pairs to the PQ.

        Adds the (element, value) pairs from the list pairs to the PQ.  Only the
        pairs for which element is not already in the PQ are added.

        Keyword arguments:
        pairs -- A list of 2-tuples of the form (element, value) where value is the priority of element.
        """
        if len(pairs) >= len(self._minheap) :
            for p in pairs :
                if self._index[p[0]] < 0 :
                    self._minheap.append(p)
            self._heapify()
        else :
            for el,val in pairs :
                self.insert(el,val)

    def peekMin(self) :
        """Returns, but does not remove, the element with the minimum priority value."""
        
        return self._minheap[0][0]

    def extractMin(self) :
        """Removes and returns the element with minimum priority value."""
        
        minElement = self._minheap[0][0]
        oldLast = self._minheap.pop()
        if len(self._minheap) > 0 :
            self._minheap[0] = oldLast
            self._percolate_down(0)
        self._index[minElement] = -1
        return minElement

    def contains(self, element) :
        """Returns True if element is in the PQ and False otherwise.

        Keyword arguments:
        element -- The element
        """
        return self._index[element] >= 0

    def getPriority(self, element) :
        """Gets the current priority of the specified element.

        Keyword arguments:
        element -- The element
        """
        return self._minheap[self._index[element]][1]

    def changePriority(self, element, value) :
        """Changes the priority of an element in the PQ.

        Changes the priority of an element that is in the PQ.
        Does nothing if the PQ doesn't contains the element.

        Returns True if element is present in the PQ and False otherwise.

        Keyword arguments:
        element -- The element to add.
        value -- The new priority for the element.
        """
        if not self.contains(element) :
            return False
        position = self._index[element]
        if self._minheap[position][1] > value :
            self._minheap[position] = (element, value)
            self._percolate_up(position)
        elif self._minheap[position][1] < value :
            self._minheap[position] = (element, value)
            self._percolate_down(position)
        return True

    

    def _left(i) :
        return 2*i+1

    def _right(i) :
        return 2*i+2

    def _parent(i) :
        return (i-1)//2

    def _heapify(self) :
        start = len(self._minheap) // 2 - 1
        for i in range(start, -1, -1) :
            self._percolate_down_no_index(i)
        for i, p in enumerate(self._minheap) :
            self._index[p[0]] = i

    def _percolate_up(self, position) :
        current = self._minheap[position]
        p = PQInts._parent(position)
        while p >= 0 and self._minheap[p][1] > current[1] :
            self._minheap[position] = self._minheap[p]
            self._index[self._minheap[position][0]] = position 
            position = p
            p = PQInts._parent(position)
        self._minheap[position] = current
        self._index[self._minheap[position][0]] = position

    def _percolate_down(self, position) :
        minChildPos = PQInts._left(position)
        current = self._minheap[position]
        while minChildPos < len(self._minheap) :
            if minChildPos + 1 < len(self._minheap) and self._minheap[minChildPos + 1][1] < self._minheap[minChildPos][1] :
                minChildPos = minChildPos + 1
            if self._minheap[minChildPos][1] < current[1] :
                self._minheap[position] = self._minheap[minChildPos]
                self._index[self._minheap[position][0]] = position
                position = minChildPos
                minChildPos = PQInts._left(position)
            else :        
                 break
        self._minheap[position] = current
        self._index[self._minheap[position][0]] = position

    def _percolate_down_no_index(self, position) :
        minChildPos = PQInts._left(position)
        current = self._minheap[position]
        while minChildPos < len(self._minheap) :
            if minChildPos + 1 < len(self._minheap) and self._minheap[minChildPos + 1][1] < self._minheap[minChildPos][1] :
                minChildPos = minChildPos + 1
            if self._minheap[minChildPos][1] < current[1] :
                self._minheap[position] = self._minheap[minChildPos]
                position = minChildPos
                minChildPos = PQInts._left(position)
            else :        
                 break
        self._minheap[position] = current



