# Caddy Configuration for KitsuneCore

This directory contains Caddy reverse proxy configurations for KitsuneCore, replacing the previous nginx setup.

## Why Caddy?

Caddy offers several advantages over nginx:

1. **Automatic HTTPS**: Caddy automatically obtains and renews SSL/TLS certificates from Let's Encrypt
2. **Simpler Configuration**: No complex SSL setup or certificate management scripts needed
3. **HTTP/3 Support**: Built-in support for the latest HTTP protocols including QUIC
4. **Zero Downtime Reloads**: Configuration changes can be applied without restarts
5. **Better Defaults**: Secure defaults out of the box

## Files

- `Dockerfile` - Production Caddy image with HTTPS support
- `dev.Dockerfile` - Development Caddy image (HTTP only)
- `Caddyfile` - Production configuration with automatic HTTPS
- `Caddyfile.dev` - Development configuration (HTTP only, simpler)

## Development Setup

For local development, the dev configuration runs on HTTP only (port 80) without SSL certificates:

```bash
docker-compose -f docker-compose.dev.yml up
```

Access the application at: http://localhost

## Production Setup

For production, Caddy automatically handles HTTPS with Let's Encrypt:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables

Make sure your `.env` file contains:

```env
CERTBOT_EMAIL=your-email@example.com
DOMAIN_NAME=kitsunecore.com
WWW_DOMAIN_NAME=www.kitsunecore.com
SERVER_IP=your.server.ip
```

Caddy will automatically:
- Obtain SSL certificates from Let's Encrypt
- Redirect HTTP to HTTPS
- Handle certificate renewals
- Redirect IP access to your domain

## Features

### Automatic HTTPS

Caddy automatically obtains certificates from Let's Encrypt on first run. No manual certificate management needed!

### HTTP/3 Support

Production configuration includes HTTP/3 (QUIC) support on port 443/udp for better performance.

### Request Size Limits

Both configurations set a 30MB request body size limit for file uploads.

### Logging

- **Development**: Console output (stdout) for easy debugging
- **Production**: JSON logs saved to `/var/log/caddy/access.log`

## Migration from nginx

The previous nginx setup required:
- Manual certificate setup with certbot
- Complex SSL configuration
- Separate init scripts for certificate management
- Certificate renewal cron jobs

With Caddy, all of this is handled automatically!

## Troubleshooting

### View Caddy logs

```bash
docker-compose logs caddy
```

### Check certificate status

Caddy stores certificates in the `caddy_data` volume. To inspect:

```bash
docker-compose exec caddy ls -la /data/caddy/certificates
```

### Test configuration

```bash
docker-compose exec caddy caddy validate --config /etc/caddy/Caddyfile
```

## Volume Management

- `caddy_data`: Persistent storage for certificates and Caddy data
- `caddy_config`: Configuration cache for better performance

These volumes ensure certificates persist across container restarts.
