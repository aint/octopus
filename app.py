#!/usr/bin/env python3

from flask import Flask, request, send_file
import pydot

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

    graph = Digraph('G', filename = f"{name}.gv", format = 'png')

    graphList = pydot.graph_from_dot_file(f"{name}.gv", encoding = 'utf-8')
    graph = graphList[0]
    graph.set_strict(True)
    print(type(graphList))
    print(type(graph))

    node_app = pydot.Node(name, style = "filled", fillcolor = "#0000ff")
    graph.add_node(node_app)
    for entry in dependencies:
        print(entry)
        for k, v in entry.items():
            print("key: " + k)
            print("val: " + v)
            node_shape = ""
            if v == "database":
                node_shape = 'box'
                print("database")
            else:
                node_shape = 'ellipse'

            node_svc = pydot.Node(k, style = "filled", fillcolor = "green", shape = node_shape)
            graph.add_node(node_svc)
            graph.add_edge(pydot.Edge(node_app, node_svc))

    graph.write_png(f"{name}.png")
    graph.write(f"{name}.gv")

    return send_file(f"{name}.png", mimetype='image/gif')

    return send_file(f"{name}.gv.png", mimetype='image/gif')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)