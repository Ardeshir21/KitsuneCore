# Project Setup Guide

This guide covers local setup, installing libraries, deploying to an AWS server, and **VPS setup (Ubuntu)** with Docker and a Cloudflare-only firewall — see **section 5**.

---

## 1. Local Setup — Start Project

### 1.1 Prepare the codebase

1. Take a copy of the KitsuneCore repository.
2. Remove the hidden `.git` folder.
3. Rename the KitsuneCore folder to your project name.

### 1.2 Review and update configuration

Review and adjust these files for your project:

| File | Purpose |
|------|--------|
| **`.env`** | Environment variables (DB, secrets, URLs). |
| **`init.sql`** (e.g. `docker/database/init.sql`) | Database initialization. |

**Vue frontend only:**

| File | Purpose |
|------|--------|
| **`package.json`** | App name, scripts, dependencies. |

### 1.3 Build icons (Vue frontend only)

If `iconify/icons.css` does not exist, enter the frontend container and run the build:

```bash
docker exec -it kitsunecore-frontend-1 /bin/bash
```

Inside the container:

```bash
pnpm run build:icons
```

### 1.4 Start the stack

From the project root:

```bash
docker compose -f docker-compose.dev.yml up --build -d
```

### 1.5 Django: migrations and superuser (development)

Enter the mainframe container:

```bash
docker exec -it kitsunecore-mainframe-1 /bin/bash
```

Inside the container:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

**Production:** Do not run `makemigrations` on the server. Run only:

```bash
python manage.py migrate
python manage.py collectstatic
```

---

## 2. Set up social account login (e.g. Google)

To allow users to sign in with Google (or other OAuth providers), configure the provider and your app so the **callback URL** matches. Django-allauth uses a fixed path; the domain comes from how users reach your site.

### 2.1 Configure the OAuth provider (e.g. Google Cloud Console)

1. In [Google Cloud Console](https://console.cloud.google.com/), create or select a project and go to **APIs & Services → Credentials**.
2. Create an **OAuth 2.0 Client ID** (application type: Web application).
3. Under **Authorized redirect URIs**, add the **exact** callback URL(s) your app will use:

   | Environment | Redirect URI |
   |-------------|----------------|
   | Local      | `http://127.0.0.1:8000/accounts/google/login/callback/` |
   | Production | `https://yourdomain.com/accounts/google/login/callback/` |
   | With www   | `https://www.yourdomain.com/accounts/google/login/callback/` |

   Format: `{origin}/accounts/google/login/callback/` (include the trailing slash).

4. Copy the **Client ID** and **Client secret**; you will add them in Django Admin (see below).

### 2.2 Set your site URL in `.env`

Ensure `SITE_URL` in `.env` matches the base URL users use to access your app so that links and the OAuth callback domain are consistent:

- **Local:** `SITE_URL=http://127.0.0.1:8000` (or the host/port you use).
- **Production:** `SITE_URL=https://yourdomain.com` (or `https://www.yourdomain.com` if you use www).

The callback URL Django builds uses the request host; `SITE_URL` should match that domain.

### 2.3 Add the social app in Django Admin

1. Run migrations and create a superuser if you have not already (see **1.5**).
2. Log in to Django Admin: `http://127.0.0.1:8000/admin/` (or your `SITE_URL`).
3. Open **Sites → Sites** and ensure the site with **SITE_ID=1** has the correct **Domain name** (e.g. `yourdomain.com` or `127.0.0.1:8000` for local).
4. Open **Social applications → Social applications** → **Add**.
5. Choose **Provider:** Google.
6. Enter **Client id** and **Client secret** from the Google Cloud Console.
7. Under **Sites**, move your site (e.g. **example.com**) from “Available sites” to “Chosen sites” and save.

### 2.4 Quick checklist

| Where | What to set |
|-------|-----------------------------|
| **Google (or other) OAuth app** | Authorized redirect URI: `https://yourdomain.com/accounts/google/login/callback/` (and the same for http + port for local if needed). |
| **`.env`** | `SITE_URL=https://yourdomain.com` in production (and `http://127.0.0.1:8000` for local). |
| **Django Admin → Sites** | Domain for the site with **SITE_ID=1** matches the domain above. |
| **Django Admin → Social applications** | Add a Google (or other) social app with client id/secret and assign the site. |

For other providers (e.g. Facebook, GitHub), use the same idea: register the callback URL `{origin}/accounts/{provider}/login/callback/` in the provider’s app settings and add the app under **Social applications** in Django Admin.

---

## 3. Install a New Library

To add a Python dependency and use it in the mainframe container:

**Option A — shell into container, then install:**

```bash
docker exec -it kitsunecore-mainframe-1 /bin/bash
# inside container:
pip install requests
```

**Option B — one-liner:**

```bash
docker exec -it kitsunecore-mainframe-1 pip install requests
```

Add the new package to your project’s `requirements.txt` (or equivalent) so it is installed on future builds.

---

## 4. AWS Server Setup

### Step 1: Connect to the EC2 instance

```bash
ssh -i your-key.pem ec2-user@your-aws-instance-ip
```

### Step 2: Install Docker and Docker Compose

**Amazon Linux:**

```bash
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user
```

**Ubuntu:**

```bash
sudo apt update -y
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

**Docker Compose (both):**

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

Log out and log back in so the `docker` group takes effect:

```bash
exit
ssh -i your-key.pem ec2-user@your-aws-instance-ip
```

### Step 3: Install Git and set up SSH (for GitHub)

**Install Git (Amazon Linux):**

```bash
sudo yum install git -y
git --version
```

**SSH key for GitHub (on the server):**

```bash
ssh-keygen -t ed25519
eval "$(ssh-agent -s)"
```

Move the created key into `~/.ssh` and add it:

```bash
ssh-add ~/.ssh/Created_Key_File
```

**Optional — SSH config for GitHub:**

Edit or create `~/.ssh/config`:

```
Host github.com
  HostName ssh.github.com
  Port 443
  User git
  IdentityFile ~/.ssh/Created_Key_File
  AddKeysToAgent yes
```

Test:

```bash
ssh -T git@github.com
```

**Clone the repo:**

1. Copy the **public** key and add it as a deploy key (or SSH key) in the GitHub repo settings.
2. Clone (replace with your repo URL):

   ```bash
   git clone git@github.com:YourOrg/YourRepo.git
   git remote -v
   ```

### Step 4: Build and run with Docker Compose

**Important:** Check `.env` and `init.sql` (or your DB init script) before running.

```bash
cd your-repo
docker compose -f docker-compose.prod.yml up -d --build
```

**Useful commands:**

| Command | Purpose |
|--------|---------|
| `docker ps` | List running containers |
| `docker compose -f docker-compose.prod.yml logs` | Compose logs |
| `docker logs -f <container>` | Follow one container |
| `docker exec -it <container> bash` | Shell into container |
| `docker compose -f docker-compose.prod.yml down -v` | Stop and remove volumes |
| `docker compose -f docker-compose.prod.yml down` | Stop (no volume removal) |

---

## 5. VPS setup (Ubuntu) — Docker + Cloudflare firewall

One-time setup on a fresh Ubuntu VPS so you can run the app with Docker and lock down the firewall to Cloudflare-only for web traffic. SSH stays open so you can connect with your PEM key from your laptop.

### 5.1 What the setup script does

- **Docker** – Installs Docker Engine (official script).
- **Docker Compose** – Installs the Compose plugin (`docker compose`).
- **UFW** – Configures the firewall:
  - **SSH (22)** – Allowed so you can connect with your PEM key (restrict to your IP later if you want).
  - **80, 443 (tcp), 443 (udp)** – Allowed **only** from [Cloudflare IP ranges](https://www.cloudflare.com/ips/) (orange cloud + Full Strict).
  - **5544** – Allowed only from `127.0.0.1` (PgAdmin from the server only).
  - Default: deny incoming, allow outgoing.

### 5.2 Point the domain to this VPS (DNS)

After the VPS is ready, point your domain to it so the site resolves to your app.

**1. Get your VPS public IP**  
From your VPS provider’s dashboard or by running on the VPS: `curl -s ifconfig.me`.

**2. In your DNS provider (e.g. GoDaddy, Cloudflare):**

- **A records for your root domain**  
  Point the root domain to your VPS: create or edit an A record so it uses your **VPS public IP**.
- **www** – Use a CNAME to your root domain (e.g. `www` → `yourdomain.com`) or an A record to the same IP.
- Leave NS, TXT, and other existing records as needed.

**3. Propagation**  
DNS can take from a few minutes up to 24–48 hours. After it propagates, your domain and `www` will resolve to your VPS. Ensure the app is running (`docker compose -f docker-compose.prod.yml up -d`) and that the firewall allows HTTP/HTTPS as in the setup above.

### 5.3 Prerequisites

- Ubuntu 20.04+ (or similar Debian-based).
- Root or sudo.
- SSH access to the VPS using your PEM key (key-only auth on your side).

### 5.4 Run the setup once

The setup scripts live in the repo under `vps-scripts/`.

**1. From your laptop: SSH into the VPS** (with your PEM key):

```bash
ssh -i /path/to/your.pem user@your-vps-ip
```

**2. On the VPS: get the project and run the setup script**

First time (clone; replace with your GitHub repo URL):

```bash
git clone https://github.com/YOUR_ORG/KitsuneCore.git
cd KitsuneCore
chmod +x vps-scripts/vps-setup.sh
sudo ./vps-scripts/vps-setup.sh
```

Already cloned – pull then run if you need to re-run setup:

```bash
cd KitsuneCore
git pull
sudo ./vps-scripts/vps-setup.sh
```

If you’re not root, log out and back in after the script so your user is in the `docker` group.

### 5.5 Deploy the app (after setup)

On the VPS, from the repo root (with `.env` in place):

```bash
cd KitsuneCore   # if not already there
docker compose -f docker-compose.prod.yml up -d
```

Ensure `.env` has at least:

- `DOMAIN_NAME`, `WWW_DOMAIN_NAME` (for Caddy)
- `CERTBOT_EMAIL` (for Caddy / Let’s Encrypt)
- `SITE_URL` (e.g. `https://yourdomain.com`)
- Any DB and app secrets your stack needs

### 5.6 Optional: refresh Cloudflare IP rules

When Cloudflare updates their IP list, refresh UFW rules without reinstalling Docker:

```bash
sudo ./vps-scripts/ufw-cloudflare-only.sh
```

Run this periodically or after [Cloudflare IP list](https://www.cloudflare.com/ips/) changes.

### 5.7 Optional: restrict SSH to your IP

To allow only your laptop to reach SSH, add your home IP and then remove the generic “allow 22” rule (replace `YOUR_HOME_IP`):

```bash
sudo ufw allow from YOUR_HOME_IP to any port 22 comment 'SSH from my laptop'
# Then remove the generic "allow 22" rule by number:
# sudo ufw status numbered   # find the 22/tcp rule number
# sudo ufw delete <number>
```

### 5.8 VPS script files

| File | Purpose |
|------|--------|
| `vps-scripts/vps-setup.sh` | One-time: install Docker, Docker Compose, configure UFW (SSH + Cloudflare-only 80/443). |
| `vps-scripts/ufw-cloudflare-only.sh` | Re-apply Cloudflare-only rules for 80/443 (e.g. after Cloudflare IP list updates). |

---

## 6. PEM key (Windows) — connection issues

If you have trouble connecting with your `.pem` file on Windows:

1. In **File Explorer**, right-click the `.pem` file → **Properties**.
2. Open the **Security** tab → **Advanced**.
3. **Disable inheritance** → **Remove all inherited permissions**.
4. **Add** → **Select a principal** → enter your Windows username → **Check Names** → **OK**.
5. Grant **Read** only → **OK** → **Apply** → **OK**.

---

## 7. Multi-language app (server)

On the server, install gettext for Django translations:

```bash
sudo apt-get update
sudo apt install gettext
```

(On Amazon Linux you may use `sudo yum install gettext` if the package is available.)

---

## Appendix A: HTTPS and SSL with Nginx + Certbot (archived)

This section is kept for reference only. The project uses Caddy for the reverse proxy and automatic HTTPS; Nginx is no longer used.

Only on the **host** where the app runs (not inside containers for cert generation).

1. Edit the Nginx config for your domain.
2. Install Certbot:
   - **Amazon Linux:** `sudo yum install -y certbot`
   - **Ubuntu:** `sudo apt-get install certbot`
3. Stop the stack temporarily so port 80 is free:
   ```bash
   docker compose -f docker-compose.prod.yml down
   ```
4. Generate certificates (replace with your domain):
   ```bash
   sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com -d mail.yourdomain.com
   ```
5. Certificates are saved under:
   - `/etc/letsencrypt/live/yourdomain.com/fullchain.pem`
   - `/etc/letsencrypt/live/yourdomain.com/privkey.pem`
6. Use your `default_prod_ssl` (or equivalent) Nginx config, point it to these paths, and in `docker-compose.prod.yml` mount the SSL certs and use the SSL Nginx config.

**Renewal:** Stop the stack, run Certbot, then start again:

```bash
docker compose -f docker-compose.prod.yml down
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
docker compose -f docker-compose.prod.yml up -d
```
