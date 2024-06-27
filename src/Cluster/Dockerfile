FROM ubuntu:latest

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory in the container
WORKDIR /app

# Copy your Python script into the container
COPY server.py .

# Expose the port the server listens on
EXPOSE 65432

# Set the default command to run when the container starts
CMD ["python3", "server.py"]
