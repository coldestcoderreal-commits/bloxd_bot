# 1. Use the official Playwright base image for Python.
FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

# 2. Set the working directory
WORKDIR /app

# --- ADD THIS LINE ---
# Set the PYTHONUNBUFFERED environment variable to force logs to appear instantly
ENV PYTHONUNBUFFERED=1

# 3. Copy project files into the container
COPY requirements.txt .
COPY browse.py .

# 4. Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Set the command to run the script
CMD ["python", "browse.py"]
