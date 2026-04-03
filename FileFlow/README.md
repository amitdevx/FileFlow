# FileFlow - Google Drive Clone

A full-stack file management application with Flask/FastAPI backend and React frontend.

## Quick Start

### One-Command Startup
```bash
./start.sh
```

This will automatically:
- ✅ Create Python virtual environment
- ✅ Install all dependencies (backend + frontend)
- ✅ Initialize the database
- ✅ Start Flask backend on port 5000
- ✅ Start React frontend on port 3000

Then open **http://localhost:3000** in your browser!

### Use FastAPI Backend (Optional)
```bash
./start.sh --fastapi
```

### Stop Servers
Press `Ctrl+C` in the terminal running start.sh

## Features

### ✨ Working Buttons
- **Upload** - Upload files to current folder
- **New Folder** - Create new folders
- **Rename** - Rename files/folders (also F2 key)
- **Delete** - Delete selected items (also Delete key)
- **Download** - Download files
- **Back/Forward** - Navigate history
- **View Modes** - List, Grid, Details

### 🎯 User Interactions
- **Double-click folder** - Navigate into folder
- **Double-click file** - View/open file
- **Right-click** - Context menu (Open, Download, Copy, Cut, Rename, Delete)
- **Ctrl/Cmd+Click** - Multi-select files
- **Breadcrumb navigation** - Click to jump to any parent folder

### ⌨️ Keyboard Shortcuts
- `Ctrl/Cmd+A` - Select all files
- `Delete` - Delete selected files
- `F2` - Rename selected file
- `Esc` - Clear selection / Close dialogs

## Tech Stack

### Backend
- **Flask** - Python web framework (default)
- **FastAPI** - Modern async Python framework (optional)
- **SQLAlchemy** - Database ORM
- **Flask-Login** - User authentication
- **SQLite** - Database

### Frontend
- **React** - UI framework
- **Axios** - HTTP client
- **CSS Variables** - Theme support (dark/light)

## Project Structure

```
FileFlow/
├── backend/              # Flask backend
│   ├── api/             # API routes
│   ├── models/          # Database models
│   ├── services/        # Business logic
│   ├── venv/            # Python virtual environment (auto-created)
│   └── requirements.txt # Python dependencies
├── backend_fastapi/     # FastAPI backend (alternative)
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── context/     # State management
│   │   └── App.js       # Main app
│   ├── package.json     # npm dependencies
│   └── node_modules/    # npm packages (auto-created)
├── user_files/          # User uploaded files
├── start.sh             # Startup script
└── README.md            # This file
```

## API Endpoints

### Authentication
- `POST /signup` - Register new user
- `POST /login` - Login
- `POST /logout` - Logout
- `GET /dashboard` - Main file manager page

### File Operations
- `GET /api/files` - List files (optional ?folder_id=<id>)
- `POST /upload` - Upload file
- `DELETE /delete_file/<id>` - Delete file/folder
- `POST /rename_file/<id>` - Rename file/folder
- `POST /move_file/<id>` - Move file/folder
- `GET /download_file/<id>` - Download file
- `GET /view_file/<id>` - View file

### Folder Operations
- `POST /create_folder` - Create new folder
- `GET /api/breadcrumbs/<id>` - Get folder navigation path

## Development

### Backend Only
```bash
cd FileFlow
export FLASK_APP=backend.app
backend/venv/bin/flask run --port=5000
```

### Frontend Only
```bash
cd frontend
npm start
```

### Build Frontend for Production
```bash
cd frontend
npm run build
```

### Run Tests
```bash
cd backend_fastapi
backend_fastapi/venv/bin/pytest
```

## Configuration

### Environment Variables (Optional)
- `FLASK_APP=backend.app` - Flask application entry point
- `FLASK_ENV=development` - Development mode
- `SECRET_KEY` - Flask secret key (auto-generated if not set)

### Database
- Location: `backend/instance/fileflow.db`
- Auto-created on first run
- SQLite database

### File Storage
- Location: `user_files/<user_id>/`
- Auto-created per user
- Organized by user ID

## Requirements

- **Python 3.8+** - Backend runtime
- **Node.js 14+** - Frontend runtime
- **npm** - Package manager

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
kill $(lsof -ti:5000)

# Kill process on port 3000
kill $(lsof -ti:3000)
```

### Dependencies Not Installing
```bash
# Manually create venv and install
cd FileFlow
python3 -m venv backend/venv
backend/venv/bin/pip install -r backend/requirements.txt

cd frontend
npm install
```

### Database Issues
```bash
# Remove and reinitialize database
rm backend/instance/fileflow.db
export FLASK_APP=backend.app
backend/venv/bin/flask init-db
```

## Documentation

- **FIXES.md** - Detailed fix documentation for frontend buttons
- **MIGRATION_PLAN.md** - Flask to FastAPI migration plan
- **MIGRATION_ROADMAP.md** - Migration roadmap and timeline

## License

This project is for educational purposes.

## Authors

FileFlow Team

---

**Need Help?** Check FIXES.md for detailed setup instructions and troubleshooting.
