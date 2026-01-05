# AI Content Creator - Quick Start Script
# Run this script to set up and start the application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI Content Creator - Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "[1/4] Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "[OK] Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Docker is not installed or not running!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/" -ForegroundColor Red
    exit 1
}

# Check if docker-compose is available
try {
    $composeVersion = docker-compose --version
    Write-Host "[OK] Docker Compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Docker Compose is not available!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Check if .env file exists
Write-Host "[2/4] Checking configuration..." -ForegroundColor Yellow
if (-Not (Test-Path ".env")) {
    Write-Host "[INFO] .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "[OK] .env file created" -ForegroundColor Green
    Write-Host ""
    Write-Host "[IMPORTANT] Please edit .env and add your Groq API key:" -ForegroundColor Yellow
    Write-Host "  GROQ_API_KEY=your_api_key_here" -ForegroundColor White
    Write-Host ""
    Write-Host "Get your free API key at: https://console.groq.com" -ForegroundColor Cyan
    Write-Host ""
    $continue = Read-Host "Press Enter after adding your API key to .env, or type 'exit' to quit"
    if ($continue -eq "exit") {
        exit 0
    }
}

# Check if API key is configured
$envContent = Get-Content ".env" -Raw
if ($envContent -notmatch "GROQ_API_KEY=gsk_" -and $envContent -notmatch "GROQ_API_KEY=.{30,}") {
    Write-Host "[WARNING] Groq API key may not be configured in .env" -ForegroundColor Yellow
    Write-Host "The application may not work without a valid API key." -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "[OK] Configuration ready" -ForegroundColor Green
Write-Host ""

# Stop any existing containers
Write-Host "[3/4] Cleaning up old containers..." -ForegroundColor Yellow
docker-compose down 2>$null
Write-Host "[OK] Cleanup complete" -ForegroundColor Green

Write-Host ""

# Start services
Write-Host "[4/4] Starting services..." -ForegroundColor Yellow
Write-Host "   - PostgreSQL Database" -ForegroundColor Cyan
Write-Host "   - Streamlit Application" -ForegroundColor Cyan
Write-Host ""

docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Services started successfully" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to start services" -ForegroundColor Red
    Write-Host "Check logs with: docker-compose logs" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Wait for services to be ready
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

$maxRetries = 30
$retry = 0
$allHealthy = $false

while (($retry -lt $maxRetries) -and (-not $allHealthy)) {
    try {
        $status = docker-compose ps --format json | ConvertFrom-Json
        if ($status) {
            $unhealthy = $status | Where-Object { $_.State -ne "running" }
            
            if ($null -eq $unhealthy -or $unhealthy.Count -eq 0) {
                $allHealthy = $true
            } else {
                $retry++
                Write-Host "   Waiting for services... ($retry/$maxRetries)" -ForegroundColor Gray
                Start-Sleep -Seconds 2
            }
        } else {
            $retry++
            Write-Host "   Waiting for services... ($retry/$maxRetries)" -ForegroundColor Gray
            Start-Sleep -Seconds 2
        }
    } catch {
        $retry++
        Write-Host "   Waiting for services... ($retry/$maxRetries)" -ForegroundColor Gray
        Start-Sleep -Seconds 2
    }
}

if ($allHealthy) {
    Write-Host "[OK] All services are healthy" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Services started but may not be fully ready" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Application is running at:" -ForegroundColor Cyan
Write-Host "  http://localhost:8501" -ForegroundColor White -BackgroundColor DarkBlue
Write-Host ""
Write-Host "Services:" -ForegroundColor Cyan
Write-Host "  - Streamlit App:  http://localhost:8501" -ForegroundColor Gray
Write-Host "  - PostgreSQL:     localhost:5432" -ForegroundColor Gray
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Cyan
Write-Host "  - View logs:      docker-compose logs -f" -ForegroundColor Gray
Write-Host "  - Stop services:  docker-compose down" -ForegroundColor Gray
Write-Host "  - Restart:        docker-compose restart" -ForegroundColor Gray
Write-Host ""
Write-Host "Opening browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

# Try to open browser
try {
    Start-Process "http://localhost:8501"
} catch {
    Write-Host "Could not open browser automatically." -ForegroundColor Yellow
    Write-Host "Please open http://localhost:8501 manually." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Happy creating!" -ForegroundColor Green
Write-Host ""
