from collections import deque
import math
from disjointset import DisjointIntegerSets
from intpq import PQInts

class Graph :
    """Graph represented with adjacency lists."""

    __slots__ = ['_adj']

    def __init__(self, v=10, edges=[]) :
        """Initializes a graph with a specified number of vertices.

        Keyword arguments:
        v - number of vertices
        edges - any iterable of ordered pairs indicating the edges 
        """
        self._adj = [ _AdjacencyList() for i in range(v) ]
        for u, v in edges :
            self.addEdge(u, v)
        
    def addEdge(self, a, b) :
        """Adds an edge to the graph.

        Keyword arguments:
        a - first end point
        b - second end point
        """
        self._adj[a].add(b)
        self._adj[b].add(a)

    def numVertices(self) :
        """Gets number of vertices of graph."""        
        return len(self._adj)

    def degree(self, vertex) :
        """Gets degree of specified vertex.

        Keyword arguments:
        vertex - integer id of vertex
        """        
        return self._adj[vertex]._size

    def bfs(self, s) :
        """Performs a BFS of the graph from a specified starting vertex.
        Returns a list of objects, one per vertex, containing the vertex's distance
        from s in attribute d, and vertex id of its predecessor in attribute pred.

        Keyword arguments:
        s - the integer id of the starting vertex.
        """
        
        class VertexData :
            __slots__ = [ 'd', 'pred' ]

            def __init__(self) :
                self.d = math.inf
                self.pred = None

        vertices = [VertexData() for i in range(self.numVertices())]
        vertices[s].d = 0
        q = deque([s])
        while len(q) > 0 :
            u = q.popleft()
            for v in self._adj[u] :
                if vertices[v].d == math.inf :
                    vertices[v].d = vertices[u].d + 1
                    vertices[v].pred = u
                    q.append(v)
        return vertices

    def dfs(self, onFinish=lambda v : None) :
        """Performs a DFS of the graph.  Returns a list of objects, one per vertex, containing
        the vertex's discovery time (d), finish time (f), and predecessor in the depth first forest
        produced by the search (pred).
        """

        class VertexData :
            __slots__ = [ 'd', 'f', 'pred' ]

            def __init__(self) :
                self.d = 0
                self.pred = None

        vertices = [VertexData() for i in range(self.numVertices())]
        time = 0

        def dfs_visit(u) :
            nonlocal time
            nonlocal vertices

            time = time + 1
            vertices[u].d = time
            for v in self._adj[u] :
                if vertices[v].d == 0 :
                    vertices[v].pred = u
                    dfs_visit(v)
            time = time + 1
            vertices[u].f = time
            onFinish(u)

        for u in range(len(vertices)) :
            if vertices[u].d == 0 :
                dfs_visit(u)
        return vertices

    def getEdgeList(self) :
        """Returns a list of the edges of the graph
        as a list of tuples:
        [ (a, b), (c, d), ... ] where a, b, c, d, etc are
        vertex ids.  
        """
        return [ (u,v) for u, uList in enumerate(self._adj) for v in uList if v > u]

class WeightedGraph(Graph) :
    """Weighted graph represented with adjacency lists."""

    class VertexData:
        __slots__ = ['v', 'd', 'pred']

        def __init__(self):

            self.d = math.inf
            self.pred = None

    def __init__(self, v=10, edges=[], weights=[]) :
        """Initializes a weighted graph with a specified number of vertices.

        Keyword arguments:
        v - number of vertices
        edges - any iterable of ordered pairs indicating the edges 
        weights - list of weights, same length as edges list

        """
        self._adj = [ _WeightedAdjacencyList() for i in range(v) ]
        for i, (u,v) in enumerate(edges) :

            self.addEdge(u, v, weights[i])
                
    def addEdge(self, a, b, w=1) :
        """Adds an edge to the graph.

        Keyword arguments:
        a - first end point
        b - second end point
        """
        self._adj[a].add(b, w)
        self._adj[b].add(a, w)

    def getEdgeList(self, withWeights=False) :
        """Returns a list of the edges of the graph
        as a list of tuples.  Default is of the form
        [ (a, b), (c, d), ... ] where a, b, c, d, etc are
        vertex ids.  If with_weights is True, the generated
        list includes the weights in the following form
        [ ((a, b), w1), ((c, d), w2), ... ] where w1, w2, etc
        are the edge weights.

        Keyword arguments:
        withWeights -- True to include weights
        """
        if not withWeights :
            return super().getEdgeList()
        else :
            return [ ((u,v),w) for u, uList in enumerate(self._adj) for v, w in uList.__iter__(True) if v > u]

    def mstKruskal(self) :
        """Returns the set of edges in some
        minimum spanning tree (MST) of the graph,
        computed using Kruskal's algorithm.
        """
        
        A = set()
        forest = DisjointIntegerSets(self.numVertices())
        edges = self.getEdgeList(True)
        edges.sort(key=lambda x : x[1])
        for (u,v), w in edges :
            if forest.findset(u) != forest.findset(v) :
                A.add((u,v))
                forest.union(u,v)
        return A

    def mstPrim(self, r=0) :
        """Returns the set of edges in some
        minimum spanning tree (MST) of the graph,
        computed using Prim's algorithm.

        Keyword arguments:
        r - vertex id to designate as the root (default is 0).
        """

        parent = [ None for x in range(self.numVertices())]
        Q = PQInts(self.numVertices())
        Q.insert(r, 0)
        for u in range(self.numVertices()) :
            if u != r :
                Q.insert(u, math.inf)
        while not Q.isEmpty() :
            u = Q.extractMin()
            for v, w in self._adj[u].__iter__(True) :
                if Q.contains(v) and w < Q.getPriority(v) :
                    parent[v] = u
                    Q.changePriority(v, w)
        return { (u,v) for v, u in enumerate(parent) if u != None}

    def bellmanFord(self,s) :
        """Bellman Ford Algorithm for single source shortest path.

        Keyword Arguments:
        s - The source vertex.
        """

        # Programming Assignment 3:
        # 1) Implement Bellman Ford Algorithm.
        #
        #    If there are negative weight cycles,
        #    have this method return an empty list
        #    (instead of the False from the pseudocode).
        #
        #    If there are no negative weight cycles, then
        #    have this method return a list of 3-tuples,
        #    one for each vertex, such that first position
        #    is vertex id, second is distance from source
        #    vertex (i.e., what pseudocode from textbook refers
        #    to as v.d), and third is the vertex's parent (what
        #    the textbook refers to as v.pi).  E.g., (2, 10, 5)
        #    would mean the shortest path from s to 2 has weight 10,
        #    and vertex 2's parent is vertex 5.
        #
        #    The parameter s is the source vertex.
        #
        # Useful Hint (for both parts 1 and 2):
        #  The loops of lines 3 and 5 of the pseudocode for
        #  Bellman Ford iterate over the edges of the graph.
        #  You will also need the weights.  The adjacency list
        #  class has two iterators, one that gives you the weights
        #  and one that doesn't.  To implement the iteration over the
        #  edges, you will actually need a pair of nested loops, one
        #  over the vertices u, and then one over the edges that
        #  start at u (along with the weights of those edges). 
        #  To iterate over the vertices adjacent to u, and
        #  get the weight associated with each edge, you can do:
        #  for v, w in self._adj[u].__iter__(True)
        #  You don't normally call methods that start with __ directly.
        #  Python's for loops call that method to control how many
        #  times to iterate when iterating over a collection like a list.
        #  I provided an optional parameter to that method, which when
        #  passed True, gives you the adjacent vertices and the edge weights.
        #  Or you can also feel free to use the getEdgeList method
        #  to get a list of the edges with weights.  If you do that,
        #  then you'll just need a pair of nested loops.
        #
        #  Important Hint: In the pseudocode of Bellman Ford, the pair
        #  of nested loops will become a triple
        #  of nested loops in your Python code.  This is because
        #  you need a pair of nested loops to iterate
        #  over the edges, and that will itself be within another
        #  loop (the outer loop from the pseudocode).
        #  Don't forget about that outer loop.  If you leave it out,
        #  you won't get the actual shortest paths,
        #  and when you time your code in part 3, your times will
        #  be significantly off from what they should be.
        #  Although if you do use my getEdgeList method then you really
        #  will only need a pair of nested loops.
        #
        #  When you get to part 2 later, when you implement Dijkstra's
        #  algorithm, you will need to do a similar
        #  thing (line 7 of the pseduocode of Dijkstra's algorithm).
        #  Only there you'll just iterate over the
        #  vertices adjacent to u, and not all of the edges.
        #  So the getEdgeList method will be completely irrelevant to you
        #  for Dijkstra's algorithm.
        pass

    def dijkstra(self,s) :
        """Dijkstra's Algorithm using a binary heap as the PQ.

        Keyword Arguments:
        s - The source vertex.
        """

        # Programming Assignment 3:
        # 2) Implement Dijkstra's Algorithm using a binary heap
        #    implementation of a PQ as the PQ.
        #    Specifically, use the PQInts class from the intpq.py
        #    that I have provided.  You can see examples of its usage
        #    above in the implementation of Prim's algorithm.
        #
        #    Have this method return a list of 3-tuples, one for
        #    each vertex, such that first position is vertex id,
        #    second is distance from source vertex (i.e., what
        #    pseudocode from textbook refers to as v.d), and third
        #    is the vertex's parent (what the textbook refers to
        #    as v.pi).  E.g., (2, 10, 5) would mean the shortest path
        #    from s to 2 has weight 10, and vertex 2's parent is vertex 5.
        #
        #    The parameter s is the source vertex.
        #
        #    Whenever you need to change the value of d for a
        #    vertex, don't forget to also call the appropriate
        #    method from the PQInts class to decrease that vertex's
        #    priority.  Your implementation will be incorrect if you
        #    forget to update priorities.
        pass

class Digraph(Graph) :
    """Digraph represented with adjacency lists."""

    __slots__ = [ '_inDegree' ]

    def __init__(self, v=10, edges=[]) :
        self._inDegree = [ 0 for i in range(v) ]
        self._adj = [ _AdjacencyList() for i in range(v) ]
        for u, v in edges :
            self.addEdge(u, v)
        
    def addEdge(self, a, b) :
        """Adds a directed edge to the graph.

        Keyword arguments:
        a - source (starting) vertex
        b - target (ending) vertex
        """
        self._adj[a].add(b)
        self._inDegree[b] += 1

    def outDegree(self, vertex) :
        """Gets the outdegree of a vertex

        Keyword arguments:
        vertex - the vertex id"""
        return super().degree(vertex)

    def inDegree(self, vertex) :
        """Gets the indegree of a vertex

        Keyword arguments:
        vertex - the vertex id"""
        return self._inDegree[vertex]

    def degree(self, vertex) :
        """Gets the indegree of a vertex

        Keyword arguments:
        vertex - the vertex id"""
        return self.outDegree(vertex) + self.inDegree(vertex)

    def getEdgeList(self) :
        """Returns a list of the edges of the graph
        as a list of tuples:
        [ (a, b), (c, d), ... ] where a, b, c, d, etc are
        vertex ids.  
        """
        return [ (u,v) for u, uList in enumerate(self._adj) for v in uList]

    def transpose(self) :
        """Generates and returns the transpose of this Digraph."""
        T = Digraph(self.numVertices())
        for u, adjacent in enumerate(self._adj) :
            for v in adjacent :
                T.addEdge(v, u)
        return T

    def topologicalSort(self) :
        """Topological Sort of the directed graph (Section 22.4 from textbook).
        Returns the topological sort as a list of vertex indices.
        """
        topSort = []
        def onFinish(u) :
            nonlocal topSort
            topSort.append(u)
        self.dfs(onFinish)
        topSort.reverse()
        return topSort

    def scc(self) :
        """Computes the strongly connected components of a digraph.
        Returns a list of sets, containing one set for each
        strongly connected component,
        which is simply a set of the vertices in that component."""
        ordered = self.topologicalSort()
        T = self.transpose()
        
        discovered = [ False for i in range(T.numVertices())]
        def dfs_visit(u, component) :
            nonlocal discovered
            nonlocal T

            discovered[u] = True
            component.add(u)
            for v in T._adj[u] :
                if not discovered[v] :
                    dfs_visit(v, component)

        SCC = []
        for u in ordered :
            if not discovered[u] :
                component = set()
                dfs_visit(u, component)
                SCC.append(component)
        return SCC

class WeightedDigraph(WeightedGraph,Digraph) :
    """Weighted Digraph represented with adjacency lists."""

    def __init__(self, v=10, edges=[], weights=[]) :
        """Initializes a weighted digraph with a specified number of vertices.

        Keyword arguments:
        v - number of vertices
        edges - any iterable of ordered pairs indicating the edges 
        weights - list of weights, same length as edges list
        """
        self._adj = [ _WeightedAdjacencyList() for i in range(v) ]
        for i, (u,v) in enumerate(edges) :
            self.addEdge(u, v, weights[i])
        
    def addEdge(self, a, b, w=1) :
        """Adds an edge to the graph.

        Keyword arguments:
        a - source (starting) vertex
        b - target (ending) vertex
        """
        self._adj[a].add(b, w)

    def degree(self, vertex) :
        return Digraph.degree(self, vertex)

    def getEdgeList(self, withWeights=False) :
        """Returns a list of the edges of the graph
        as a list of tuples.  Default is of the form
        [ (a, b), (c, d), ... ] where a, b, c, d, etc are
        vertex ids.  If with_weights is True, the generated
        list includes the weights in the following form
        [ ((a, b), w1), ((c, d), w2), ... ] where w1, w2, etc
        are the edge weights.

        Keyword arguments:
        withWeights -- True to include weights
        """
        if not withWeights :
            return super().getEdgeList()
        else :
            return [ ((u,v),w) for u, uList in enumerate(self._adj) for v, w in uList.__iter__(True)]
     
    def transpose(self) :
        """Generates and returns the transpose of this Digraph."""
        T = WeightedDigraph(self.numVertices())
        for u, adjacent in enumerate(self._adj) :
            for v, w in adjacent.__iter__(True) :
                T.addEdge(v, u, w)
        return T

class _AdjacencyList :

    __slots__ = [ '_first', '_last', '_size']

    def __init__(self) :
        self._first = self._last = None
        self._size = 0

    def add(self, vertex) :
        self._add(_AdjListNode(vertex))
        
    def _add(self, listNode) :
        if self._first == None :
            self._first = self._last = listNode
        else :
            self._last._next = listNode
            self._last = self._last._next
        self._size += 1

    def __iter__(self):
        return _AdjListIter(self)    

class _WeightedAdjacencyList(_AdjacencyList) :

    __slots__ = []

    def __init__(self) :
        super().__init__()

    def add(self, vertex, w=1) :
        self._add(_WeightedAdjListNode(vertex, w))

    def __iter__(self, weighted=False):
        if weighted :
            return _AdjListIterWithWeights(self)
        else :
            return _AdjListIter(self)    
    
class _AdjListNode :

    __slots__ = [ '_next', '_targetVertex' ]

    def __init__(self, vertex) :
        self._next = None
        self._targetVertex = vertex

class _WeightedAdjListNode(_AdjListNode) :

    __slots__ = [ '_w' ]

    def __init__(self, vertex, w=1) :
        super().__init__(vertex)
        self._w = w

class _AdjListIter :

    __slots__ = [ '_next' ]

    def __init__(self, adjlist) :
        self._next = adjlist._first
        
    def __iter__(self) :
        return self

    def __next__(self) :
        if self._next == None :
            raise StopIteration
        vertex = self._next._targetVertex
        self._next = self._next._next
        return vertex

class _AdjListIterWithWeights(_AdjListIter) :

    __slots__ = []

    def __init__(self, adjlist) :
        super().__init__(adjlist)

    def __next__(self) :
        if self._next == None :
            raise StopIteration
        vertex = self._next._targetVertex
        w = self._next._w
        self._next = self._next._next
        return vertex, w




    
