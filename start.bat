@echo off
cd /d "%~dp0"

echo Starting Text Toolbox...
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker is not installed. Please install Docker first
    pause
    exit /b 1
)

REM Start services
docker-compose up -d

echo.
echo Services started successfully!
echo.
echo Frontend: http://localhost:8080
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo View logs: docker-compose logs -f
echo Stop services: docker-compose down
echo.
pause
