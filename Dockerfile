# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
# PREVENT Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# PREVENT Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
# DEBIAN FRONTEND to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
# ffmpeg and libsm6/libxext6 are required for opencv and audio processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port that Gradio listens on (Updated to 7880)
EXPOSE 7880

# Define the command to run the application
# Using --server-name 0.0.0.0 is crucial for Docker networking
CMD ["python", "main.py"]
