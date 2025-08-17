# 1. Use the official Playwright base image for Python.
# This image includes Python, Playwright, and all necessary browser dependencies.
# Using a specific version tag ensures reproducibility.
FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

# 2. Set the working directory
WORKDIR /app

# 3. Copy project files into the container
COPY requirements.txt .
COPY browse.py .

# 4. Install Python dependencies from requirements.txt
# The base image already includes Playwright, but this ensures the version is locked.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Set the command to run the script
CMD ["python", "browse.py"]
