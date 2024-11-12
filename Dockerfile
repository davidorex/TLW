# Use the official Python 3.10 slim image as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Install gunicorn using pip
RUN pip install gunicorn

# Copy the entire project into the container
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput
