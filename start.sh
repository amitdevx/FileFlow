#!/bin/bash

# FileFlow - Quick Start Script

echo "🚀 Starting FileFlow..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.12 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd "$SCRIPT_DIR/FileFlow/backend"
pip install -r ../requirements.txt

# Initialize database
echo "🗄️  Initializing database..."
export FLASK_APP=app.py
flask init-db

# Start backend server in background
echo "🐍 Starting backend server..."
flask run &
BACKEND_PID=$!

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd "$SCRIPT_DIR/FileFlow/frontend"
npm install

# Start frontend development server
echo "⚛️  Starting frontend server..."
npm start &
FRONTEND_PID=$!

echo "✅ FileFlow is running!"
echo "🌐 Backend: http://localhost:5000"
echo "🌐 Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers"

# Trap Ctrl+C and kill both processes
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

# Wait for processes
wait
