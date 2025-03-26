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
    pass


class Graph:
    """
    A simple weighted graph, with edges sorted by non-decreasing length.
    node_names are to indices of Points in an associated Cloud object.

    Attributes
    ----------
    edges : [Edge]
    node_names : [str]
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
        pass

    def add_edges(self, es: [Edge]) -> None:
        """Add a list of edges to the graph,
        maintaining the length-sorted invariant.
        """
        # TODO: Exercise 4
        pass


def graph_from_cloud(c: Cloud):
    """Construct the complete graph whose nodes are names of points in c
    and where the length of the edge between two points is the Euclidean
    distance between them.
    """
    res = Graph()
    # TODO: Exercise 5
    pass
    return res


def graph_from_matrix(node_names: [str], dist_matrix: [[float]]):
    """Construct the complete graph on the given list of node names
    with the length of the edge between nodes i and j given by the
    (i,j)-th entry of the matrix.
    """
    res = Graph()
    # TODO: Exercise 6
    pass
    return res


def graph_from_matrix_file(filename):
    """Construct the graph specified in the named file.  The first line
    in the file is the number n of nodes; the next n lines give the node
    names; and the following n lines are the rows of the distance matrix
    (n entries per line, comma-separated).
    """
    # TODO: Exercise 6
    pass

