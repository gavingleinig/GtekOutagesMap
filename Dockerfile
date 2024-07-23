# Use the official Python 3.10 image from the Docker Hub
FROM python:3.10-slim

# Install Git
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV PORT 8080

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
