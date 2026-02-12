$ServerIP = "YOUR_SERVER_IP" # e.g. 146.190.29.129
$User = "root"

Write-Host "ZARA STOCK TRACKER - SİSTEM GÜNCELLENİYOR (V4 - FINAL)..." -ForegroundColor Cyan

# 1. Archive files 
Write-Host "1. Dosyalar paketleniyor..."
try {
    tar -czf zst_deploy.tar.gz --exclude="node_modules" --exclude="target" --exclude=".git" --exclude=".idea" backend scraper frontend docker-compose.yml setup_server.sh server_deploy.sh
}
catch {
    Write-Host "Hata: 'tar' komutu çalışmadı." -ForegroundColor Red
    exit
}

# 2. Upload Archive
Write-Host "2. Paket sunucuya gönderiliyor (Şifre isteyebilir)..."
scp zst_deploy.tar.gz ${User}@${ServerIP}:/root/

# 3. Setup & Run on Server (Single line command to avoid CRLF issues)
Write-Host "3. Sunucuda başlatılıyor..."
$RemoteCommand = "mkdir -p /root/zst; tar -xzf /root/zst_deploy.tar.gz -C /root/zst; rm /root/zst_deploy.tar.gz; cd /root/zst; tr -d '\r' < server_deploy.sh > deploy_clean.sh; chmod +x deploy_clean.sh; ./deploy_clean.sh"

ssh ${User}@${ServerIP} $RemoteCommand

# 4. Cleanup Local Archive
Remove-Item zst_deploy.tar.gz

Write-Host "---------------------------------------------------"
Write-Host "GÜNCELLEME TAMAMLANDI!" -ForegroundColor Green
Write-Host "Web Arayüzü: http://$ServerIP"
Write-Host "---------------------------------------------------"
