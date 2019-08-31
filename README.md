<p align="center">
	<img src="https://i.imgur.com/IfzW8Ce.png" alt="Octopus" width="500">
</p>
<h2 align="center">Microservice Architecture Visualization Tool </h3>

<p align="center">
    <a href="https://github.com/aint/octopus/graphs/commit-activity"><img src="https://img.shields.io/maintenance/yes/2019.svg"></a>
    <a href="https://travis-ci.org/aint/octopus"><img src="https://travis-ci.org/aint/octopus.svg?branch=master"></a>
	<a href="https://libraries.io/aint/octopus"><img src="https://img.shields.io/librariesio/github/aint/octopus.svg"></a>
	<br>
	<a href="https://sourcegraph.com/github.com/mholt/caddy?badge" title="Octopus on Sourcegraph"><img src="https://img.shields.io/sourcegraph/rrc/github.com/aint/octopus.svg" alt="Octopus on Sourcegraph"></a>
    <a href="https://github.com/aint"><img src="https://img.shields.io/badge/ask%20me-anything-1abc9c.svg"></a>
    <a href="http://flask.pocoo.org"><img src="https://img.shields.io/badge/made%20with-Python/Flask-1f425f.svg"></a>
    <a href="https://github.com/aint/octopus/blob/master/LICENSE"><img src="https://img.shields.io/github/license/aint/octopus.svg"></a>
    <a href="https://hub.docker.com/r/aint/octopus"><img src="https://img.shields.io/docker/pulls/aint/octopus.svg"></a>

</p>

---

**Octopus** is an open-source microservice architecture tool for visualizing dependency graph. It's simple and easy to use.

# Why

The microservice architecture has a lot of advantages but there are a lot disadvantages too. One of the main problem is that it can easily get out of control because of the quantity of the moving pieces. Especially if you just mindlessly jumped into the microservices hype.

**Octopus** aims to solve some of that issue by providing an overall dependency graph between microservices.

- you need it to paint the big picture. Don’t underestimate the value of seeing the big picture because you definitely need it even if you are not doing the architecture on daily basis
- you also need this to do some impact analysis

# Features
![](https://i.imgur.com/xeHAstb.png)

# Quick Start
```docker
docker pull aint/octopus:latest
docker run -it -p 5000:5000 aint/octopus:latest
```

Octopus server should now be running at [http://localhost:5000](http://localhost:5000)

Send some POST request with curl
```
curl -X POST \
  http://localhost:5000/ \
  -H 'Content-Type: application/json' \
  -d '{
    "eventType": "CREATE",
    "serviceName": "service-1",
    "serviceType": "svc",
    "serviceMetadata": "Java 8, Spring 5.0",
    "dependencies": {
        "SERVICES": [
            "service-2", "service-3",
        ],
        "DATABASES": [ "MySQL" ],
        "LAMBDAS": [],
        "THIRD_PARTY": []
    }
}'
```

Check out [http://localhost:5000](http://localhost:5000) to see a result.


# Contributing

# Code of Conduct
I don't care about your feelings.

# Licence
Apache License 2.0
