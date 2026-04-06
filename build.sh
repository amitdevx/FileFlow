#!/bin/bash
# Render build and deployment script
# This initializes the database on first deployment

set -e

echo "📦 Installing dependencies..."
pip install -r FileFlow/backend/requirements.txt

echo "🗄️ Initializing database..."
cd FileFlow
python -c "
import os
os.environ['FLASK_ENV'] = 'production'
from backend.app import app, db

with app.app_context():
    db.create_all()
    print('✓ Database initialized successfully')
"

echo "✅ Build complete!"
