#!/usr/bin/env python3

from flask import Flask, request, send_file
from graphviz import parse_graph, create_node
import pydot

ELLIPSE_SHAPE = "ellipse"
BOX_SHAPE = "box"
OCTAGON_SHAPE = "octagon"

record_table = """<<table border='0' cellspacing='0'>
                    <tr><td port='port1' border='1' bgcolor='red'>{0}</td></tr>
                    <tr><td port='port2' border='1' bgcolor='gray'>{1}</td></tr>
                </table>>"""

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/consume', methods=['POST'])
def parse_request():
    print(request.is_json)
    content = request.get_json()
    print(content)
    name = content["serviceName"]
    print(name)

    graph = parse_graph()
    print(type(graph))

    node_names = []
    for node in graph.get_nodes():
        node_names.append(node.get_name().strip('\"'))

    print(node_names)

    if name not in node_names:
        node_app = pydot.Node(name, style = "filled", fillcolor = "#0000ff")
        graph.add_node(node_app)
    else:
        for node in graph.get_nodes():
            print(node.get_name().strip('\"'))
            if node.get_name().strip('\"') == name:
                node_app = node
                break

    record_enabled = True

    for dep in content["dependencies"]:
        dependencies = dep
        print(dependencies)
        for svc in content["dependencies"][dependencies]:
            print("svc: " + svc)
            if record_enabled:
                dep_type = dependency_type(dependencies)
                label = record_table.format(svc, dep_type)
                shape = "none"
            else:
                shape = node_shape(dependencies)

            print("shape: " + shape)

            if svc not in node_names:
                print(f"--{svc} not in nodes")
                node_svc = create_node(svc, shape, label)
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
    }[type.lower()]

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)