#!/usr/bin/env python3

from typing import List
import pydot
import os

record_table = """<<table border='0' cellspacing='0'>
                    <tr><td port='port1' border='1' bgcolor='{3}'>{0}</td></tr>
                    <tr><td port='port2' border='1' bgcolor='{4}'>{1}</td></tr>
                    <tr><td port='port2' border='1' bgcolor='{5}'>{2}</td></tr>
                </table>>"""

# def render(filename = None):
#     graph.write("graph.gv")
#     graph.write(path="graph.svg", format="svg")
#     return

# def parse_graph() -> pydot.Dot:
#     if not os.path.exists("graph.gv"):
#         pydot.Dot(graph_type='digraph').write("graph.gv")

#     graphList = pydot.graph_from_dot_file("graph.gv", encoding = 'utf-8')
#     graph = graphList[0]
#     graph.set_strict(True) #TODO make it configurable
#     return graph

def create_node(name, shape, label = None) -> pydot.Node:
    if label == None:
        return pydot.Node(name, style = "filled", fillcolor = "green", shape = shape)
    else:
        return pydot.Node(name, shape = shape, label = label)

def create_record_node(name, dep_type, metadata) -> pydot.Node:
    c1, c2, c3 = record_colors(dep_type)
    label = record_table.format(name, dep_type, metadata, c1, c3, c3)

    return pydot.Node(name, shape = "none", label = label, URL = "/" + name)

def update_record_node(node, dep_type, metadata) -> pydot.Node:
    c1, c2, c3 = record_colors(dep_type)
    label = record_table.format(node.get_name(), dep_type, metadata, c1, c3, c3)
    node.set("label", label)

    return node

# def find_edges(graph: pydot.Dot, source: str) -> List[pydot.Edge]:
#     edges = []
#     for e in graph.get_edges():
#         if e.get_source() == source:
#             edges.append(e)

#     return edges

# def find_node_by_name(name, graph):
#     for node in graph.get_nodes():
#         if node.get_name().strip('\"') == name:
#             return node
#     raise ValueError("Graph doesn't contain node with specified name", name)

# def node_names_list(graph):
#     node_names = []
#     for node in graph.get_nodes():
#         node_names.append(node.get_name().strip('\"'))

#     return node_names

def record_colors(type):
    return {
        "svc": ("#009f89", "#14877e", "#52c8be"),
        "db": ("#6cc400", "#6a9721", "#acde56"),
        "fn": ("#ff4300", "#b2593b", "#fe9777"),
        "3rd party": ("#ffba00", "#b89321", "#fdda59")
    }[type.lower()]

class Graphviz:
    def __init__(self):
        if not os.path.exists("graph.gv"):
            pydot.Dot(graph_type='digraph').write("graph.gv")

        graphList = pydot.graph_from_dot_file("graph.gv", encoding = 'utf-8')
        graph: pydot.Dot = graphList[0]
        graph.set_strict(True) #TODO make it configurable

        self.graph = graph

    def find_edges(self, source: str) -> List[pydot.Edge]:
        edges = []
        for e in self.graph.get_edges():
            if e.get_source() == source:
                edges.append(e)

        return edges

    def node_names_list(self) -> List[str]:
        node_names = []
        for node in self.graph.get_nodes():
            node_names.append(node.get_name().strip('\"'))

        return node_names

    def find_node_by_name(self, name):
        for node in self.graph.get_nodes():
            if node.get_name().strip('\"') == name:
                return node
        raise ValueError("Graph doesn't contain node with specified name", name)

    def add_node(self, node_svc):
        self.graph.add_node(node_svc)

    def del_node(self, name):
        self.graph.del_node(name)

    def add_edge(self, node_app, node_svc):
        self.graph.add_edge(pydot.Edge(node_app, node_svc))

    def del_edge(self, src, dst):
        self.graph.del_edge(src, dst)

    def del_edges_by_name(self, name):
        for e in self.graph.get_edges():
            if e.get_source() == name or e.get_destination() == name:
                r = self.graph.del_edge(e.get_source(), e.get_destination())
                print('Deleting %s : %s', name, str(r))

    def write(self, format):
        graph_path = "graph." + format
        self.graph.write(path=graph_path, format=format)
        return graph_path