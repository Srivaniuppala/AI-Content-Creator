@echo off
REM AI Content Creator - Quick Start Script
REM Run this script to set up and start the application

color 0B
echo ========================================
echo   AI Content Creator - Quick Start
echo ========================================
echo.

REM Check if Docker is installed
echo [1/4] Checking Docker installation...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Docker is not installed or not running!
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/
    color 07
    pause
    exit /b 1
)
color 0A
echo [OK] Docker found
docker --version
color 07

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Docker Compose is not available!
    color 07
    pause
    exit /b 1
)
color 0A
echo [OK] Docker Compose found
docker-compose --version
color 07

echo.

REM Check if .env file exists
echo [2/4] Checking configuration...
if not exist ".env" (
    color 0E
    echo [INFO] .env file not found!
    echo Creating .env from template...
    copy ".env.example" ".env" >nul
    color 0A
    echo [OK] .env file created
    color 0E
    echo.
    echo [IMPORTANT] Please edit .env and add your Groq API key:
    echo   GROQ_API_KEY=your_api_key_here
    echo.
    echo Get your free API key at: https://console.groq.com
    echo.
    color 07
    pause
)

REM Check if API key is configured
findstr /C:"GROQ_API_KEY=gsk_" ".env" >nul 2>&1
if %errorlevel% neq 0 (
    color 0E
    echo [WARNING] Groq API key may not be configured in .env
    echo The application may not work without a valid API key.
    echo.
    color 07
)

color 0A
echo [OK] Configuration ready
color 07
echo.

REM Stop any existing containers
echo [3/4] Cleaning up old containers...
docker-compose down >nul 2>&1
color 0A
echo [OK] Cleanup complete
color 07

echo.

REM Start services
echo [4/4] Starting services...
echo    - PostgreSQL Database
echo    - Streamlit Application
echo.

docker-compose up -d

if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Failed to start services
    echo Check logs with: docker-compose logs
    color 07
    pause
    exit /b 1
)

color 0A
echo [OK] Services started successfully
color 07

echo.

REM Wait for services to be ready
echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul

color 0A
echo [OK] Services should be ready
color 0B
echo.
echo ========================================
echo   Setup Complete!
echo ========================================
color 07
echo.
echo Application is running at:
color 0B
echo   http://localhost:8501
color 07
echo.
echo Services:
echo   - Streamlit App:  http://localhost:8501
echo   - PostgreSQL:     localhost:5432
echo.
echo Useful commands:
echo   - View logs:      docker-compose logs -f
echo   - Stop services:  docker-compose down
echo   - Restart:        docker-compose restart
echo.
echo Opening browser...
timeout /t 2 /nobreak >nul

REM Try to open browser
start http://localhost:8501

echo.
color 0A
echo Happy creating!
color 07
echo.
pause
