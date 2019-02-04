#!/usr/bin/env python3

from typing import List
import pydot

record_table = """<<table border='0' cellspacing='0'>
                    <tr><td port='port1' border='1' bgcolor='red'>{0}</td></tr>
                    <tr><td port='port2' border='1' bgcolor='gray'>{1}</td></tr>
                    <tr><td port='port2' border='1' bgcolor='gray'>{2}</td></tr>
                </table>>"""

def parse_graph() -> pydot.Dot:
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
    label = record_table.format(name, dep_type, metadata)

    return pydot.Node(name, shape = "none", label = label)

def update_record_node(node, dep_type, metadata) -> pydot.Node:
    label = record_table.format(node.get_name(), dep_type, metadata)
    node.set("label", label)

    return node

def find_edges(graph: pydot.Dot, source: str) -> List[pydot.Edge]:
    edges = []
    for e in graph.get_edges():
        if e.get_source() == source:
            edges.append(e)

    return edges

def node_names_list(graph):
    node_names = []
    for node in graph.get_nodes():
        node_names.append(node.get_name().strip('\"'))

    return node_names
