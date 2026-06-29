#!/usr/bin/env powershell
# 🚀 QUICK START CHECKLIST
# Run this to verify your setup is ready

Write-Host "🩺 Diabetes Risk Prediction Dashboard - Verification Checklist" -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Green
Write-Host ""

$checks_passed = 0
$checks_total = 0

# Helper function
function Check-Status {
    param([string]$Name, [bool]$Pass)
    $checks_total++
    if ($Pass) {
        $checks_passed++
        Write-Host "✅ $Name" -ForegroundColor Green
    } else {
        Write-Host "❌ $Name" -ForegroundColor Red
    }
}

# Check 1: Python Version
Write-Host "1️⃣  PYTHON CHECK" -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
$pythonCheck = $pythonVersion -match "3\.[8-9]|3\.1[0-9]"
Check-Status "Python 3.8+ installed" $pythonCheck
Write-Host "   Version: $pythonVersion" -ForegroundColor Gray
Write-Host ""

# Check 2: Current Directory
Write-Host "2️⃣  DIRECTORY CHECK" -ForegroundColor Yellow
$projectPath = "d:\MLC CLASS PROJECT 2"
$pathExists = Test-Path $projectPath
Check-Status "Project directory exists: $projectPath" $pathExists
$currentDir = Get-Location
Write-Host "   Current location: $currentDir" -ForegroundColor Gray
Write-Host ""

# Check 3: Key Files
Write-Host "3️⃣  FILES CHECK" -ForegroundColor Yellow
$appPyExists = Test-Path "$projectPath\app.py"
Check-Status "app.py exists" $appPyExists

$reqExists = Test-Path "$projectPath\requirements.txt"
Check-Status "requirements.txt exists" $reqExists

$modelExists = Test-Path "$projectPath\models\diabetes_model.pkl"
Check-Status "diabetes_model.pkl exists" $modelExists

$scalerExists = Test-Path "$projectPath\models\scaler.pkl"
Check-Status "scaler.pkl exists" $scalerExists
Write-Host ""

# Check 4: Python Packages
Write-Host "4️⃣  PACKAGES CHECK" -ForegroundColor Yellow
$streamlitCheck = python -c "import streamlit; print('OK')" 2>&1
$hasStreamlit = $streamlitCheck -eq "OK"
Check-Status "Streamlit installed" $hasStreamlit

$sklearnCheck = python -c "import sklearn; print('OK')" 2>&1
$hasScikit = $sklearnCheck -eq "OK"
Check-Status "scikit-learn installed" $hasScikit

$pandasCheck = python -c "import pandas; print('OK')" 2>&1
$hasPandas = $pandasCheck -eq "OK"
Check-Status "pandas installed" $hasPandas

$numpyCheck = python -c "import numpy; print('OK')" 2>&1
$hasNumpy = $numpyCheck -eq "OK"
Check-Status "numpy installed" $hasNumpy

$mplCheck = python -c "import matplotlib; print('OK')" 2>&1
$hasMpl = $mplCheck -eq "OK"
Check-Status "matplotlib installed" $hasMpl
Write-Host ""

# Check 5: Model Loading
Write-Host "5️⃣  MODEL LOADING CHECK" -ForegroundColor Yellow
$modelLoadCheck = python -c "
import pickle
try:
    with open('$projectPath\models\diabetes_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print('OK')
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1

$modelLoads = $modelLoadCheck -eq "OK"
Check-Status "SVM model loads successfully" $modelLoads

$scalerLoadCheck = python -c "
import pickle
try:
    with open('$projectPath\models\scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print('OK')
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1

$scalerLoads = $scalerLoadCheck -eq "OK"
Check-Status "Scaler loads successfully" $scalerLoads
Write-Host ""

# Summary
Write-Host "=================================================================" -ForegroundColor Green
Write-Host "SUMMARY" -ForegroundColor Yellow
Write-Host "Checks Passed: $checks_passed / $checks_total" -ForegroundColor Green
Write-Host ""

if ($checks_passed -eq $checks_total) {
    Write-Host "🎉 ALL CHECKS PASSED! You're ready to go!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next step:" -ForegroundColor Yellow
    Write-Host "  cd `"d:\MLC CLASS PROJECT 2`"" -ForegroundColor Cyan
    Write-Host "  streamlit run app.py" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Your dashboard will open at: http://localhost:8501" -ForegroundColor Green
} else {
    $failed = $checks_total - $checks_passed
    Write-Host "⚠️  $failed CHECK(S) FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please fix the issues above before running the app." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Common fixes:" -ForegroundColor Yellow
    Write-Host "1. Install dependencies: pip install -r requirements.txt" -ForegroundColor Cyan
    Write-Host "2. Check model files: Run main.ipynb to regenerate them" -ForegroundColor Cyan
    Write-Host "3. Check working directory: Should be d:\MLC CLASS PROJECT 2" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "For help, see: DEPLOYMENT_GUIDE.md or README.md" -ForegroundColor Gray
