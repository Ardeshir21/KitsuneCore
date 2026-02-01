# Automatic SSL with Let's Encrypt & Nginx

This document explains how to set up fully automated SSL certificate generation and renewal for your production environment using Nginx and Certbot, integrated directly into Docker Compose.

The system uses a robust two-stage process to ensure reliability and avoid common errors.

---

### Key Features

- **Automated First-Time Setup**: Acquires an SSL certificate on the first run.
- **Handles Existing Certificates**: Correctly uses valid certificates if they already exist.
- **Integrated Auto-Renewal**: A background process within the Nginx container automatically renews certificates.
- **Simplified & Robust**: Eliminates the need for a separate Certbot container and avoids common state-related errors.
- **Zero Manual Steps**: After the initial setup, the entire process is hands-off.

---

### 1. Prerequisite: Environment Variables

Before you start, you must create a `.env` file in the root of your project. This is the central place for all your configuration.

Copy the following into your `.env` file and **update the values to match your domain and email**:

```env
# ----------------------------------------------------
# REQUIRED SSL CONFIGURATION
# ----------------------------------------------------
# The primary domain for your website.
DOMAIN_NAME=giftq.com.au

# The 'www' version of your domain.
WWW_DOMAIN_NAME=www.giftq.com.au

# The email address for Let's Encrypt notifications (e.g., expiry warnings).
CERTBOT_EMAIL=captain@giftq.com.au

# The public IP address of your server.
SERVER_IP=13.238.104.108

# ----------------------------------------------------
# Optional: For Testing
# ----------------------------------------------------
# Set to 'true' to use the Let's Encrypt staging server, which has higher
# rate limits and is ideal for testing. Staging certificates are not trusted
# by browsers. Remove this line or set to 'false' for production.
# USE_STAGING=true
```

---

### 2. How to Run It (First-Time Setup)

Follow these steps precisely for the initial launch to ensure a clean start.

**Step 1: Stop Any Running Services**
If you have containers running from previous attempts, stop them.
```bash
docker-compose -f docker-compose.prod.yml down
```

**Step 2: Clear Any Old Certificate Data (Crucial for First Run)**
This command removes the Docker volume where old, potentially corrupted certificate files are stored. This prevents errors on the first real run.
```bash
docker volume rm giftq_certbot_conf
```

**Step 3: Build the Nginx Image**
This builds your Nginx container with the latest startup scripts.
```bash
docker-compose -f docker-compose.prod.yml build --no-cache nginx
```

**Step 4: Launch the Services**
This will start all your services, and the Nginx container will automatically begin the certificate acquisition process.
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

### 3. How It Works: The Two-Stage Process

The system is designed to be intelligent and handle different scenarios.

**Scenario A: First-Time Run (No Certificate Found)**

1.  **Stage 1: Acquisition Mode**
    *   The script detects that no valid SSL certificate exists.
    *   It starts Nginx with a temporary, minimal configuration that only listens on port 80 to respond to the Let's Encrypt validation challenge.
    *   `certbot` runs and acquires a new SSL certificate.
    *   The temporary Nginx is stopped.
2.  **Stage 2: Production Mode**
    *   The script now swaps in your final, SSL-enabled Nginx configuration.
    *   Nginx is launched as the main container process, serving your site over HTTPS.
    *   A background renewal checker is started.

**Scenario B: Subsequent Runs (Valid Certificate Found)**

1.  **Validation**: The script starts, checks the certificate files in the Docker volume, and finds a valid, non-expired certificate.
2.  **Direct Launch**: It skips Stage 1 entirely and immediately launches Nginx with the final SSL configuration.
3.  **Renewal Check**: The background renewal checker is started as usual.

---

### 4. Troubleshooting

If you encounter issues, it's almost always related to one of these two things:

- **DNS Not Pointing to Server**: Let's Encrypt cannot validate your domain if the DNS A record for `giftq.com.au` and `www.giftq.com.au` does not point to your server's IP (`13.238.104.108`).
- **Firewall Blocking Ports**: Your server's firewall (e.g., `ufw` on Ubuntu or AWS Security Groups) must allow incoming traffic on **Port 80** (for the validation challenge) and **Port 443** (for HTTPS). 