# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for Chrome and the Chrome driver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# Install ChromeDriver
RUN wget https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.60/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/ \
    && rm chromedriver-linux64.zip

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY browse.py .

# Command to run the Python script
CMD ["python", "browse.py"]
