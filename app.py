#!/usr/bin/env python3

from flask import Flask, request, send_file
import pydot

ELLIPSE_SHAPE = "ellipse"
BOX_SHAPE = "box"

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/consume', methods=['POST'])
def parse_request():
    print(request.is_json)
    content = request.get_json()
    print(content)
    name = content["name"]
    print(name)
    dependencies = content["dependencies"]
    print(dependencies)

    graph = parse_graph(name)
    print(type(graph))

    node_names = []
    for node in graph.get_nodes():
        node_names.append(node.get_name().strip('\"'))

    print(node_names)

    if name not in node_names:
        node_app = pydot.Node(name, style = "filled", fillcolor = "#0000ff")
        graph.add_node(node_app)
    for entry in dependencies:
        print(entry)
        for k, v in entry.items():
            print("key: " + k)
            print("val: " + v)
            shape = node_shape(v)

            if k not in node_names:
                print(f"--{k} not in nodes")
                node_svc = pydot.Node(k, style = "filled", fillcolor = "green", shape = shape)
                graph.add_node(node_svc)
                graph.add_edge(pydot.Edge(node_app, node_svc))
            else:
                print(f"++{k} in nodes")

    graph.write_png(f"{name}.png")
    graph.write(f"{name}.gv")

    return send_file(f"{name}.png", mimetype='image/gif')

def node_shape(service_type):
    return BOX_SHAPE if service_type == "database" else ELLIPSE_SHAPE

def parse_graph(name) -> pydot.Dot:
    graphList = pydot.graph_from_dot_file(f"{name}.gv", encoding = 'utf-8')
    print(type(graphList))
    graph = graphList[0]
    graph.set_strict(True)
    return graph



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)