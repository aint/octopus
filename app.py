#!/usr/bin/env python3

from flask import Flask, request, send_file
from graphviz import parse_graph, create_node, create_record_node, update_record_node
import pydot

ELLIPSE_SHAPE = "ellipse"
BOX_SHAPE = "box"
OCTAGON_SHAPE = "octagon"

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/consume', methods=['POST'])
def parse_request():
    json = request.get_json()
    name = json["serviceName"]
    metadata = json["serviceMetadata"]
    dependencies = json["dependencies"]

    graph = parse_graph()

    node_names = []
    for node in graph.get_nodes():
        node_names.append(node.get_name().strip('\"'))

    if name not in node_names:
        dep_type = "svc"
        node_app = create_record_node(name, dep_type, metadata)
        graph.add_node(node_app)
    else:
        for node in graph.get_nodes():
            if node.get_name().strip('\"') == name:
                node_app = node
                dep_type = "svc"
                node_app = update_record_node(node, dep_type, metadata)
                break

    record_enabled = True

    for dep in dependencies:
        for svc in dependencies[dep]:
            print("svc: " + svc)
            if record_enabled:
                dep_type = dependency_type(dep)
                shape = "none"
            else:
                shape = node_shape(dep)

            if svc not in node_names:
                print(f"--{svc} not in nodes")
                node_svc = create_record_node(svc, dep_type, "N/D")
                graph.add_node(node_svc)
            else:
                print(f"++{svc} in nodes")
                for node in graph.get_nodes():
                    print(node.get_name().strip('\"'))
                    if node.get_name().strip('\"') == svc:
                        node_svc = node
                        print(node_svc.get_sequence())
                        break
                        # pydot.Edge.get_destination()
                        # pydot.Edge.get_source()

            graph.add_edge(pydot.Edge(node_app, node_svc))

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