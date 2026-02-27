#!/usr/bin/env bash
#
# Refreshes UFW rules so that ports 80/443 (and 443/udp) are allowed only
# from current Cloudflare IP ranges. Run with sudo.
# Use this after initial vps-setup.sh when Cloudflare updates their IP list.
#
# Usage: sudo ./ufw-cloudflare-only.sh
#

set -e

CLOUDFLARE_IPS_V4="https://www.cloudflare.com/ips-v4"
CLOUDFLARE_IPS_V6="https://www.cloudflare.com/ips-v6"

echo "==> Removing existing Cloudflare-related UFW rules..."
for num in $(ufw status numbered | grep 'Cloudflare' | sed -n 's/^\[\s*\([0-9]*\)\].*/\1/p' | sort -rn); do
  ufw --force delete "$num"
done

echo "==> Adding current Cloudflare IPs for 80, 443 (tcp/udp)..."
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

ufw status numbered
echo "==> Done."
