# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the load balancer script into the container
COPY load_balancer.py .

# Install Flask and requests (required dependencies)
RUN pip install flask requests

# Expose port 80 for the Flask application
EXPOSE 80

# Define the command to run the load balancer script
CMD ["python", "load_balancer.py"]
