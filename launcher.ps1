# OptiWindows PowerShell Launcher
# Lance l'application avec les droits administrateur

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "        OptiWindows Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Fonction pour vérifier les droits administrateur
function Test-Administrator {
    $user = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($user)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Vérification des droits admin
if (-not (Test-Administrator)) {
    Write-Host "[!] Droits administrateur requis" -ForegroundColor Yellow
    Write-Host "    Relancement avec elevation..." -ForegroundColor Yellow
    Write-Host ""
    
    # Relance le script avec élévation
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

Write-Host "[OK] Droits administrateur detectes" -ForegroundColor Green
Write-Host ""

# Vérification de Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python detecte: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERREUR] Python n'est pas installe" -ForegroundColor Red
    Write-Host ""
    Write-Host "Veuillez installer Python depuis:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "N'oubliez pas de cocher 'Add Python to PATH'" -ForegroundColor Yellow
    pause
    exit 1
}

# Changement de répertoire vers le script
Set-Location $PSScriptRoot

# Vérification requirements.txt
if (-not (Test-Path "requirements.txt")) {
    Write-Host "[ERREUR] requirements.txt introuvable" -ForegroundColor Red
    pause
    exit 1
}

# Installation des dépendances
Write-Host ""
Write-Host "Verification des dependances..." -ForegroundColor Cyan
try {
    python -m pip install -q -r requirements.txt
    Write-Host "[OK] Dependances installees" -ForegroundColor Green
} catch {
    Write-Host "[!] Tentative d'installation avec upgrade..." -ForegroundColor Yellow
    python -m pip install --upgrade -r requirements.txt
}

# Lancement de l'application
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Lancement d'OptiWindows..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    python main.py
} catch {
    Write-Host ""
    Write-Host "[ERREUR] L'application s'est terminee avec une erreur" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    pause
}
