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

container_names = ["dynamic_weighted_load_balancer-app1-1", "dynamic_weighted_load_balancer-app2-1", "dynamic_weighted_load_balancer-app3-1"]

# Initialize a dictionary to store the health status of backend services
service_health = {service: True for service in backend_services}

@app.route('/')
def load_balancer():
    # Perform health checks and exclude unhealthy services
    active_services = [service for service in backend_services if service_health[service]]

    if not active_services:
        return "No healthy services available", 503

    # Retrieve CPU loads and calculate weights based on the CPU load
    cpu_loads = get_cpu_loads_from_containers(container_names)
    weights = [10 - (cpu_load['cpu_load'] / 10) for cpu_load in cpu_loads]

    # Perform weighted random selection
    backend_service = weighted_random_selection(active_services, weights)

    hostname, port = backend_service

    try:
        response = requests.get(f'http://{hostname}:{port}', timeout=5)
        return Response(response.content, status=response.status_code, content_type=response.headers['content-type'])
    except requests.exceptions.RequestException as e:
        # Handle errors and mark the service as temporarily unhealthy
        service_health[backend_service] = False
        return str(e), 500

def get_cpu_loads_from_containers(container_names):
    # Initialize an array to store the CPU loads
    cpu_loads = []

    for container_name in container_names:
        # Construct the URL with the specified port
        url = f'http://{container_name}:5000/cpu-load'

        try:
            # Make an API request to get CPU load information
            response = requests.get(url)
            response_data = response.json()
            cpu_load = response_data.get("cpu_load")

            if cpu_load is not None:
                cpu_loads.append({"container_name": container_name, "cpu_load": cpu_load})
            else:
                cpu_loads.append({"container_name": container_name, "error": "Invalid response data"})
        except Exception as e:
            cpu_loads.append({"container_name": container_name, "error": str(e)})

    return cpu_loads

def weighted_random_selection(population, weights):
    total_weight = sum(weights)
    target = random.uniform(0, total_weight)
    cumulative_weight = 0

    for i in range(len(population)):
        cumulative_weight += weights[i]
        if cumulative_weight >= target:
            return population[i]

    raise ValueError("Target weight out of bounds.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
