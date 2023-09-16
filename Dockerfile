# alpine slim
FROM python:3.10-slim

# Maintainer
LABEL maintainer="Rafal Nowak"

COPY . /app

# Install vlc and pip
RUN apt-get update && apt-get install -y vlc && apt-get install -y python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r /app/requirements.txt && \
    apt-get purge -y --auto-remove python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set the default directory where CMD will execute \
WORKDIR /app

# Expose port 5017
EXPOSE 5017

# Run app.py when the container launches
CMD ["python3", "main.py"]
