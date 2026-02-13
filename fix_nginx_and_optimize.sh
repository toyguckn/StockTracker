#!/bin/bash

DOMAIN="146.190.29.129.nip.io"
NGINX_CONF_PATH="./nginx_conf"

echo "### Fixing Nginx Configuration for $DOMAIN ..."

mkdir -p "$NGINX_CONF_PATH"
cat > "$NGINX_CONF_PATH/default.conf" <<EOF
server {
    listen 80;
    server_name $DOMAIN 146.190.29.129;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$DOMAIN\$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name $DOMAIN 146.190.29.129;
    
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    
    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files \$uri \$uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://backend:8080/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

echo "### Reloading Nginx ..."
docker compose exec frontend nginx -s reload

echo "### Setting up System Optimization (Cron Job) ..."
# Create a daily cron job to prune docker system and clear caches
cat > /etc/cron.daily/docker-prune <<EOF
#!/bin/bash
docker system prune -af --filter "until=24h"
sync; echo 1 > /proc/sys/vm/drop_caches
EOF

chmod +x /etc/cron.daily/docker-prune

echo "### Done! Nginx updated and optimization scheduled."
