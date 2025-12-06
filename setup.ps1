# NEU Virtual Assistant - Complete Setup Script for Windows
# This script automates the entire setup process

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     NEU Virtual Assistant - Automated Setup Script        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Continue"

# Function to check if a command exists
function Test-Command {
    param($command)
    try {
        if (Get-Command $command -ErrorAction Stop) {
            return $true
        }
    }
    catch {
        return $false
    }
}

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow
Write-Host ""

$prereqsMet = $true

# Check Node.js
if (Test-Command "node") {
    $nodeVersion = node --version
    Write-Host "✅ Node.js is installed: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js is NOT installed" -ForegroundColor Red
    Write-Host "   Please install Node.js 16+ from https://nodejs.org/" -ForegroundColor Yellow
    $prereqsMet = $false
}

# Check npm
if (Test-Command "npm") {
    $npmVersion = npm --version
    Write-Host "✅ npm is installed: v$npmVersion" -ForegroundColor Green
} else {
    Write-Host "❌ npm is NOT installed" -ForegroundColor Red
    $prereqsMet = $false
}

# Check Python
if (Test-Command "python") {
    $pythonVersion = python --version
    Write-Host "✅ Python is installed: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python is NOT installed" -ForegroundColor Red
    Write-Host "   Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Yellow
    $prereqsMet = $false
}

# Check pip
if (Test-Command "pip") {
    $pipVersion = pip --version
    Write-Host "✅ pip is installed" -ForegroundColor Green
} else {
    Write-Host "❌ pip is NOT installed" -ForegroundColor Red
    $prereqsMet = $false
}

Write-Host ""

if (-not $prereqsMet) {
    Write-Host "❌ Prerequisites not met. Please install the required software and try again." -ForegroundColor Red
    exit 1
}

Write-Host "✅ All prerequisites met!" -ForegroundColor Green
Write-Host ""

# Setup Backend
Write-Host "📦 Setting up Backend..." -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan

Set-Location "backend"

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "🔧 Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment and install dependencies
Write-Host "📥 Installing Python dependencies..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
pip install -r requirements.txt --quiet
Write-Host "✅ Python dependencies installed" -ForegroundColor Green

# Create .env file
if (-not (Test-Path ".env")) {
    Write-Host "⚙️ Creating backend .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Backend .env file created" -ForegroundColor Green
} else {
    Write-Host "✅ Backend .env file already exists" -ForegroundColor Green
}

# Create uploads directory
if (-not (Test-Path "uploads")) {
    New-Item -ItemType Directory -Path "uploads" | Out-Null
    Write-Host "✅ Uploads directory created" -ForegroundColor Green
}

Set-Location ".."
Write-Host ""

# Setup Frontend
Write-Host "📦 Setting up Frontend..." -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan

Set-Location "frontend"

# Install dependencies
Write-Host "📥 Installing npm dependencies (this may take a few minutes)..." -ForegroundColor Yellow
npm install --silent
Write-Host "✅ npm dependencies installed" -ForegroundColor Green

# Create .env file
if (-not (Test-Path ".env")) {
    Write-Host "⚙️ Creating frontend .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Frontend .env file created" -ForegroundColor Green
} else {
    Write-Host "✅ Frontend .env file already exists" -ForegroundColor Green
}

Set-Location ".."
Write-Host ""

# Summary
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    Setup Complete! 🎉                      ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start the backend server:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "2. In a NEW terminal, start the frontend:" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Open your browser and visit:" -ForegroundColor White
Write-Host "   Frontend: http://localhost:5173" -ForegroundColor Gray
Write-Host "   Backend API: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 For more information, see:" -ForegroundColor Cyan
Write-Host "   - QUICKSTART.md for quick start guide" -ForegroundColor Gray
Write-Host "   - README.md for full documentation" -ForegroundColor Gray
Write-Host "   - backend/README.md for backend details" -ForegroundColor Gray
Write-Host "   - frontend/README.md for frontend details" -ForegroundColor Gray
Write-Host ""
