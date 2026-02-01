# Dockerfile_prod.nginx

# Start from the official Nginx image
FROM nginx:1.27.2

# Install certbot, openssl, gettext, and curl for certificate management and testing
RUN apt-get update && apt-get install -y \
    certbot \
    openssl \
    gettext-base \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Nginx configuration templates to the container
COPY ./docker/nginx/default_prod.conf /etc/nginx/conf.d/default.conf.template
COPY ./docker/nginx/init.conf.template /etc/nginx/conf.d/init.conf.template

# Copy the initialization script
COPY ./docker/nginx/init-letsencrypt.sh /usr/local/bin/init-letsencrypt.sh

# Make the script executable
RUN chmod +x /usr/local/bin/init-letsencrypt.sh

# Set the entrypoint to our initialization script
ENTRYPOINT ["/usr/local/bin/init-letsencrypt.sh"]
