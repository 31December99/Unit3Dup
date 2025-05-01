@echo off
setlocal

:: Run "docker build -t unit3dup ." inside the Docker folder first
:: run this script

:: Fixed path to Unit3Dbot.json on the host (edit if needed)
set "HOST_PATH=C:\Users\PC\AppData\Local\Unit3Dup_config\Unit3Dbot.json"

:: Fixed path inside the container
set "GUEST_PATH=/root/Unit3Dup_config/Unit3Dbot.json"

:: Check if the JSON file exists
if not exist "%HOST_PATH%" (
    echo Error: The JSON config file does not exist
    echo   %HOST_PATH%
    pause
    exit /b 1
)

:: Run Test
docker run --rm -v "%HOST_PATH%:%GUEST_PATH%" unit3dup --help