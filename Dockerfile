# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# 1. Install prerequisite packages, including curl and jq for version detection
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    jq \
    --no-install-recommends

# 2. Download and install the latest Google Chrome
RUN wget -O /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# Use dpkg and apt-get -f to automatically install Chrome and all its dependencies
RUN dpkg -i /tmp/google-chrome-stable_current_amd64.deb || apt-get install -fy --no-install-recommends
RUN rm /tmp/google-chrome-stable_current_amd64.deb

# 3. Automatically detect the installed Chrome version and download the matching ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | cut -f 3 -d ' ' | cut -d '.' -f 1) && \
    echo "Detected Chrome version: $CHROME_VERSION" && \
    DRIVER_URL=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json" | jq -r ".milestones[\"$CHROME_VERSION\"].downloads.chromedriver[] | select(.platform==\"linux64\") | .url") && \
    echo "Downloading ChromeDriver from: $DRIVER_URL" && \
    wget -O /tmp/chromedriver.zip ${DRIVER_URL} && \
    unzip /tmp/chromedriver.zip -d /tmp && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ && \
    rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64

# 4. Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the Python script
COPY browse.py .

# 6. Set the command to run the script
CMD ["python", "browse.py"]
