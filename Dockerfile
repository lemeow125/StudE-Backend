# Use the official Python 3.11 image
# FROM --platform=arm64 python:3.11.4-bookworm
FROM python:3.11.4-bookworm

ENV PYTHONBUFFERED 1

# Install necessary dependencies, including cmake
RUN apt-get update && apt-get install -y \
    wget \
    tar \
    cmake \
    proj-bin \
    libgeos-c1v5 \
    libproj-dev \
    libfreexl1 \
    libminizip-dev \
    libspatialite-dev \
    gdal-bin \
    libsqlite3-mod-spatialite

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install pipenv
RUN pip install -r linux-requirements.txt

# Make migrations
RUN python stude/manage.py makemigrations

# Run custom migrate
RUN python stude/manage.py custom_migrate

# Expose port 8000 for the web server
EXPOSE 8000

# Run the web server
CMD ["python", "stude/manage.py", "runserver"]