# Dockerfile for Caddy reverse proxy
# Caddy automatically handles SSL/TLS certificates with Let's Encrypt

FROM caddy:2.8.4-alpine

# Create log directory
RUN mkdir -p /var/log/caddy

# Copy the Caddyfile configuration
COPY ./docker/caddy/Caddyfile /etc/caddy/Caddyfile

# Expose HTTP and HTTPS ports
EXPOSE 80
EXPOSE 443
EXPOSE 443/udp

# Caddy will automatically run with the Caddyfile
# Data persistence (certificates, etc.) is handled via volumes
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
