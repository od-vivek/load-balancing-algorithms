# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application code into the container
COPY app.py .

# Install Flask (required dependency)

RUN pip install flask
RUN pip install psutil

# Expose port 5000 for the Flask application
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app.py"]
