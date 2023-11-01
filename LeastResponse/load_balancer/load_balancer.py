import os
from flask import Flask, request, Response
import requests
import time

app = Flask(__name__)

backend_services = os.environ.get('BACKEND_SERVICES', '').split()

# Use a dictionary to store the health status of each backend service
service_health = {service: True for service in backend_services}

print(backend_services)

request_number = 0

@app.route('/')
def load_balancer():
    global request_number
    request_number += 1

    # Filter out unhealthy services
    active_services = [service for service in backend_services if service_health[service]]

    if not active_services:
        return "No healthy services available", 503

    # Implement a load balancing algorithm here, e.g., least response time, round-robin, etc.
    current_service = active_services[request_number % len(active_services)]

    try:
        start_time = time.time()
        response = requests.get(f'http://{current_service}', timeout=5)
        end_time = time.time()
        response_time = end_time - start_time

        # Update the response times based on the actual response time
        response_times[current_service] = response_time

        with open('logs.txt', 'a') as log_file:
            log_message = f"Request {request_number}: {response_times}\n"
            log_file.write(log_message)

        return Response(response.content, status=response.status_code, content_type=response.headers['content-type'])

    except requests.exceptions.RequestException as e:
        # Handle errors and mark the service as unhealthy
        service_health[current_service] = False
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
