#!/bin/bash
# Start script for FileFlow FastAPI backend

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run with uvicorn
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
