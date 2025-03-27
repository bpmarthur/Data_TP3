#! /usr/bin/env python3
import sys
import unittest
import numpy as np

from itertools import permutations

from TD.cloud import *
from TD.graph import *
from TD.dendrogram import *


"""
Annotations used for the autograder.

[START-AUTOGRADER-ANNOTATION]
{
  "total" : 12,
  "names" : [
      "graph.py::test_lt",
      "graph.py::test_add_nodes",
      "graph.py::test_add_edges",
      "graph.py::test_graph_from_cloud",
      "graph.py::test_graph_from_matrix",
      "graph.py::test_graph_from_matrix_file",
      "dendrogram.py::test_find_rep",
      "dendrogram.py::test_merge",
      "dendrogram.py::test_build",
      "dendrogram.py::test_set_clusters",
      "dendrogram.py::test_count_ns_clusters",
      "dendrogram.py::test_get_cluster_height"
      ],
  "points" : [5, 5, 7, 5, 5, 8, 12, 5, 12, 12, 12, 12]
}
[END-AUTOGRADER-ANNOTATION]
"""


def print_help():
    print(
        "./grader script. Usage: ./grader.py test_number, e.g., ./grader.py 1 for the 1st exercise."
    )
    print("N.B.: ./grader.py 0 runs all tests.")
    print(f"You provided {sys.argv}.")
    exit(1)

def make_example():
    c = Cloud()
    for x in [0.0, 1.0, 3.0, 4.0, 9.0]:
        c.add_point(Point([x]))
    g = graph_from_cloud(c)
    d = Dendrogram(g)
    d.build()
    return d

class Grader(unittest.TestCase):
    def test_lt(self):
        message = "Less-than operator (Edge.__lt__ method)"
        e_0 = Edge(4, 5, 1.7)
        e_1 = Edge(0, 1, 10.0)
        e_2 = Edge(0, 1, 2.3)
        e_3 = Edge(2, 3, 10.0)
        self.assertLess(e_0, e_2, msg=message)
        self.assertLess(e_2, e_1, msg=message)
        self.assertFalse(e_1 < e_3, msg=message)
        self.assertFalse(e_2 < e_0, msg=message)

    def test_add_nodes(self):
        message = "add_nodes"
        g = Graph()
        g.add_nodes(['A', 'B', 'C'])
        self.assertEqual(g.node_names, ['A', 'B', 'C'])
        g.add_nodes([])
        self.assertEqual(g.node_names, ['A', 'B', 'C'])
        g.add_nodes(['D'])
        self.assertEqual(g.node_names, ['A', 'B', 'C', 'D'])

    def test_add_edges(self):
        g = Graph()
        e_1 = Edge(0, 1, 1.2)
        e_2 = Edge(0, 2, -1)
        g.add_edges([e_1])
        self.assertEqual(g.edges, [e_1])
        g.add_edges([e_2])
        self.assertEqual(len(g.edges), 2)
        self.assertEqual(g.edges, [e_2, e_1], msg="edges not sorted")

    def test_graph_from_cloud(self):
        c = Cloud()
        c.add_point(Point([1.0, 0.0, 0.0], 'x'))
        c.add_point(Point([0.0, 1.0, 0.0], 'y'))
        c.add_point(Point([0.0, 0.0, 1.0], 'z'))
        g = graph_from_cloud(c)
        self.assertEqual(g.node_names, ['x', 'y', 'z'])
        self.assertEqual(len(g.edges), 3)
        self.assertEqual(g.edges[0].p1, 1)
        self.assertEqual(g.edges[0].p2, 0)
        self.assertAlmostEqual(g.edges[0].length, 1.4142135623730951)
        self.assertEqual(g.edges[1].p1, 2)
        self.assertEqual(g.edges[1].p2, 0)
        self.assertAlmostEqual(g.edges[1].length, 1.4142135623730951)
        self.assertEqual(g.edges[2].p1, 2)
        self.assertEqual(g.edges[2].p2, 1)
        self.assertAlmostEqual(g.edges[2].length, 1.4142135623730951)

    def test_graph_from_matrix(self):
        nodes = ['A', 'B', 'C']
        lengths = [[0,1,2],[1,0,3],[2,3,0]]
        g = graph_from_matrix(nodes, lengths)
        self.assertEqual(g.node_names, nodes)
        self.assertEqual(g.edges[0].p1, 1)
        self.assertEqual(g.edges[0].p2, 0)
        self.assertAlmostEqual(g.edges[0].length, 1)
        self.assertEqual(g.edges[1].p1, 2)
        self.assertEqual(g.edges[1].p2, 0)
        self.assertAlmostEqual(g.edges[1].length, 2)
        self.assertEqual(g.edges[2].p1, 2)
        self.assertEqual(g.edges[2].p2, 1)
        self.assertAlmostEqual(g.edges[2].length, 3)

    def test_graph_from_matrix_file(self):
        filename = 'csv/languages.csv'
        message = "Graph from csv/languages.csv"
        g = graph_from_matrix_file(filename)
        self.assertEqual(len(g.node_names), 19, msg=message)
        self.assertEqual(len(g.edges), 171, msg=message)
        # Check some of the entries
        self.assertEqual(g.node_names[0], "English", msg=message)
        self.assertEqual(g.node_names[6], "West_Frisian", msg=message)
        self.assertEqual(g.node_names[18], "Sranan", msg=message)
        #
        self.assertEqual(g.edges[0].p1, 16, msg=message)
        self.assertEqual(g.edges[0].p2, 12, msg=message)
        self.assertAlmostEqual(g.edges[0].length, 4.0, msg=message)
        #
        self.assertEqual(g.edges[2].p1, 15, msg=message)
        self.assertEqual(g.edges[2].p2, 14, msg=message)
        self.assertAlmostEqual(g.edges[2].length, 10.0, msg=message)
        #
        self.assertEqual(g.edges[-1].p1, 18, msg=message)
        self.assertEqual(g.edges[-1].p2, 9, msg=message)
        self.assertAlmostEqual(g.edges[-1].length, 51.0, msg=message)

    def test_find_rep(self):
        g = Graph()
        g.add_nodes(['A', 'B', 'C', 'D', 'E'])
        d = Dendrogram(g)
        message_1 = "Dendrogram with 5 nodes, 0 with parents"
        for i in range(5):
            self.assertEqual(d.find_rep(i), i, msg=message_1)
        #
        parents = [1, 2, -1, 4, -1]
        reference = [2, 2, 2, 4, 4]
        message_2 = f"Dendrogram with 5 nodes, {parents=}"
        d.parent = parents[:]
        for i in range(5):
            self.assertEqual(d.find_rep(i), reference[i], msg=message_2)

    def test_merge(self):
        p1 = Point([0.0, 0.0], name='O')
        p2 = Point([1.0, 0.0], name='A')
        p3 = Point([1.0, 0.5], name='B')
        p4 = Point([1.0, 2.0], name='C')
        c = Cloud()
        c.add_point(p1)
        c.add_point(p2)
        c.add_point(p3)
        c.add_point(p4)
        g = graph_from_cloud(c)
        d = Dendrogram(g)
        #
        d.merge(g.edges[0])
        self.assertEqual(d.parent[1], 2)
        self.assertAlmostEqual(d.height[1], 0.25)
        #
        d.merge(g.edges[1])
        self.assertEqual(d.parent[1], 2)
        self.assertAlmostEqual(d.height[1], 0.25)
        self.assertEqual(d.parent[0], 2)
        self.assertAlmostEqual(d.height[0], 0.5)

    def test_build(self):
        c = Cloud()
        for x in [0.0, 1.0, 3.0, 4.0, 9.0]:
            c.add_point(Point([x]))
        g = graph_from_cloud(c)
        d = Dendrogram(g)
        d.build()
        self.assertEqual(d.parent, [1, 3, 3, -1, 3])
        self.assertEqual(d.left, [-1, 2, -1, -1, 1])
        self.assertEqual(d.down, [-1, 0, -1, 4, -1])
        height_ref = [0.5, 1.0, 0.5, -1, 2.5]
        for i in range(5):
            self.assertAlmostEqual(d.height[i], height_ref[i])

    def test_set_clusters(self):
        # Part 1...
        d = make_example()
        d.set_clusters(0.5)
        self.assertEqual(d.cluster, [1, 1, 3, 3, 4],
                         msg="Example with cut height = 1")
        # Part 2...
        d = make_example()
        d.set_clusters(1)
        self.assertEqual(d.cluster, [3, 3, 3, 3, 4],
                         msg="Example with cut height = 0.5")

    def test_count_ns_clusters(self):
        # Part 1...
        d = make_example()
        d.set_clusters(0.1)
        self.assertEqual(d.count_ns_clusters(), 0,
                         msg="Example with cut height = 0.1")
        # Part 2...
        d = make_example()
        d.set_clusters(0.5)
        self.assertEqual(d.count_ns_clusters(), 2,
                         msg="Example with cut height = 0.5")
        # Part 3...
        d = make_example()
        d.set_clusters(1)
        self.assertEqual(d.count_ns_clusters(), 1,
                         msg="Example with cut height = 1.0")

    def test_get_cluster_height(self):
        def gch_test(height, refs):
            d = make_example()
            d.set_clusters(height)
            #for i in range(5):
            #    print(f"[MOI] i = {i}, {d.get_cluster_height(i)}")
            for i in range(5):
                self.assertAlmostEqual(d.get_cluster_height(i), refs[i],
                                    msg=f"Example with cut height = {height}")
        gch_test(0.1, [0, 0, 0, 0, 0])
        gch_test(0.5, [0, 0.5, 0, 0.5, 0])
        gch_test(2.0, [0, 0, 0, 1.0, 0])
        gch_test(2.5, [0, 0, 0, 2.5, 0])


def suite(test_nb):
    suite = unittest.TestSuite()
    test_name = [
        "test_lt",
        "test_add_nodes",
        "test_add_edges",
        "test_graph_from_cloud",
        "test_graph_from_matrix",
        "test_graph_from_matrix_file",
        "test_find_rep",
        "test_merge",
        "test_build",
        "test_set_clusters",
        "test_count_ns_clusters",
        "test_get_cluster_height"
    ]

    if test_nb > 0:
        suite.addTest(Grader(test_name[test_nb - 1]))
    else:
        for name in test_name:
            suite.addTest(Grader(name))

    return suite


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
    try:
        test_nb = int(sys.argv[1])
    except ValueError as e:
        print(
            f"You probably didn't pass an int to ./grader.py: passed {sys.argv[1]}; error {e}"
        )
        exit(1)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite(test_nb))
