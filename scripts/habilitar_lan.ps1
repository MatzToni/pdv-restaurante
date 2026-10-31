# Script para habilitar acceso en Red Local (LAN) a tablets, iPad y comanderos móviles
# Requiere ejecutarse como Administrador en Windows

$ErrorActionPreference = "SilentlyContinue"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Configurador de Red Local - Eden Cafe PDV (WSL2)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Obtener la IP actual de WSL2 dinámicamente
try {
    $wslIp = (wsl hostname -I).Trim().Split(" ")[0]
} catch {
    $wslIp = "172.17.253.112"
}

if (-not $wslIp) {
    $wslIp = "172.17.253.112"
}

Write-Host "[INFO] IP interna de WSL2 detectada: $wslIp" -ForegroundColor Yellow

# 2. Configurar portproxy para Frontend (5173) y Backend (8000)
Write-Host "[INFO] Configurando reenvio de puertos 5173 y 8000 hacia WSL2..." -ForegroundColor Yellow
netsh interface portproxy delete v4tov4 listenport=5173 listenaddress=0.0.0.0 *>$null
netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=0.0.0.0 *>$null

netsh interface portproxy add v4tov4 listenport=5173 listenaddress=0.0.0.0 connectport=5173 connectaddress=$wslIp
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=$wslIp

# 3. Regla en el Firewall de Windows
Write-Host "[INFO] Configurando reglas de entrada en Firewall de Windows..." -ForegroundColor Yellow
netsh advfirewall firewall delete rule name="PDV Eden Cafe" *>$null
netsh advfirewall firewall add rule name="PDV Eden Cafe" dir=in action=allow protocol=TCP localport=5173,8000 *>$null

# 4. Obtener la IP local física de la computadora (Ethernet o Wi-Fi)
$lanIp = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { 
    $_.InterfaceAlias -notmatch "vEthernet|WSL|Loopback" -and 
    $_.IPAddress -notmatch "^127\.|^169\.254\." 
} | Select-Object -ExpandProperty IPAddress -First 1)

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  CONFIGURACION EXITOSA" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Desde tu iPad, tablet o celular conectado al mismo Wi-Fi:"
if ($lanIp) {
    Write-Host "👉 Abre Safari / Chrome en: http://${lanIp}:5173" -ForegroundColor Cyan
} else {
    Write-Host "👉 Abre Safari / Chrome en: http://<IP_LOCAL>:5173" -ForegroundColor Cyan
}
Write-Host ""
Write-Host "Cuentas de prueba para ingresar:"
Write-Host "  * Carlos Lopez (Mesero):  PIN 7777"
Write-Host "  * Ana Gomez (Mesera):    PIN 5556"
Write-Host "  * Cocina KDS:            PIN 4444"
Write-Host "  * Caja / Cobros:         PIN 1111 o 2222"
Write-Host "==========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona cualquier tecla para cerrar esta ventana..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
