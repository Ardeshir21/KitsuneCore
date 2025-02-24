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
# read APP_NAME from .env file
# Use an argument for build-time substitution
ARG APP_NAME

# Set an environment variable for runtime
ENV APP_NAME=${APP_NAME}

# Debugging: Print the app name during build
RUN echo "APP_NAME: $APP_NAME"

# Set the default command to run the application
CMD gunicorn --config ./docker/mainframe/gunicorn-cfg.py "${APP_NAME}.wsgi:application"