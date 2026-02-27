#!/usr/bin/env bash
#
# AurexLiving VPS initial setup (run once on a fresh Ubuntu VPS).
# - Installs Docker and Docker Compose
# - Configures UFW: SSH allowed; HTTP/HTTPS only from Cloudflare IPs
#
# Prerequisites:
# - Ubuntu 20.04+ (or Debian with minor adjustments)
# - Root or sudo access
# - SSH access via your PEM key (configure key-only auth on your side)
#
# Usage (repo is on GitHub; run from inside the cloned repo on the VPS):
#   ssh -i your.pem user@your-vps
#   git clone https://github.com/YOUR_ORG/AurexLiving.git && cd AurexLiving
#   chmod +x scripts/vps-setup.sh && sudo ./scripts/vps-setup.sh
#
# After this script, deploy with:
#   docker compose -f docker-compose.prod.yml up -d
#

set -e

CLOUDFLARE_IPS_V4="https://www.cloudflare.com/ips-v4"
CLOUDFLARE_IPS_V6="https://www.cloudflare.com/ips-v6"

echo "==> AurexLiving VPS setup (Docker + UFW + Cloudflare-only web traffic)"

# --- Docker ---
if ! command -v docker &> /dev/null; then
  echo "==> Installing Docker..."
  curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
  sh /tmp/get-docker.sh
  rm -f /tmp/get-docker.sh
  systemctl enable --now docker
else
  echo "==> Docker already installed."
fi

# --- Docker Compose plugin ---
if ! docker compose version &> /dev/null; then
  echo "==> Installing Docker Compose plugin..."
  apt-get update -qq
  apt-get install -y -qq docker-compose-plugin
else
  echo "==> Docker Compose plugin already installed."
fi

# --- Add current user to docker group (optional; skip if root) ---
if [ -n "$SUDO_USER" ] && [ "$SUDO_USER" != "root" ]; then
  if ! groups "$SUDO_USER" | grep -q docker; then
    usermod -aG docker "$SUDO_USER"
    echo "==> Added $SUDO_USER to group 'docker'. You may need to log out and back in for it to take effect."
  fi
fi

# --- UFW: SSH + HTTP/HTTPS from Cloudflare only ---
echo "==> Configuring UFW (SSH allowed; 80/443 only from Cloudflare)..."

ufw --force reset
ufw default deny incoming
ufw default allow outgoing

# SSH: allow so you can connect with your PEM from your laptop
ufw allow 22/tcp comment 'SSH (key-only; restrict to your IP later if desired)'

# HTTP/HTTPS only from Cloudflare IPs
for cidr in $(curl -sL "$CLOUDFLARE_IPS_V4"); do
  [ -z "$cidr" ] && continue
  ufw allow from "$cidr" to any port 80 proto tcp comment 'HTTP from Cloudflare'
  ufw allow from "$cidr" to any port 443 proto tcp comment 'HTTPS from Cloudflare'
  ufw allow from "$cidr" to any port 443 proto udp comment 'HTTP/3 QUIC from Cloudflare'
done
for cidr in $(curl -sL "$CLOUDFLARE_IPS_V6"); do
  [ -z "$cidr" ] && continue
  ufw allow from "$cidr" to any port 80 proto tcp comment 'HTTP from Cloudflare'
  ufw allow from "$cidr" to any port 443 proto tcp comment 'HTTPS from Cloudflare'
  ufw allow from "$cidr" to any port 443 proto udp comment 'HTTP/3 QUIC from Cloudflare'
done

# PgAdmin (5544): allow only from localhost so it's not exposed to the internet
ufw allow from 127.0.0.1 to any port 5544 proto tcp comment 'PgAdmin local only'

ufw --force enable
ufw status numbered

echo ""
echo "==> Setup complete."
echo "    - Docker and Docker Compose are installed."
echo "    - UFW is enabled: SSH (22) allowed; 80/443 only from Cloudflare; 5544 localhost only."
echo ""
echo "Next steps:"
echo "  1. Copy your app to the VPS (e.g. git clone or rsync)."
echo "  2. Put .env on the VPS and set DOMAIN_NAME, CERTBOT_EMAIL, etc."
echo "  3. Run:  docker compose -f docker-compose.prod.yml up -d"
echo ""
echo "To update Cloudflare IP rules later: re-run this script or run the 'scripts/ufw-cloudflare-only.sh' snippet."
