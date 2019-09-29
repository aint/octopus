#!/usr/bin/env python3

import io, os
from flask import Flask, request, send_file, render_template, Markup
from graphviz import create_node, create_record_node, update_record_node, Graphviz
import pydot

SVG_MIME_TYPE = 'image/svg+xml'

app = Flask(__name__)

@app.route('/')
def index():
    graph = Graphviz()
    file = graph.write("svg")
    return send_file(file, mimetype=SVG_MIME_TYPE)

@app.route('/<name>')
def get_node_details(name):
    name = name.lower()
    graph = Graphviz()
    node = graph.find_node_by_name(name)
    nodeGraph = pydot.Dot()
    nodeGraph.add_node(node)

    for e in graph.find_edges(name):
        dest_node = graph.find_node_by_name(e.get_destination())
        nodeGraph.add_node(dest_node)
        nodeGraph.add_edge(pydot.Edge(node.get_name(), e.get_destination()))

    nodeGraph.write(path=f"{name}.svg", format="svg")

    with open(f"{name}.svg", "r") as imageFile:
        f = imageFile.read().replace('\n', '')

    os.remove(f"{name}.svg")

    return render_template('service.html', title=name, desc="desc", img=Markup(f))

@app.route('/', methods=['POST'])
def parse_request():
    json = request.get_json()
    name = json["serviceName"]
    event_type = json["eventType"]
    metadata = json["serviceMetadata"]
    service_type = json["serviceType"]
    dependencies = json["dependencies"]

    graph = Graphviz()
    node_names = graph.node_names_list()

    if event_type == "DESTROY":
        app.logger.info('DESTROY event')
        if name in node_names:
            graph.del_edges_by_name(name)
            graph.del_node(name)

        graph.write("gv")
        file = graph.write("svg")

        return send_file(file, mimetype=SVG_MIME_TYPE)


    if name not in node_names:
        node_app = create_record_node(name, service_type, metadata)
        graph.add_node(node_app)
    else:
        node = graph.find_node_by_name(name)
        node_app = update_record_node(node, service_type, metadata)

    record_enabled = True

    edges = []
    for e in graph.find_edges(name):
        edges.append(e.get_destination())

    deps = []
    for dep in dependencies:
        for svc in dependencies[dep]:
            app.logger.info('svc: %s', svc)
            deps.append(svc)

            if svc not in edges:
                dep_type = dependency_type(dep)
                node_svc = create_record_node(svc, dep_type, "" if dep_type == "db" or dep_type == "3rd party" else "N/D")
                graph.add_node(node_svc)
                graph.add_edge(node_app, node_svc)

    for e in graph.find_edges(name):
        if e.get_destination() not in deps:
            graph.del_edge(name, e.get_destination())

    graph.write("gv") 
    file = graph.write("svg")

    return send_file(file, mimetype=SVG_MIME_TYPE)

def dependency_type(type):
    return {
        "services": "svc",
        "databases": "db",
        "lambdas": "fn",
        "third_party": "3rd party"
    }[type.lower()]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

def strip_quote(s: str):
    return s.strip('\"')


# - color configurable
# - event type
# - makefile
# - pipfile
# - readme
# - docker
# - saving GV source file

# class abstraction over Graph
# endpoint for deps of the specified service
# logging