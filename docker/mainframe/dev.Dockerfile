# Dockerfile.dev

# Use a specific Python version
FROM python:3.12-bookworm

# Set the working directory
WORKDIR /app

# Copy requirements.txt into the container
COPY ./requirements.txt ./

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the files
COPY . .

# Expose the port that the app will run on
EXPOSE 9000

# Command to run the application (can be overridden in docker-compose.yml)
CMD ["gunicorn", "--config", "./docker/mainframe/gunicorn-cfg.py", "KitsuneCore.wsgi:application"]

