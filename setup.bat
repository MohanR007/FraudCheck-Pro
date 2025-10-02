@echo off
echo ========================================
echo FraudCheck Web - Setup Script
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)
echo Python found!

echo.
echo [2/4] Installing Python dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!

echo.
echo [3/4] Creating pretrained fraud detection model...
cd ..\models
python create_model.py
if errorlevel 1 (
    echo ERROR: Failed to create model
    pause
    exit /b 1
)
echo Model created successfully!

echo.
echo [4/4] Setup complete!
echo ========================================
echo.
echo To start the application, run: run.bat
echo Or manually: cd backend && python app.py
echo Then open: http://localhost:5000
echo.
echo ========================================
pause