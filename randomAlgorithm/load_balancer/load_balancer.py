import random
from flask import Flask, request, Response
import requests

app = Flask(__name__)

# List of backend services with their hostnames and ports
backend_services = [
    ("app1", 5000),
    ("app2", 5000),
    ("app3", 5000),
]


@app.route('/')
def load_balancer():
    backend_service = random.choice(backend_services)
    hostname, port = backend_service

    try:
        response = requests.get(f'http://{hostname}:{port}', timeout=5)
        return Response(response.content, status=response.status_code, content_type=response.headers['content-type'])
    except requests.exceptions.RequestException as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
