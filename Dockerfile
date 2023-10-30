# Use the official Python 3.11 image
# FROM --platform=arm64 python:3.11.4-bookworm
# ARG BUILDPLATFORM
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
    libsqlite3-mod-spatialite \
    vim

# Create directory
RUN mkdir /code

# Set the working directory to /code
WORKDIR /code

# Mirror the current directory to the working directory for hotreloading
ADD . /code/

# Install pipenv
RUN pip install --no-cache-dir -r linux-requirements.txt

# Make migrations
RUN python stude/manage.py makemigrations

# Run custom migrate
RUN python stude/manage.py custom_migrate

# Generate DRF Spectacular Documentation
RUN python stude/manage.py spectacular --color --file stude/schema.yml

# Expose port 8000 for the web server
EXPOSE 8000
