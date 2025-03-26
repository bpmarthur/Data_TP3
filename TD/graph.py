import numpy as np
from TD.cloud import Point, Cloud

class Edge:
    """An edge in a Point graph.

    Attributes
    ----------
    p1, p2 : Point -- the vertices connected by the edge
    length : float -- the length of the edge
    """

    def __init__(self, p1, p2, length):
        self.p1 = p1
        self.p2 = p2
        self.length = length

    def __repr__(self):
        return f"Edge({repr(self.p1)}, {repr(self.p2)}, {self.length})"

    def __str__(self):
        return f"Edge: {self.p1} -> {self.p2} (length {self.length})"

    # TODO: Exercise 3
    def __lt__(self, other):
        '''
        Again, since __lt__ is a “dunder” (double-underscore) method, you should never call it directly: it exists so that Python can apply the < comparison operator to Edge objects, and therefore sort collections of Edges.
        These < comparisons are translated directly into implicit calls to __lt__ (for example, e_1 < e_3 is translated to e_1.__lt__(e_3)).
        '''
        return self.length < other.length
    



class Graph:
    """
    A simple weighted graph, with edges sorted by non-decreasing length.
    node_names are to indices of Points in an associated Cloud object.

    Attributes
    ----------
    edges : [Edge]
    node_names : [str]

    Il faut ici voir node_names[i] comme le nom du point i dans le Cloud associé.
    """

    def __init__(self):
        self.edges = []
        self.node_names = []

    def __str__(self):
        n = len(self.node_names)
        if n == 0:
            node_str = "0 Nodes"
        elif n == 1:
            node_str = f"1 Node: 0: {self.node_names[0]}"
        else:
            node_str = f"{n} Nodes: " + ", ".join(
                f"{i}: {n}" for (i, n) in enumerate(self.node_names)
            )
        m = len(self.edges)
        if m == 0:
            edge_str = "0 Edges"
        elif m == 1:
            edge_str = f"1 Edge: {self.edges}"
        else:
            edge_str = f"{m} Edges: {self.edges}"
        return f"Graph:\n{node_str}\n{edge_str}"

    def __iter__(self):
        # Iterate over a Graph -> iterate over its edges list
        return iter(self.edges)

    def edge_count(self):
        return len(self.edges)

    def node_count(self):
        return len(self.node_names)

    def get_name(self, i: int) -> str:
        return self.node_names[i]

    def get_edge(self, i: int) -> Edge:
        """The i-th edge of the (length-sorted) edge list."""
        return self.edges[i]

    def add_nodes(self, ns: [str]) -> None:
        """Add a list of (names of) nodes to the graph."""
        # TODO: Exercise 4
        self.node_names.extend(ns)

    def add_edges(self, es: [Edge]) -> None:
        """Add a list of edges to the graph,
        maintaining the length-sorted invariant.
        """
        # TODO: Exercise 4
        self.edges.extend(es)
        self.edges.sort()


def graph_from_cloud(c: Cloud):
    """Construct the complete graph whose nodes are names of points in c
    and where the length of the edge between two points is the Euclidean
    distance between them.
    """
    res = Graph()
    # TODO: Exercise 5
    for i in range(len(c)):
        for j in range(i):
            p1 = c[i]
            p2 = c[j]
            length = p1.dist(p2)
            e = Edge(i, j, length)
            res.add_edges([e])
        res.add_nodes([c[i].name])
    return res


def graph_from_matrix(node_names: [str], dist_matrix: [[float]]):
    """Construct the complete graph on the given list of node names
    with the length of the edge between nodes i and j given by the
    (i,j)-th entry of the matrix.
    """
    res = Graph()
    # TODO: Exercise 6
    for i in range(len(node_names)):
        for j in range(i):
            p1 = node_names[i]
            p2 = node_names[j]
            length = dist_matrix[i][j]
            e = Edge(i, j, length)
            res.add_edges([e])
        res.add_nodes([node_names[i]])
    return res

def graph_from_matrix_file(filename):
    """Construct the graph specified in the named file.  The first line
    in the file is the number n of nodes; the next n lines give the node
    names; and the following n lines are the rows of the distance matrix
    (n entries per line, comma-separated).
    """
    # TODO: Exercise 6
    node_names = []
    dist_matrix = []
    with open(filename, 'r') as f:
        n = int(f.readline())
        for _ in range(n):
            node_names.append(f.readline().strip())
        for _ in range(n):
            dist_matrix.append([float(x) for x in f.readline().strip().split(',')])
    return graph_from_matrix(node_names, dist_matrix)

