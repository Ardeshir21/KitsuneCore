# Dockerfile for Caddy reverse proxy - Development
# Simplified configuration without SSL complexity

FROM caddy:2.8.4-alpine

# Copy the development Caddyfile
COPY ./docker/caddy/Caddyfile.dev /etc/caddy/Caddyfile

# Expose only HTTP port for development
EXPOSE 80

# Caddy will automatically run with the Caddyfile
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
