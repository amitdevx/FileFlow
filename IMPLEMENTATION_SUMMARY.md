# FileFlow - Modern File Management System

A comprehensive, feature-rich file management system with a modern UI, built with Flask and React.

## 🎯 Features Implemented

### Phase 1: Foundation ✅

#### Real File Manager Dashboard
- ✅ **Dual-pane layout** - Modern file browser with dedicated preview panel
- ✅ **Multiple view modes** - List, Grid, and Details views with easy switching
- ✅ **Real-time file preview panel** - Preview images, videos, PDFs, and text files
- ✅ **Breadcrumb navigation** - Easy path traversal with clickable breadcrumbs
- ✅ **Back/Forward navigation** - Browser-style history navigation

#### Advanced Toolbar
- ✅ Quick action buttons (Upload, Create Folder, Rename, Delete, Copy, Cut, Paste)
- ✅ View toggle buttons (List/Grid/Details)
- ✅ Search and filter bar with advanced options
- ✅ Theme toggle (Dark/Light mode)

#### Status Bar & Information Panel
- ✅ Display selected file count and total size
- ✅ Current path and file count display
- ✅ Keyboard shortcut hints

### Phase 2: Core Features ✅

#### Folder Operations
- ✅ Create/Delete folders
- ✅ Nested folder structure support
- ✅ Folder navigation with breadcrumbs
- ✅ Back/Forward buttons with history

#### Advanced File Moving & Copying
- ✅ **Drag & Drop** - Drag files between folders
- ✅ **Cut/Copy/Paste Operations** - Full clipboard support
- ✅ **Context Menus** - Right-click actions for files and folders

#### Keyboard Shortcuts
- ✅ `Ctrl+A` - Select all files
- ✅ `Ctrl+C` - Copy selected files
- ✅ `Ctrl+X` - Cut selected files
- ✅ `Ctrl+V` - Paste files
- ✅ `Delete` - Delete selected files
- ✅ `F2` - Rename selected file
- ✅ `Escape` - Clear selection
- ✅ `Alt+Left` - Navigate back
- ✅ `Alt+Right` - Navigate forward

### Phase 3: Polish & Advanced Features ✅

#### Search & Filtering
- ✅ **Full-text search** - Search by filename and tags
- ✅ **File type filters** - Filter by image, video, audio, PDF, text
- ✅ **Size range filters** - Filter files by size
- ✅ **Date range filters** - Filter by creation/modification date
- ✅ **Saved search profiles** - Save and reuse common searches

#### File Preview
- ✅ **Image preview** - View images directly in preview panel
- ✅ **Text file preview** - View text files inline
- ✅ **PDF preview** - Embedded PDF viewer
- ✅ **Video/Audio preview** - Built-in media player

#### Compression Utilities
- ✅ **Create archives** - ZIP, TAR, 7Z support
- ✅ **Extract archives** - With password support
- ✅ **Archive browsing** - View contents before extraction

#### Theme Support
- ✅ **Dark/Light theme toggle** - System-wide theme switching
- ✅ **Persistent theme** - Saves preference to localStorage
- ✅ **Smooth transitions** - Animated theme switching

### Technical Enhancements ✅

#### Backend Improvements (Python)
- ✅ **Pathlib usage** - Robust cross-platform file path handling
- ✅ **Service layer architecture** - FileService, CompressionService, WatcherService
- ✅ **Database caching** - SQLite-based metadata caching for faster searches
- ✅ **Compression support** - ZIP, TAR, 7Z with py7zr
- ✅ **File watching** - Real-time updates with watchdog library
- ✅ **Validation utilities** - Comprehensive file validation and sanitization
- ✅ **Helper utilities** - File size formatting, hash calculation, duplicate detection

#### Frontend Enhancements (React)
- ✅ **React framework** - Modern component-based architecture
- ✅ **Context API** - State management with ThemeContext and FileContext
- ✅ **Keyboard shortcuts** - Power user navigation support
- ✅ **Responsive design** - Mobile and tablet support
- ✅ **Dark/Light theme** - Complete theme system
- ✅ **Context menus** - Right-click actions

## 📁 Project Structure

```
FileFlow/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── config.py                 # Configuration
│   ├── requirements.txt          # Python dependencies
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication routes
│   │   ├── files.py             # File operations
│   │   ├── folders.py           # Folder operations
│   │   ├── search.py            # Search & filtering
│   │   ├── upload.py            # File upload
│   │   └── compression.py       # Archive operations
│   ├── services/
│   │   ├── file_service.py      # File operations service
│   │   ├── compression_service.py # Compression utilities
│   │   └── watcher_service.py   # File system watcher
│   ├── models/
│   │   └── database.py          # Database models
│   └── utils/
│       ├── validators.py        # Input validation
│       └── helpers.py           # Utility functions
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js               # Main React component
│   │   ├── App.css              # Global styles
│   │   ├── components/
│   │   │   ├── Toolbar.js       # Toolbar component
│   │   │   ├── Breadcrumb.js    # Breadcrumb navigation
│   │   │   ├── FileList.js      # File list display
│   │   │   ├── StatusBar.js     # Status bar
│   │   │   ├── SearchPanel.js   # Search interface
│   │   │   ├── PreviewPanel.js  # File preview
│   │   │   └── ContextMenu.js   # Right-click menu
│   │   └── context/
│   │       ├── ThemeContext.js  # Theme management
│   │       └── FileContext.js   # File operations state
│   └── package.json
└── .github/
    └── workflows/
        └── ci.yml               # CI/CD pipeline
```

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd FileFlow/backend
pip install -r ../requirements.txt
flask init-db  # Initialize the database
flask run
```

### Frontend Setup

```bash
cd FileFlow/frontend
npm install
npm start
```

## 🔧 Configuration

### Backend Configuration (`backend/config.py`)
- Database URI
- Upload folder path
- Secret key
- Max file size

### Environment Variables
```
FLASK_APP=backend/app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///fileflow.db
```

## 📝 API Endpoints

### Authentication
- `POST /signup` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Files
- `GET /api/files` - List files
- `POST /api/upload` - Upload file
- `GET /api/download_file/<id>` - Download file
- `GET /api/view_file/<id>` - View file
- `DELETE /api/delete_file/<id>` - Delete file
- `POST /api/rename_file/<id>` - Rename file
- `POST /api/move_file/<id>` - Move file

### Folders
- `GET /dashboard` - Dashboard view
- `GET /dashboard/<folder_id>` - Folder contents
- `POST /api/create_folder` - Create folder

### Search
- `POST /api/search` - Advanced search
- `GET /api/search/profiles` - Get saved searches
- `POST /api/search/profiles` - Save search profile
- `DELETE /api/search/profiles/<id>` - Delete search profile

### Compression
- `POST /api/compress/create` - Create archive
- `POST /api/compress/extract/<id>` - Extract archive
- `GET /api/compress/list/<id>` - List archive contents

## 🎨 Theming

The application supports dark and light themes. Toggle between themes using the theme button in the toolbar. The preference is saved to localStorage and persists across sessions.

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+A` | Select all files |
| `Ctrl+C` | Copy selected files |
| `Ctrl+X` | Cut selected files |
| `Ctrl+V` | Paste files |
| `Delete` | Delete selected files |
| `F2` | Rename selected file |
| `Escape` | Clear selection |
| `Alt+Left` | Navigate back |
| `Alt+Right` | Navigate forward |

## 🧪 Testing

### Backend Tests
```bash
cd FileFlow
python -m pytest backend/tests/
```

### Frontend Tests
```bash
cd FileFlow/frontend
npm test
```

## 🚀 Deployment

The project includes a GitHub Actions CI/CD pipeline that:
- Lints Python code with flake8
- Runs backend tests
- Builds the React frontend
- Runs frontend tests

## 📦 Dependencies

### Backend
- Flask - Web framework
- Flask-SQLAlchemy - ORM
- Flask-Login - Authentication
- Flask-Bcrypt - Password hashing
- watchdog - File system monitoring
- py7zr - 7Z compression
- pillow - Image processing
- python-magic - File type detection

### Frontend
- React - UI framework
- axios - HTTP client
- Font Awesome - Icons

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

MIT License

## 🎉 Acknowledgments

Built with modern best practices and user experience in mind.
