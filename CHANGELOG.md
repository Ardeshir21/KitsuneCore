# Changelog

All notable changes to the KitsuneCore project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-01

### Added
- **Caddy Reverse Proxy**: Complete migration from nginx to Caddy
  - Automatic SSL/TLS certificate management with Let's Encrypt
  - HTTP/3 (QUIC) support for improved performance
  - Simplified configuration with Caddyfile format
  - Zero-downtime certificate renewals
  - Production Dockerfile with automatic HTTPS
  - Development Dockerfile with HTTP-only configuration
  - Comprehensive documentation (README, MIGRATION-GUIDE, DEV-SETUP, COMPARISON)

- **Docker Infrastructure**:
  - Unified mainframe Dockerfile for both development and production
  - Caddy data volumes for automatic certificate persistence (`caddy_data`, `caddy_config`)
  - HTTP/3 port configuration (443/udp) in production

- **Documentation**:
  - `docker/caddy/README.md` - Caddy overview and usage guide
  - `docker/caddy/MIGRATION-GUIDE.md` - Detailed migration steps from nginx
  - `docker/caddy/DEV-SETUP.md` - Development environment setup
  - `docker/caddy/COMPARISON.md` - Side-by-side nginx vs Caddy comparison

### Changed
- **Docker Compose Configuration**:
  - `docker-compose.dev.yml`:
    - Mainframe service now uses unified Dockerfile with command override
    - Replaced nginx service with caddy service
    - Removed unused HTTPS port (443) from development
    - Simplified volume structure
  
  - `docker-compose.prod.yml`:
    - Mainframe service uses unified Dockerfile with default gunicorn command
    - Replaced nginx service with caddy service
    - Added HTTP/3 support on port 443/udp
    - Replaced certbot volumes with Caddy data volumes
    - Added default environment variable values for easier deployment

- **Mainframe Container**:
  - Consolidated `docker/mainframe/dev.Dockerfile` and `prod.Dockerfile` into single `Dockerfile`
  - Default CMD uses gunicorn for production (can be overridden for development)
  - Development mode uses command override: `python manage.py runserver 0.0.0.0:9000`

- **Reverse Proxy Configuration**:
  - Simplified from ~520 lines (nginx) to ~174 lines (Caddy) - 67% reduction
  - Automatic HTTPS configuration replaces manual certbot setup
  - Cleaner, more readable Caddyfile syntax
  - Consistent configuration between development and production

### Removed
- **nginx Infrastructure** (deprecated, can be cleaned up):
  - `docker/nginx/` directory and all nginx configurations
  - `docker/nginx/dev.Dockerfile` - Replaced by Caddy
  - `docker/nginx/prod.Dockerfile` - Replaced by Caddy
  - `docker/nginx/default_dev.conf` - Replaced by Caddyfile.dev
  - `docker/nginx/default_prod.conf` - Replaced by Caddyfile
  - `docker/nginx/init-letsencrypt.sh` - No longer needed with Caddy
  - `docker/nginx/init.conf.template` - No longer needed
  - `docker/mainframe/dev.Dockerfile` - Replaced by unified Dockerfile
  - `docker/mainframe/prod.Dockerfile` - Replaced by unified Dockerfile

- **Certbot Dependencies**:
  - Manual certificate management scripts
  - Certbot volumes (`certbot_conf`, `certbot_www`)
  - Certificate renewal cron jobs (Caddy handles automatically)
  - SSL initialization scripts

- **Environment Variables**:
  - `USE_STAGING` - No longer needed (Caddy uses production Let's Encrypt by default)

### Fixed
- **SSL/TLS Management**:
  - Eliminated manual certificate setup complexity
  - Removed potential for certificate expiration issues
  - Fixed certificate renewal requiring manual intervention
  - Resolved SSL configuration complexity and potential misconfigurations

- **Development Experience**:
  - Simplified local development setup (HTTP only, no SSL complexity)
  - Eliminated need for separate dev and prod Dockerfiles for mainframe
  - Reduced configuration file maintenance burden

### Security
- **Automatic Certificate Management**:
  - Caddy automatically obtains and renews SSL certificates from Let's Encrypt
  - Zero-downtime certificate renewals without manual intervention
  - Automatic HTTPS redirects from HTTP
  - Modern TLS defaults and cipher suites

- **Improved Security Defaults**:
  - Caddy uses secure-by-default configuration
  - Automatic optimal TLS settings without manual configuration
  - Built-in OCSP stapling and security headers
  - HTTP/3 support for improved security and performance

- **Reduced Attack Surface**:
  - Eliminated separate certbot service and potential vulnerabilities
  - Simplified configuration reduces misconfiguration risks
  - Integrated certificate management reduces external dependencies

### Technical Details
- **Caddy Version**: 2.8.4-alpine
- **Python Version**: 3.12-bookworm (unchanged)
- **Gunicorn Configuration**: 3 workers, debug logging, auto-reload enabled
- **Request Body Limit**: 30MB for file uploads
- **Proxy Timeouts**: 500 seconds (read, write, dial)

### Performance Improvements
- **HTTP/3 Support**: Built-in QUIC protocol support for faster connections
- **Reduced Resource Usage**: Single integrated service vs nginx + certbot
- **Faster Certificate Operations**: No external certbot process needed
- **Better Connection Handling**: Modern HTTP protocol support

### Migration Impact
- **Configuration Complexity**: Reduced by 67% (520 lines → 174 lines)
- **Maintenance Time**: Estimated 2-3 hours/month saved on certificate management
- **Deployment Time**: Faster deployments with automatic certificate handling
- **Learning Curve**: Simpler configuration for new team members

### Backward Compatibility
- ✅ All existing environment variables remain compatible
- ✅ Same port mappings (80, 443)
- ✅ Same volume structure for static/media files
- ✅ No changes to Django application code required
- ✅ Database configuration unchanged

### Rollback Plan
If needed, rollback to nginx is straightforward:
1. Stop Caddy containers: `docker-compose down`
2. Checkout previous nginx configuration from git
3. Restore separate mainframe Dockerfiles if needed
4. Start with old configuration: `docker-compose up -d`

---

## Version Guidelines

### Version Format: MAJOR.MINOR.PATCH

- **MAJOR**: Incompatible API changes or major feature overhauls
- **MINOR**: New features in a backwards-compatible manner
- **PATCH**: Backwards-compatible bug fixes

### Change Categories

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements
- **Performance**: Performance improvements
- **Technical Details**: Implementation specifics

### Release Notes

When releasing a new version:
1. Move changes from `[Unreleased]` to a new version section
2. Add release date in format `[X.Y.Z] - YYYY-MM-DD`
3. Update version numbers in relevant files
4. Create git tag for the release
5. Update documentation if needed

### Example Entry Format

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- Feature description with details
  - Sub-feature or implementation detail
  - Another detail

### Changed
- What changed and why
  - Specific file or component affected
  - Impact of the change

### Security
- Security improvement description
  - What vulnerability was addressed
  - How it was fixed
```
