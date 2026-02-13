$ServerIP = "146.190.29.129"
$User = "root"

Write-Host "ZARA STOCK TRACKER - SYSTEM UPDATING (V4 - FINAL)..." -ForegroundColor Cyan

# 1. Archive files 
Write-Host "1. Packing files..."
try {
    tar -czf zst_deploy.tar.gz --exclude="node_modules" --exclude="target" --exclude=".git" --exclude=".idea" --exclude="certbot" --exclude="nginx_conf" backend scraper frontend docker-compose.yml setup_server.sh server_deploy.sh setup_ssl.sh fix_nginx_and_optimize.sh
}
catch {
    Write-Host "Error: 'tar' command failed." -ForegroundColor Red
    exit
}

# 2. Upload Archive
Write-Host "2. Sending package to server (May ask for password)..."
scp zst_deploy.tar.gz ${User}@${ServerIP}:/root/

# 3. Setup & Run on Server (Single line command to avoid CRLF issues)
Write-Host "3. Starting on server..."
$RemoteCommand = "mkdir -p /root/zst; tar -xzf /root/zst_deploy.tar.gz -C /root/zst; rm /root/zst_deploy.tar.gz; cd /root/zst; tr -d '\r' < server_deploy.sh > deploy_clean.sh; tr -d '\r' < setup_ssl.sh > ssl_clean.sh; tr -d '\r' < fix_nginx_and_optimize.sh > fix_clean.sh; chmod +x deploy_clean.sh ssl_clean.sh fix_clean.sh; ./deploy_clean.sh"

ssh ${User}@${ServerIP} $RemoteCommand

# 4. Cleanup Local Archive
Remove-Item zst_deploy.tar.gz

Write-Host "---------------------------------------------------"
Write-Host "UPDATE COMPLETE!" -ForegroundColor Green
Write-Host "Web Interface: http://$ServerIP"
Write-Host "---------------------------------------------------"
