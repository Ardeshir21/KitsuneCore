# Migration Guide: nginx to Caddy

This guide explains the migration from nginx to Caddy in KitsuneCore.

## Changes Made

### 1. Replaced nginx with Caddy

**Before (nginx)**:
- Complex SSL certificate management with certbot
- Manual certificate renewal scripts
- Separate configurations for SSL and non-SSL
- Multiple files: nginx.conf, certbot scripts, cron jobs

**After (Caddy)**:
- Automatic SSL certificate management
- Zero configuration certificate renewals
- Simple, single configuration file
- Native Let's Encrypt integration

### 2. Simplified Docker Setup

**Before**:
- Separate nginx containers for dev and prod
- Volume mounts for certbot certificates
- Init scripts for SSL setup

**After**:
- Clean separation: `dev.Dockerfile` for dev, `Dockerfile` for prod
- Caddy data volumes for automatic certificate persistence
- No init scripts needed

### 3. Unified Mainframe Dockerfile

**Before**:
- `docker/mainframe/dev.Dockerfile` - Development with runserver
- `docker/mainframe/prod.Dockerfile` - Production with gunicorn

**After**:
- Single `docker/mainframe/Dockerfile` 
- Default CMD uses gunicorn (production)
- Dev overrides with `command: python manage.py runserver 0.0.0.0:9000`

## Docker Compose Changes

### Development (`docker-compose.dev.yml`)

**Key Changes**:
1. `mainframe` now uses unified `Dockerfile` with command override
2. `nginx` service replaced with `caddy`
3. HTTP only (port 80) for simpler local development
4. Removed SSL-related volumes

```yaml
# Old
nginx:
  dockerfile: ./docker/nginx/dev.Dockerfile
  ports:
    - "80:80"
    - "443:443"

# New
caddy:
  dockerfile: ./docker/caddy/dev.Dockerfile
  ports:
    - "80:80"  # HTTP only for dev
```

### Production (`docker-compose.prod.yml`)

**Key Changes**:
1. `mainframe` uses same unified `Dockerfile` (default gunicorn CMD)
2. `nginx` service replaced with `caddy`
3. Added `caddy_data` and `caddy_config` volumes
4. Removed `certbot_conf` and `certbot_www` volumes
5. Added HTTP/3 support (port 443/udp)

```yaml
# Old
nginx:
  dockerfile: ./docker/nginx/prod.Dockerfile
  volumes:
    - certbot_conf:/etc/letsencrypt
    - certbot_www:/var/www/certbot
  ports:
    - "80:80"
    - "443:443"

# New
caddy:
  dockerfile: ./docker/caddy/Dockerfile
  volumes:
    - caddy_data:/data
    - caddy_config:/config
  ports:
    - "80:80"
    - "443:443"
    - "443:443/udp"  # HTTP/3
```

## Configuration Mapping

### Static File Serving

**nginx**:
```nginx
location /static/ {
    alias /app/static/;
}
```

**Caddy**:
```caddy
handle /static/* {
    root * /app
    file_server
}
```

### Reverse Proxy

**nginx**:
```nginx
location / {
    proxy_pass http://mainframe:9000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

**Caddy**:
```caddy
handle {
    reverse_proxy mainframe:9000 {
        header_up Host {host}
        header_up X-Real-IP {remote_host}
    }
}
```

### SSL/TLS

**nginx**:
```nginx
ssl_certificate /etc/letsencrypt/live/domain/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/domain/privkey.pem;
# + 50+ lines of SSL configuration
```

**Caddy**:
```caddy
domain.com {
    tls email@example.com
    # That's it! Caddy handles everything
}
```

## Environment Variables

### Updated Variables

Some environment variables have changed:

| Old (nginx) | New (Caddy) | Notes |
|-------------|-------------|-------|
| `CERTBOT_EMAIL` | `CERTBOT_EMAIL` | Same, used for Let's Encrypt |
| `USE_STAGING` | N/A | Caddy uses production by default |

### New Variables (same as before)

- `DOMAIN_NAME` - Your primary domain
- `WWW_DOMAIN_NAME` - WWW subdomain
- `SERVER_IP` - Server IP for redirects

## Migration Steps

### For Development

1. Stop old containers:
   ```bash
   docker-compose -f docker-compose.dev.yml down
   ```

2. Remove old nginx volumes (optional):
   ```bash
   docker volume rm kitsunecore_nginx_cache
   ```

3. Start with new configuration:
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

### For Production

1. Backup current SSL certificates (optional - Caddy will get new ones):
   ```bash
   docker cp kitsunecore-nginx-1:/etc/letsencrypt ./letsencrypt-backup
   ```

2. Stop old containers:
   ```bash
   docker-compose -f docker-compose.prod.yml down
   ```

3. Update `.env` file with required variables

4. Start with Caddy:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

5. Caddy will automatically obtain certificates from Let's Encrypt (takes ~30 seconds)

6. Verify HTTPS is working:
   ```bash
   curl -I https://your-domain.com
   ```

## Benefits of Migration

1. **Reduced Complexity**: No more certbot scripts, cron jobs, or manual SSL management
2. **Better Security**: Automatic certificate renewals, modern TLS defaults
3. **Improved Performance**: HTTP/3 support, better connection handling
4. **Easier Maintenance**: Simple, readable configuration files
5. **Zero Downtime**: Certificate renewals happen automatically without restarts

## Troubleshooting

### Certificates not obtained

Check Caddy logs:
```bash
docker-compose logs caddy
```

Ensure:
- Domain DNS points to your server
- Ports 80 and 443 are accessible
- `CERTBOT_EMAIL` is set correctly

### HTTP instead of HTTPS

Caddy obtains certificates on first request. Try accessing your domain via browser, wait 30 seconds, then refresh.

### Old nginx containers still running

```bash
docker ps | grep nginx
docker stop <container-id>
docker rm <container-id>
```

## Rollback Plan

If you need to rollback to nginx:

1. Stop Caddy containers:
   ```bash
   docker-compose down
   ```

2. Checkout previous nginx configuration from git:
   ```bash
   git checkout HEAD~1 docker-compose.*.yml docker/nginx/
   ```

3. Restore separate mainframe Dockerfiles if needed

4. Start with old configuration:
   ```bash
   docker-compose up -d
   ```

## Additional Resources

- [Caddy Documentation](https://caddyserver.com/docs/)
- [Caddyfile Concepts](https://caddyserver.com/docs/caddyfile/concepts)
- [Automatic HTTPS](https://caddyserver.com/docs/automatic-https)
