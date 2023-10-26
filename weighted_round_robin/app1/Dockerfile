# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask and any other dependencies (if needed)
RUN pip install flask

# Expose the port the application will run on
EXPOSE 5000


# Define the command to run the application
CMD ["python", "app.py"]
