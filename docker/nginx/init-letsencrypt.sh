#!/bin/bash

# Set default values from environment variables
DOMAIN_NAME=${DOMAIN_NAME:-giftq.com.au}
WWW_DOMAIN_NAME=${WWW_DOMAIN_NAME:-www.giftq.com.au}
CERTBOT_EMAIL=${CERTBOT_EMAIL:-captain@giftq.com.au}
SERVER_IP=${SERVER_IP:-13.238.104.108}

# Export variables for use in nginx templates
export DOMAIN_NAME WWW_DOMAIN_NAME SERVER_IP

# Define paths
LIVE_CERT_PATH="/etc/letsencrypt/live/${DOMAIN_NAME}"
FINAL_CONF_PATH="/etc/nginx/conf.d/default.conf"

# Function to check for valid Let's Encrypt certificates
has_valid_certs() {
    if [ -d "$LIVE_CERT_PATH" ]; then
        if openssl x509 -in "${LIVE_CERT_PATH}/fullchain.pem" -checkend 86400 -noout >/dev/null 2>&1; then
            echo "Valid, non-expired Let's Encrypt certificate found."
            return 0
        else
            echo "Certificate is expired or invalid. Will attempt renewal."
            return 1
        fi
    fi
    echo "No certificate found. Will attempt to acquire a new one."
    return 1
}

# Stage 1: Certificate Acquisition
if ! has_valid_certs; then
    echo "--- STAGE 1: ACQUIRING CERTIFICATE ---"
    # Clean up everything to ensure a pristine state for Certbot
    echo "Cleaning up /etc/letsencrypt directory..."
    rm -rf /etc/letsencrypt/*

    # Use the temporary config for the validation challenge
    echo "Processing temporary Nginx configuration..."
    envsubst '${DOMAIN_NAME} ${WWW_DOMAIN_NAME}' < /etc/nginx/conf.d/init.conf.template > "${FINAL_CONF_PATH}"

    echo "Starting Nginx temporarily for validation..."
    nginx -t
    nginx &
    sleep 5 # Give Nginx a moment to start

    # Use staging flag if set
    STAGING_FLAG=""
    if [ "${USE_STAGING:-false}" = "true" ]; then
        STAGING_FLAG="--staging"
        echo "Using Let's Encrypt STAGING environment."
    fi

    echo "Requesting new certificate from Let's Encrypt..."
    if certbot certonly --webroot --webroot-path=/var/www/certbot \
        --email "${CERTBOT_EMAIL}" \
        --agree-tos --no-eff-email --non-interactive \
        -d "${DOMAIN_NAME}" -d "${WWW_DOMAIN_NAME}" \
        --cert-name "${DOMAIN_NAME}" \
        $STAGING_FLAG; then
        echo "Certificate acquired successfully."
    else
        echo "ERROR: Certificate acquisition failed."
        echo "Please check DNS records and firewall settings."
        echo "Exiting."
        exit 1
    fi

    echo "Stopping temporary Nginx..."
    nginx -s stop
    sleep 5 # Wait for Nginx to shut down
fi

# Stage 2: Final SSL Configuration
echo "--- STAGE 2: CONFIGURING FINAL NGINX ---"
echo "Processing final Nginx SSL configuration..."
envsubst '${DOMAIN_NAME} ${WWW_DOMAIN_NAME} ${SERVER_IP}' < /etc/nginx/conf.d/default.conf.template > "${FINAL_CONF_PATH}"

echo "Starting Nginx with final SSL configuration..."
nginx -t

# Use `exec` to replace the script process with Nginx, making it the main container process.
# A subshell is used to run the renewal check in the background.
(
    while :; do
        echo "Renewal check running in background..."
        certbot renew --quiet
        sleep 12h
    done
) &

exec nginx -g 'daemon off;' 