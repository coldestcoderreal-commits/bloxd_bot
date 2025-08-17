# 1. Use the official Playwright base image for Python.
FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

# 2. Set the working directory
WORKDIR /app

# 3. Force Python logs to be unbuffered so they appear instantly
ENV PYTHONUNBUFFERED=1

# 4. Install tools needed for downloading uBlock
RUN apt-get update && apt-get install -y wget unzip curl jq --no-install-recommends

# 5. Dynamically find and download the latest uBlock Origin release
RUN UBLOCK_URL=$(curl -s https://api.github.com/repos/gorhill/uBlock/releases/latest | jq -r ".assets[] | select(.name | endswith(\".chromium.zip\")) | .browser_download_url") && \
    echo "Downloading uBlock Origin from: ${UBLOCK_URL}" && \
    wget -O /tmp/ublock.zip "${UBLOCK_URL}" && \
    unzip /tmp/ublock.zip -d /app/ublock_extension && \
    rm /tmp/ublock.zip

# 6. Copy project files into the container
COPY requirements.txt .
COPY browse.py .

# 7. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 8. Set the command to run the script
CMD ["python", "browse.py"]
