# Use Python 3.10 with Debian Buster as base image
FROM python:3.10-buster

# Set a working directory
WORKDIR /app
RUN mkdir /app/out
# Install system dependencies (if any specific ones are needed)
RUN apt-get update && apt-get install -y curl git

# Copy the requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script
COPY sub-nats-minio-api.py .

# Set the command to run the script
CMD ["python", "sub-nats-minio-api.py"]
