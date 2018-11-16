#!/usr/bin/env python3

from flask import Flask, request

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

    return 'JSON posted'

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)