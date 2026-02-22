# VPS setup (Ubuntu)

> **This content is included in the main [SETUP-GUIDE.md](SETUP-GUIDE.md) as section 5 (VPS setup — Docker + Cloudflare firewall).** Use that guide for the current steps and script paths (`vps-scripts/`). This file is kept for reference.

One-time setup on a fresh Ubuntu VPS so you can run the app with Docker and lock down the firewall to Cloudflare-only for web traffic. SSH stays open so you can connect with your PEM key from your laptop.

## What the setup script does

- **Docker** – Installs Docker Engine (official script).
- **Docker Compose** – Installs the Compose plugin (`docker compose`).
- **UFW** – Configures the firewall:
  - **SSH (22)** – Allowed so you can connect with your PEM key (restrict to your IP later if you want).
  - **80, 443 (tcp), 443 (udp)** – Allowed **only** from [Cloudflare IP ranges](https://www.cloudflare.com/ips/) (matches orange cloud + Full Strict).
  - **5544** – Allowed only from `127.0.0.1` (PgAdmin from the server only).
  - Default: deny incoming, allow outgoing.

## Point the domain to this VPS (DNS)

After the VPS is ready, point `aurexliving.com.au` to it so the site stops showing the default GoDaddy page.

**1. Get your VPS public IP**  
From your VPS provider’s dashboard or by running on the VPS: `curl -s ifconfig.me`.

**2. In GoDaddy DNS (or wherever the domain’s DNS is managed):**

- **A records for `aurexliving.com.au`**  
  You currently have two A records (e.g. `13.248.243.5` and `76.223.105.230`). Update them so the root domain points only to your new VPS:
  - Either **edit one** A record to your VPS IP and **delete** the other, or  
  - **Edit both** so both A records use your **VPS public IP** (one IP is enough; two identical A records are optional for redundancy).
- **Leave these as-is:**  
  - **www** (CNAME → `aurexliving.com.au`)  
  - **NS** records  
  - **TXT** (e.g. `_dmarc`)  
  - **CNAME** `_domainconnect` (GoDaddy)

**3. Propagation**  
DNS can take from a few minutes up to 24–48 hours. After it propagates, `aurexliving.com.au` and `www.aurexliving.com.au` will resolve to your VPS. Ensure the app is running on the VPS (`docker compose -f docker-compose.prod.yml up -d`) and that the firewall allows HTTP/HTTPS as in the setup above.

## Prerequisites

- Ubuntu 20.04+ (or similar Debian-based).
- Root or sudo.
- SSH access to the VPS using your PEM key (you configure key-only auth on your side).

## Run the setup once

The setup scripts live in the repo, so you use the project from GitHub on the VPS.

**1. From your laptop: SSH into the VPS** (with your PEM key):

```bash
ssh -i /path/to/your.pem user@your-vps-ip
```

**2. On the VPS: get the project and run the setup script**

First time (clone; replace with your GitHub repo URL if different):

```bash
git clone https://github.com/YOUR_ORG/AurexLiving.git
cd AurexLiving
chmod +x scripts/vps-setup.sh
sudo ./scripts/vps-setup.sh
```

Later (already cloned – pull then run if you need to re-run setup):

```bash
cd AurexLiving
git pull
sudo ./scripts/vps-setup.sh
```

If you’re not root, you may need to log out and back in after the script so your user is in the `docker` group.

## Deploy the app (after setup)

On the VPS, from the repo root (with `.env` in place):

```bash
cd AurexLiving   # if not already there
docker compose -f docker-compose.prod.yml up -d
```

Ensure `.env` has at least:

- `DOMAIN_NAME`, `WWW_DOMAIN_NAME`
- `CERTBOT_EMAIL`
- Any DB and app secrets your stack needs

## Optional: refresh Cloudflare IP rules

When Cloudflare updates their IP list, refresh UFW rules without reinstalling Docker:

```bash
sudo ./scripts/ufw-cloudflare-only.sh
```

You can run this periodically or after [Cloudflare IP list](https://www.cloudflare.com/ips/) changes.

## Restricting SSH to your IP (optional)

If you want only your laptop to reach SSH, add your home IP and then remove the generic “allow 22” rule. Example (replace `YOUR_HOME_IP`):

```bash
sudo ufw allow from YOUR_HOME_IP to any port 22 comment 'SSH from my laptop'
# Then remove the generic "allow 22" rule by number:
# sudo ufw status numbered   # find the 22/tcp rule number
# sudo ufw delete <number>
```

## Files

| File | Purpose |
|------|--------|
| `scripts/vps-setup.sh` | One-time: install Docker, Docker Compose, configure UFW (SSH + Cloudflare-only 80/443). |
| `scripts/ufw-cloudflare-only.sh` | Re-apply Cloudflare-only rules for 80/443 (e.g. after Cloudflare IP list updates). |
