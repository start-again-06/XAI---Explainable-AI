@echo off
setlocal
echo 🚀 Starting XAI-IDS Unified Application...

REM Build frontend
echo 📦 Building frontend...
cd frontend
if errorlevel 1 (
    echo ❌ Frontend directory not found
    exit /b 1
)
call npm install
if errorlevel 1 (
    echo ❌ Failed to install frontend dependencies
    exit /b 1
)
call npm run build
if errorlevel 1 (
    echo ❌ Failed to build frontend
    exit /b 1
)

REM Start backend (which now serves the frontend)
echo 🔧 Starting backend server (includes frontend)...
cd ..\backend
if errorlevel 1 (
    echo ❌ Backend directory not found
    exit /b 1
)

REM Use virtual environment executables if they exist
set "PYTHON_EXE=python"
set "PIP_EXE=pip"
if exist venv\Scripts\python.exe if exist venv\Scripts\pip.exe (
    set "PYTHON_EXE=venv\Scripts\python.exe"
    set "PIP_EXE=venv\Scripts\pip.exe"
    echo ✅ Virtual environment activated
)

REM Install dependencies
call "%PIP_EXE%" install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install backend dependencies
    exit /b 1
)

REM Start the unified application
echo 🌟 Starting XAI-IDS on http://localhost:8000
call "%PYTHON_EXE%" main.py
if errorlevel 1 (
    echo ❌ Application failed to start
    exit /b 1
)

pause
endlocal
