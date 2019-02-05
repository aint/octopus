#!/usr/bin/env python3

from flask import Flask, request, send_file
from graphviz import parse_graph, create_node, create_record_node, update_record_node, node_names_list, find_edges
import pydot

ELLIPSE_SHAPE = "ellipse"
BOX_SHAPE = "box"
OCTAGON_SHAPE = "octagon"

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

def find_node_by_name(name, graph):
    for node in graph.get_nodes():
        if node.get_name().strip('\"') == name:
            return node
    raise ValueError("Graph doesn't contain node with specified name", name)

@app.route('/consume', methods=['POST'])
def parse_request():
    json = request.get_json()
    name = json["serviceName"]
    event_type = json["eventType"]
    metadata = json["serviceMetadata"]
    dependencies = json["dependencies"]

    graph = parse_graph()
    node_names = node_names_list(graph)

    if event_type == "DESTROY":
        print("DESTROY")
        if name in node_names:
            for e in graph.get_edges():
                if e.get_source() == name or e.get_destination() == name:
                    r = graph.del_edge(e.get_source(), e.get_destination())
                    print("DESTROY " + name + " :" + str(r))
            graph.del_node(name)

        graph.write(path="graph.svg", format="svg")
        graph.write("graph.gv")

        return send_file("graph.svg", mimetype='image/svg')


    if name not in node_names:
        node_app = create_record_node(name, "svc", metadata)
        graph.add_node(node_app)
    else:
        node = find_node_by_name(name, graph)
        node_app = update_record_node(node, "svc", metadata)

    record_enabled = True

    edges = []
    for e in find_edges(graph, name):
        edges.append(e.get_destination())

    deps = []
    for dep in dependencies:
        for svc in dependencies[dep]:
            print("svc: " + svc)
            deps.append(svc)

            if svc not in edges:
                dep_type = dependency_type(dep)
                node_svc = create_record_node(svc, dep_type, "N/D")
                graph.add_node(node_svc)
                graph.add_edge(pydot.Edge(node_app, node_svc))

    for e in find_edges(graph, name):
        if e.get_destination() not in deps:
            graph.del_edge(name, e.get_destination())

    graph.write(path="graph.svg", format="svg")
    graph.write("graph.gv")

    return send_file("graph.svg", mimetype='image/svg')

def node_shape(service_type):
    return {
        "services": ELLIPSE_SHAPE,
        "databases": BOX_SHAPE,
        "lambdas": OCTAGON_SHAPE,
    }[service_type.lower()]


def dependency_type(type):
    return {
        "services": "svc",
        "databases": "db",
        "lambdas": "fn",
        "third_party": "3rd party"
    }[type.lower()]

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)