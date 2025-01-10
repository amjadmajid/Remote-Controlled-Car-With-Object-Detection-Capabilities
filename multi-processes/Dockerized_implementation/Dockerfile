FROM python:3.9-slim-bullseye

# Install essential system dependencies and python3-pip in one RUN command
RUN apt-get update && apt-get install -y \
    cmake \
    git \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    libpng-dev \
    libpq-dev \
    libswscale-dev \
    libtiff-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    pkg-config \
    python3-dev \
    wget \
    libopenexr-dev \
    libopenblas-dev \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-bad1.0-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* # Cleanup

# Optimize OpenCV installation for Raspberry Pi
ARG OPENCV_VERSION=4.5.1.48
RUN pip install --extra-index-url https://www.piwheels.org/simple opencv-python-headless==${OPENCV_VERSION}

# Create a working directory for your application
WORKDIR /app

# Copy your application files into the container
COPY . /app

# Install your application's Python dependencies
RUN pip install -r requirements.txt

# Expose a port if your application needs it
EXPOSE 5000

# Define the command to run your application
CMD ["python", "CameraFeed.py"]

