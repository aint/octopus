#!/usr/bin/env python3

import io, os
from flask import Flask, request, send_file, render_template, Markup
from graphviz import parse_graph, create_node, create_record_node, update_record_node, node_names_list, find_edges, find_node_by_name
import pydot

SVG_MIME_TYPE = 'image/svg+xml'

app = Flask(__name__)

@app.route('/')
def index():
    graph = parse_graph()
    graph.write(path="graph.svg", format="svg")
    return send_file("graph.svg", mimetype=SVG_MIME_TYPE)

@app.route('/<name>')
def get_node_details(name):
    name = name.lower()
    graph = parse_graph()
    node = find_node_by_name(name, graph)
    nodeGraph = pydot.Dot()
    nodeGraph.add_node(node)

    for e in find_edges(graph, name):
        dest_node = find_node_by_name(e.get_destination(), graph)
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

    graph = parse_graph()
    node_names = node_names_list(graph)

    if event_type == "DESTROY":
        app.logger.info('DESTROY event')
        if name in node_names:
            for e in graph.get_edges():
                if e.get_source() == name or e.get_destination() == name:
                    r = graph.del_edge(e.get_source(), e.get_destination())
                    app.logger.info('DESTROY %s : %s', name, str(r))
            graph.del_node(name)

        graph.write(path="graph.svg", format="svg")
        graph.write("graph.gv")

        return send_file("graph.svg", mimetype=SVG_MIME_TYPE)


    if name not in node_names:
        node_app = create_record_node(name, service_type, metadata)
        graph.add_node(node_app)
    else:
        node = find_node_by_name(name, graph)
        node_app = update_record_node(node, service_type, metadata)

    record_enabled = True

    edges = []
    for e in find_edges(graph, name):
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
                graph.add_edge(pydot.Edge(node_app, node_svc))

    for e in find_edges(graph, name):
        if e.get_destination() not in deps:
            graph.del_edge(name, e.get_destination())

    graph.write("graph.gv")
    graph.write(path="graph.svg", format="svg")

    return send_file("graph.svg", mimetype=SVG_MIME_TYPE)

def dependency_type(type):
    return {
        "services": "svc",
        "databases": "db",
        "lambdas": "fn",
        "third_party": "3rd party"
    }[type.lower()]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
