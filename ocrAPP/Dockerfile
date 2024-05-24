# Use an official Python runtime as a parent image
FROM python:3.10.2-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container to /app
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Update and install necessary libraries
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Copy requirements.txt to the working directory
COPY requirements.txt ./

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose port 8000 for the application
EXPOSE 8000

# Define the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]