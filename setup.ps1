

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " NEU Virtual Assistant - Automated Setup Script" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

function Test-Command {
    param([string]$Command)
    try {
        $null = Get-Command $Command -ErrorAction Stop
        return $true
    }
    catch {
        return $false
    }
}

function Copy-EnvIfExampleExists {
    param([string]$ScopeName)

    if (-not (Test-Path ".env")) {
        if (Test-Path ".env.example") {
            Copy-Item ".env.example" ".env" -Force
            Write-Host "[OK] Created $ScopeName .env from .env.example" -ForegroundColor Green
        }
        else {
            Write-Host "[WARN] .env.example not found for $ScopeName. Skipping .env creation." -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "[OK] $ScopeName .env already exists" -ForegroundColor Green
    }
}

Write-Host "Checking prerequisites..." -ForegroundColor Yellow
$prereqsMet = $true

if (Test-Command "node") {
    Write-Host "[OK] Node.js: $(node --version)" -ForegroundColor Green
}
else {
    Write-Host "[ERR] Node.js is not installed." -ForegroundColor Red
    $prereqsMet = $false
}

if (Test-Command "npm") {
    Write-Host "[OK] npm: $(npm --version)" -ForegroundColor Green
}
else {
    Write-Host "[ERR] npm is not installed." -ForegroundColor Red
    $prereqsMet = $false
}

if (Test-Command "python") {
    Write-Host "[OK] Python: $(python --version)" -ForegroundColor Green
}
else {
    Write-Host "[ERR] Python is not installed." -ForegroundColor Red
    $prereqsMet = $false
}

if (-not $prereqsMet) {
    Write-Host "Install missing prerequisites and run this script again." -ForegroundColor Red
    exit 1
}

$root = $PSScriptRoot

Write-Host ""
Write-Host "Setting up backend..." -ForegroundColor Cyan
Set-Location (Join-Path $root "backend")

if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}
else {
    Write-Host "[OK] Virtual environment already exists" -ForegroundColor Green
}

$venvPython = Join-Path $PWD "venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "[ERR] Could not find venv Python at $venvPython" -ForegroundColor Red
    exit 1
}

Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt

Copy-EnvIfExampleExists -ScopeName "backend"

if (-not (Test-Path "uploads")) {
    New-Item -ItemType Directory -Path "uploads" | Out-Null
    Write-Host "[OK] Created backend/uploads" -ForegroundColor Green
}

Write-Host ""
Write-Host "Setting up frontend..." -ForegroundColor Cyan
Set-Location (Join-Path $root "frontend")

Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
npm install

Copy-EnvIfExampleExists -ScopeName "frontend"

Set-Location $root

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host " Setup complete" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Run backend manually (same terminal):" -ForegroundColor White
Write-Host "  cd backend" -ForegroundColor Gray
Write-Host "  .\run.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "Run frontend manually (second terminal):" -ForegroundColor White
Write-Host "  cd frontend" -ForegroundColor Gray
Write-Host "  npm run start" -ForegroundColor Gray
Write-Host ""
