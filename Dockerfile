# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Update and install prerequisite packages
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    --no-install-recommends

# Download Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install Google Chrome and its dependencies.
# dpkg will fail, but the subsequent apt-get -f install will fix the broken dependencies.
RUN dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -fy --no-install-recommends
RUN rm google-chrome-stable_current_amd64.deb

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
