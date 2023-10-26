import os
from flask import Flask, request, Response
import requests

app = Flask(__name__)

backend_services = os.environ.get('BACKEND_SERVICES', '').split()

current_service_index = 0


@app.route('/')
def load_balancer():
    global current_service_index
    service = backend_services[current_service_index]

    try:
        response = requests.get(f'http://{service}', timeout=5)
        return Response(response.content, status=response.status_code, content_type=response.headers['content-type'])
    except requests.exceptions.RequestException as e:
        return str(e), 500
    finally:
        current_service_index = (
            current_service_index + 1) % len(backend_services)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

