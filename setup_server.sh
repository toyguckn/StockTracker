#!/bin/bash

# 1. Add Swap Space (Crucial for 1GB RAM)
echo "Setting up Swap..."
if [ ! -f /swapfile ]; then
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' | tee -a /etc/fstab
    echo "Swap setup complete."
else
    echo "Swap already exists."
fi

# 2. Adjust System Performance
sysctl vm.swappiness=10
echo "vm.swappiness=10" >> /etc/sysctl.conf

# 3. Install Docker & Docker Compose (if not present)
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

# 4. Firewall (UFW)
echo "Configuring Firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8080/tcp
ufw allow 8000/tcp # Scraper monitoring (optional)
ufw --force enable

echo "Server Setup Complete!"
