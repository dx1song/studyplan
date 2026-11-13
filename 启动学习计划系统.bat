@echo off
title AI Study Plan System
cd /d "%~dp0backend"

set "PY=python"
where python >nul 2>nul || set "PY=py"

%PY% -c "import openai, pandas, openpyxl, fastapi, uvicorn, dotenv" >nul 2>nul
if errorlevel 1 (
    echo [First run] Installing backend dependencies, please wait...
    %PY% -m pip install -r requirements.txt
)

echo ==============================================
echo   AI Study Plan System
echo   URL: http://localhost:8000
echo   If browser does not open, visit the URL above.
echo   Press Ctrl+C to stop.
echo ==============================================
%PY% launcher.py

echo.
echo Server stopped. You can close this window now.
pause
