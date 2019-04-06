#!/usr/bin/env python3

from typing import List
import pydot
import os

record_table = """<<table border='0' cellspacing='0'>
                    <tr><td port='port1' border='1' bgcolor='{3}'>{0}</td></tr>
                    <tr><td port='port2' border='1' bgcolor='{4}'>{1}</td></tr>
                    <tr><td port='port2' border='1' bgcolor='{5}'>{2}</td></tr>
                </table>>"""

def parse_graph() -> pydot.Dot:
    if not os.path.exists("graph.gv"):
        pydot.Dot(graph_type='digraph').write("graph.gv")

    graphList = pydot.graph_from_dot_file("graph.gv", encoding = 'utf-8')
    print(type(graphList))
    graph = graphList[0]
    graph.set_strict(True) #TODO make it configurable
    return graph

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

def find_edges(graph: pydot.Dot, source: str) -> List[pydot.Edge]:
    edges = []
    for e in graph.get_edges():
        if e.get_source() == source:
            edges.append(e)

    return edges

def find_node_by_name(name, graph):
    for node in graph.get_nodes():
        if node.get_name().strip('\"') == name:
            return node
    raise ValueError("Graph doesn't contain node with specified name", name)

def node_names_list(graph):
    node_names = []
    for node in graph.get_nodes():
        node_names.append(node.get_name().strip('\"'))

    return node_names

def record_colors(type):
    return {
        "svc": ("#009f89", "#14877e", "#52c8be"),
        "db": ("#6cc400", "#6a9721", "#acde56"),
        "fn": ("#ff4300", "#b2593b", "#fe9777"),
        "3rd party": ("#ffba00", "#b89321", "#fdda59")
    }[type.lower()]