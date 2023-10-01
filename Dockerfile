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
    cron \
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

# Copy the cronjob file
COPY cronjob /etc/cron.d/cronjob

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cronjob

# Apply cron job
RUN crontab /etc/cron.d/cronjob

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Set editor as VIM
RUN export EDITOR=vim

# Run the command on container startup
CMD cron

# Expose port 8000 for the web server
EXPOSE 8000
