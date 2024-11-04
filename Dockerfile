# Use the official Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the Python script to the Docker container
COPY stress.py /app/stress.py

# Install required Python packages (if there are any, e.g., psutil, mysql-connector-python)
RUN pip install psutil mysql-connector-python

# Install other tools if necessary (e.g., stress-ng, iperf3)
RUN apt-get update && apt-get install -y stress-ng iperf3 && apt-get clean

# Run the script
CMD ["python", "stress.py"]
