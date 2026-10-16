# Contract Analyzer Setup Script
# Run this script in PowerShell to set up the project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Contract Analyzer Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Check pip installation
Write-Host "Checking pip installation..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "Found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: pip is not installed" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv
if ($LASTEXITCODE -eq 0) {
    Write-Host "Virtual environment created successfully" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host ""
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "Requirements installed successfully" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to install requirements" -ForegroundColor Red
    exit 1
}

# Download spaCy model
Write-Host ""
Write-Host "Downloading spaCy language model..." -ForegroundColor Yellow
python -m spacy download en_core_web_sm
if ($LASTEXITCODE -eq 0) {
    Write-Host "spaCy model downloaded successfully" -ForegroundColor Green
} else {
    Write-Host "WARNING: spaCy model download failed. You may need to run this manually." -ForegroundColor Yellow
}

# Create necessary directories
Write-Host ""
Write-Host "Creating necessary directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
New-Item -ItemType Directory -Force -Path "data" | Out-Null
New-Item -ItemType Directory -Force -Path "outputs" | Out-Null
Write-Host "Directories created" -ForegroundColor Green

# Check .env file
Write-Host ""
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host ".env file found" -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT: Please edit the .env file and add your Anthropic API key" -ForegroundColor Cyan
    Write-Host "You can get an API key from: https://console.anthropic.com/" -ForegroundColor Cyan
} else {
    Write-Host "WARNING: .env file not found" -ForegroundColor Yellow
    Write-Host "You'll need to enter your API key in the application sidebar" -ForegroundColor Yellow
}

# Setup complete
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Add your Anthropic API key to the .env file" -ForegroundColor White
Write-Host "2. Run the application with: streamlit run app.py" -ForegroundColor White
Write-Host ""
Write-Host "For help, see README.md" -ForegroundColor Yellow
Write-Host ""