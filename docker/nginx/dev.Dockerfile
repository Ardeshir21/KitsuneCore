# Dockerfile_dev.nginx

# Start from the official Nginx image
FROM nginx:1.27.2

# Copy custom Nginx configuration file to the container
COPY ./docker/nginx/default_dev.conf /etc/nginx/conf.d/default.conf
