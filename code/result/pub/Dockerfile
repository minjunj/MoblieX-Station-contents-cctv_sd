# Use Python 3.9 as base image
FROM python:3.10-slim

# Set a working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libopencv-dev \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install opencv-python==4.6.0.66
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script
COPY pub-nats-minio-face-detection.py .

# Set the command to run the script
CMD ["python", "pub-nats-minio-face-detection.py"]
