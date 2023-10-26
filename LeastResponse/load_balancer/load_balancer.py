import os
from flask import Flask, request, Response
import requests
import time

app = Flask(__name__)

backend_services = os.environ.get('BACKEND_SERVICES', '').split()

response_times = {service: 0 for service in backend_services}

current_service_index = 0

print(backend_services)
print(response_times)

request_number = 0

@app.route('/')
def load_balancer():
    global current_service_index, request_number
    request_number += 1
    min_response_time = min(response_times.values())
    for service, response_time in response_times.items():
        if response_time == min_response_time:
            current_service = service
            break

    try:
        start_time = time.time()
        response = requests.get(f'http://{current_service}', timeout=5)
        end_time = time.time()
        response_times[current_service] += (end_time - start_time)

        with open('logs.txt', 'a') as log_file:
            log_message = f"Request {request_number}: {response_times}\n"
            log_file.write(log_message)

        return Response(response.content, status=response.status_code, content_type=response.headers['content-type'])
    except requests.exceptions.RequestException as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
