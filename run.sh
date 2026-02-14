#!/bin/bash

# BENYAMIN BATAU JOURNAL APP - Run Script

echo "=========================================="
echo "  BENYAMIN BATAU JOURNAL APP"
echo "  Version 1.0.0"
echo "=========================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install/update dependencies
echo ""
echo "Installing/updating dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p uploads outputs static/js static/css templates utils
echo "✓ Directories created"

# Check .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠ WARNING: .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "IMPORTANT: Please edit .env file and add your API keys!"
    echo ""
fi

# Run the application
echo ""
echo "=========================================="
echo "  Starting BENYAMIN BATAU JOURNAL APP"
echo "=========================================="
echo ""
echo "Server will run on: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

# Run Flask app
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py
