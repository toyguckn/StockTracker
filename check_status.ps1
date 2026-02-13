$ServerIP = "146.190.29.129"
$User = "root"

Write-Host "Checking Server Status on $ServerIP..." -ForegroundColor Cyan

$RemoteCommand = "echo '--- FREE MEMORY ---'; free -h; echo ''; echo '--- DISK SPACE ---'; df -h; echo ''; echo '--- CONTAINER STATUS ---'; docker ps -a; echo ''; echo '--- BACKEND LOGS ---'; docker logs --tail 20 zst-backend 2>&1 || echo 'No backend logs'; echo ''; echo '--- FRONTEND LOGS ---'; docker logs --tail 20 zst-frontend 2>&1 || echo 'No frontend logs'"

ssh ${User}@${ServerIP} $RemoteCommand
