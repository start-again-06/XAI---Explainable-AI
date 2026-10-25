#!/bin/bash
set -euo pipefail

# XAI-IDS Unified Startup Script
echo "🚀 Starting XAI-IDS Unified Application..."

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm install
npm run build

# Start backend (which now serves the frontend)
echo "🔧 Starting backend server (includes frontend)..."
cd ../backend

# Use virtual environment executables if present
PYTHON_BIN="python"
PIP_BIN="pip"
if [ -x "venv/bin/python" ] && [ -x "venv/bin/pip" ]; then
    PYTHON_BIN="./venv/bin/python"
    PIP_BIN="./venv/bin/pip"
    echo "✅ Virtual environment activated"
fi

# Install dependencies
"$PIP_BIN" install -r requirements.txt

# Start the unified application
echo "🌟 Starting XAI-IDS on http://localhost:8000"
"$PYTHON_BIN" main.py
