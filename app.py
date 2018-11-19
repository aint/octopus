#!/usr/bin/env python3

from flask import Flask, request
from graphviz import Digraph

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

    graph = Digraph('G', filename = name + '.gv', format = 'png')

    for entry in dependencies:
        print(entry)
        for k, v in entry.items():
            print("key: " + k)
            print("val: " + v)
            if v == "database":
                graph.attr('node', shape='box')
                print("database")
            else:
                graph.attr('node', shape='ellipse')
            graph.edge(name, k)

    graph.render()

    return 'JSON posted\n' + graph.source

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)