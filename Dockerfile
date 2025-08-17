# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# 1. Update apt and copy project files
RUN apt-get update && apt-get install -y --no-install-recommends
COPY requirements.txt .
COPY browse.py .

# 2. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 3. Install Playwright's browser (Chromium) and its system dependencies
# The --with-deps flag is crucial as it automatically installs all necessary system libraries.
RUN playwright install --with-deps chromium

# 4. Set the command to run the script
CMD ["python", "browse.py"]
