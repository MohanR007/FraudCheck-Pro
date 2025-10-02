@echo off
echo ==========================================
echo FraudCheck Pro - Enhanced Application
echo ==========================================
echo.

echo Checking if enhanced model exists...
if not exist "models\fraud_detection_model.pkl" (
    echo Enhanced model not found! Creating advanced model...
    echo.
    cd models
    python create_enhanced_model.py
    if errorlevel 1 (
        echo Enhanced model creation failed! Trying basic model...
        python create_model.py
        if errorlevel 1 (
            echo Model creation failed! Please check the errors above.
            pause
            exit /b 1
        )
    )
    cd ..
    echo.
    echo Model created successfully!
    echo.
)

echo Starting Enhanced Flask server...
echo.
echo ==========================================
echo   Enhanced FraudCheck Pro Features:
echo ==========================================
echo   ✓ Advanced fraud detection with 13+ features
echo   ✓ Interactive dashboard with charts
echo   ✓ Transaction history tracking
echo   ✓ Comprehensive analytics
echo   ✓ Real-time statistics
echo   ✓ Enhanced API documentation
echo   ✓ Multi-page navigation
echo   ✓ Risk assessment with reasoning
echo ==========================================
echo.
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

cd backend
python enhanced_app.py