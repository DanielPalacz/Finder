# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set the working directory in the container
WORKDIR /app

# Update the package manager and install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    unzip \
    gnupg \
    software-properties-common \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    fonts-liberation \
    libatk1.0-0 \
    xdg-utils \
    chromium-browser \
    && apt-get clean

# Set Python3 as the default python command
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Copy requirements file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

RUN mkdir logs

# Set an entry point for the container
CMD ["python", "jobs.py"]
