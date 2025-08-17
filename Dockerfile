# 1. Use the official Playwright base image for Python.
FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

# 2. Set the working directory
WORKDIR /app

# 3. Force Python logs to be unbuffered so they appear instantly
ENV PYTHONUNBUFFERED=1

# 4. Copy project files into the container
COPY requirements.txt .
COPY browse.py .

# 5. Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 6. Set the command to run the script
CMD ["python", "browse.py"]
