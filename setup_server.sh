#!/bin/bash

set -e # Exit on any error
set -x # log executed lines

DOMAIN="diamondhandsllc.com"
EMAIL="diamondhandsllc.company@google.com"
FLASK_PORT=5000

sudo apt update && sudo apt upgrade -y

sudo apt install -y nginx certbot python3-certbot-nginx docker.io docker-compose docker-buildx

echo "Building and starting Flask app with Docker Compose..."
docker-compose up --build -d

echo "Configuring Nginx..."
NGINX_CONF="/etc/nginx/sites-available/$DOMAIN"
sudo tee $NGINX_CONF > /dev/null <<EOL
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    location / {
        proxy_pass http://localhost:$FLASK_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOL

echo "Enabling Nginx configuration..."
sudo ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

echo "Obtaining SSL certificate with Let's Encrypt..."
sudo certbot --nginx --non-interactive --agree-tos -m $EMAIL -d $DOMAIN -d www.$DOMAIN

echo "Setting up auto-renewal for SSL certificates..."
sudo crontab -l | { cat; echo "0 0 * * * certbot renew --quiet && systemctl reload nginx"; } | sudo crontab -

echo "All done! Your Flask app is now accessible at https://$DOMAIN"
