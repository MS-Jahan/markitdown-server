# Start from a slim and stable Python base image
FROM python:3.12-slim

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system-level dependencies required by markitdown's converters
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    exiftool \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the entire project source code into the container
COPY . .

# Install the markitdown library and Flask using pip
RUN pip --no-cache-dir install markitdown[all] Flask

# Expose the port our Flask server will be listening on
EXPOSE 8080

# Define the command that will run when the container starts
CMD ["python", "server.py"]
