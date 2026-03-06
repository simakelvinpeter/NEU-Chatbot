[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Set-Location -Path $PSScriptRoot

Write-Host "Starting NEU Chatbot backend..." -ForegroundColor Green

$venvPython = Join-Path $PSScriptRoot "venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow

    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 -m venv venv
    }
    elseif (Get-Command python -ErrorAction SilentlyContinue) {
        & python -m venv venv
    }
    else {
        Write-Host "Python was not found. Install Python 3.10+ and retry." -ForegroundColor Red
        exit 1
    }
}

$venvPython = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "Virtual environment was not created correctly." -ForegroundColor Red
    exit 1
}

$pipHealthy = $true
& $venvPython -m pip --version | Out-Null
if ($LASTEXITCODE -ne 0) {
    $pipHealthy = $false
}

if (-not $pipHealthy) {
    Write-Host "Detected broken pip in venv. Recreating virtual environment..." -ForegroundColor Yellow
    if (Test-Path "venv") {
        Remove-Item -Path "venv" -Recurse -Force
    }

    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 -m venv venv
    }
    elseif (Get-Command python -ErrorAction SilentlyContinue) {
        & python -m venv venv
    }

    $venvPython = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        Write-Host "Virtual environment recreation failed." -ForegroundColor Red
        exit 1
    }
}

Write-Host "Upgrading pip..." -ForegroundColor Yellow
& $venvPython -m pip install --upgrade pip | Out-Null

$pyMinor = (& $venvPython -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')").Trim()

Write-Host "Installing dependencies..." -ForegroundColor Yellow
& $venvPython -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    if ($pyMinor -eq "3.14") {
        Write-Host "Pinned requirements failed on Python 3.14. Installing compatible latest packages..." -ForegroundColor Yellow
        & $venvPython -m pip install fastapi "uvicorn[standard]" pydantic pydantic-settings python-dotenv python-multipart aiofiles beautifulsoup4 requests lxml openai
    }
    else {
        Write-Host "Dependency installation failed. Check requirements.txt and Python version." -ForegroundColor Red
        exit 1
    }
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "Dependency installation failed." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path ".env")) {
    Set-Content ".env" "CORS_ORIGINS=[""http://localhost:5173"",""http://localhost:3000"",""http://127.0.0.1:5173""]"
    Write-Host "Created .env with default CORS_ORIGINS" -ForegroundColor Yellow
}

if (Test-Path ".env") {
    $envText = Get-Content ".env" -Raw
    $corsMatch = [regex]::Match($envText, "(?m)^CORS_ORIGINS\s*=\s*(.+)$")

    if ($corsMatch.Success) {
        $rawCors = $corsMatch.Groups[1].Value.Trim()

        if (-not ($rawCors.StartsWith("[") -and $rawCors.EndsWith("]"))) {
            $corsItems = $rawCors.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
            if ($corsItems.Count -gt 0) {
                $jsonCors = "[" + (($corsItems | ForEach-Object { '"' + $_.Replace('"', '\"') + '"' }) -join ",") + "]"
                $envText = [regex]::Replace($envText, "(?m)^CORS_ORIGINS\s*=\s*.+$", "CORS_ORIGINS=$jsonCors")
                Set-Content ".env" $envText -NoNewline
                Write-Host "Normalized CORS_ORIGINS in .env to JSON array format" -ForegroundColor Yellow
            }
        }
    }
}

if (-not (Test-Path "uploads")) {
    New-Item -ItemType Directory -Path "uploads" | Out-Null
}

if (-not $env:OPENAI_API_KEY) {
    Write-Host "OPENAI_API_KEY not found in current shell. Scraping/FAQ features still work; AI fallback will be disabled until key is set." -ForegroundColor Yellow
}

Write-Host "Starting FastAPI server..." -ForegroundColor Green
& $venvPython app.py
