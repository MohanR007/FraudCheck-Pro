@echo off
echo ========================================
echo FraudCheck Web - Starting Application
echo ========================================
echo.

echo Checking if model exists...
if not exist "models\fraud_detection_model.pkl" (
    echo Model not found! Running setup first...
    call setup.bat
    if errorlevel 1 (
        echo Setup failed! Please check the errors above.
        pause
        exit /b 1
    )
)

echo.
echo Starting Flask server...
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

cd backend
python app.py
