# Caddy Development Setup

Quick guide for setting up KitsuneCore with Caddy for local development.

## Quick Start

```bash
# Start all services
docker-compose -f docker-compose.dev.yml up

# Or in detached mode
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f
```

Access the application at: **http://localhost**

## Development Configuration

The development setup uses:

- **HTTP only** (no HTTPS) - Faster startup, no certificate hassles
- **Port 80** - Standard HTTP port
- **Live reload** - Changes to code are reflected immediately
- **Console logging** - Easy to debug with readable console output

## Architecture

```
┌─────────────┐
│   Browser   │
│ localhost:80│
└──────┬──────┘
       │
       │ HTTP
       │
┌──────▼──────────────┐
│   Caddy Container   │
│   (Reverse Proxy)   │
└──────┬──────────────┘
       │
       │ Forward to
       │
┌──────▼──────────────────┐
│  Mainframe Container    │
│  Django Development     │
│  python manage.py       │
│  runserver 0.0.0.0:9000 │
└─────────────────────────┘
```

## File Watching

The mainframe container uses volume mounts for live code reloading:

```yaml
volumes:
  - .:/app  # Your code is mounted here
```

Any changes you make to Python files will trigger Django's auto-reloader.

## Static & Media Files

Static and media files are served by Caddy:

- `/static/` - Django static files (CSS, JS, images)
- `/media/` - User uploaded content
- `/favicon.ico` - Site favicon

These are mounted as volumes and shared between containers.

## Useful Commands

### View Caddy access logs
```bash
docker-compose -f docker-compose.dev.yml logs caddy
```

### View Django logs
```bash
docker-compose -f docker-compose.dev.yml logs mainframe
```

### Restart just Caddy
```bash
docker-compose -f docker-compose.dev.yml restart caddy
```

### Restart just mainframe
```bash
docker-compose -f docker-compose.dev.yml restart mainframe
```

### Rebuild containers
```bash
docker-compose -f docker-compose.dev.yml up --build
```

### Stop all services
```bash
docker-compose -f docker-compose.dev.yml down
```

### Stop and remove volumes
```bash
docker-compose -f docker-compose.dev.yml down -v
```

## Database Access

PostgreSQL is exposed on port 5544:

```bash
psql -h localhost -p 5544 -U your_db_user -d your_db_name
```

Or use a GUI tool like pgAdmin connecting to `localhost:5544`.

## Testing HTTPS Locally (Optional)

If you need to test HTTPS features locally, uncomment this section in `Caddyfile.dev`:

```caddy
localhost {
    tls internal
    
    # ... rest of configuration
}
```

Then access via: **https://localhost**

Caddy will generate a self-signed certificate. Your browser will show a security warning (this is normal for local dev).

## Customizing the Port

To use a different port than 80:

1. Edit `docker-compose.dev.yml`:
   ```yaml
   caddy:
     ports:
       - "8080:80"  # Use port 8080 instead
   ```

2. Access at: http://localhost:8080

## Troubleshooting

### Port 80 already in use

If another service is using port 80:

```bash
# Find what's using port 80 (Windows)
netstat -ano | findstr :80

# Kill the process
taskkill /PID <pid> /F

# Or change the port in docker-compose.dev.yml
```

### Container fails to start

Check logs for errors:
```bash
docker-compose -f docker-compose.dev.yml logs
```

Common issues:
- Port conflicts
- Missing `.env` file
- Database connection issues

### Static files not loading

Collect static files:
```bash
docker-compose -f docker-compose.dev.yml exec mainframe python manage.py collectstatic --noinput
```

### Can't connect to database

Ensure database container is running:
```bash
docker-compose -f docker-compose.dev.yml ps
```

Restart database:
```bash
docker-compose -f docker-compose.dev.yml restart db
```

## Performance Tips

1. **Use volumes for dependencies**: Consider adding a volume for pip packages to avoid reinstalling on every build

2. **Exclude large directories**: Make sure `.dockerignore` excludes:
   - `node_modules/`
   - `__pycache__/`
   - `.git/`
   - `*.pyc`

3. **Use BuildKit**: Enable Docker BuildKit for faster builds:
   ```bash
   export DOCKER_BUILDKIT=1
   ```

## Next Steps

- See [README.md](README.md) for general Caddy information
- See [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) for migration details from nginx
- Check [Production setup](README.md#production-setup) for deploying to production
