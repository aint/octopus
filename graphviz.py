#!/usr/bin/env python3

import pydot

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
