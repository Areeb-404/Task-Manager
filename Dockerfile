# Starting With An Official Python 3.12 Image
FROM python:3.12-slim

# Setting the working directory inside the container's file system
WORKDIR /app

# Copying the requirements.txt first
COPY requirements.txt .

# Install the python packages inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Copying the rest of the local files into the container
COPY . .

# Informing Docker that the app listens on port 8000 at runtime for requests
EXPOSE 8000

# Execution command to boot the fastapi app when the container starts
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]

# The host ip address is 0.0.0.0 as this address tells uvicorn to listen to all virtual network interfaces inside the container so that the windows web browser can send requests to the VM
