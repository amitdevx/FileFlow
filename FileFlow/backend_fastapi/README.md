# FileFlow FastAPI Backend

A modern, async file management API built with FastAPI.

## Features

- ⚡ **Async/Await** - Non-blocking I/O operations
- 🔐 **JWT Authentication** - Secure token-based auth
- 📁 **File Management** - Upload, download, view, delete files
- 📂 **Folder Operations** - Create, navigate, delete folders
- 🔍 **Advanced Search** - Search by name, type, size, date
- 📦 **Compression** - ZIP, TAR, 7Z support
- 📖 **Auto Documentation** - Swagger UI and ReDoc

## Quick Start

### Prerequisites

- Python 3.11+
- pip or uv package manager

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your settings

# Run the server
uvicorn main:app --reload
```

### API Documentation

- Swagger UI: http://localhost:5000/api/docs
- ReDoc: http://localhost:5000/api/redoc
- OpenAPI JSON: http://localhost:5000/api/openapi.json

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login and get tokens
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info

### Files
- `GET /api/files` - List files
- `POST /api/files/upload` - Upload file
- `GET /api/files/download/{id}` - Download file
- `GET /api/files/view/{id}` - View file
- `DELETE /api/files/{id}` - Delete file
- `POST /api/files/{id}/rename` - Rename file
- `POST /api/files/{id}/move` - Move file
- `POST /api/files/{id}/favorite` - Toggle favorite

### Folders
- `GET /api/folders` - List folder contents
- `POST /api/folders` - Create folder
- `GET /api/folders/{id}` - Open folder
- `DELETE /api/folders/{id}` - Delete folder

### Search
- `POST /api/search` - Search files
- `GET /api/search/profiles` - Get search profiles
- `POST /api/search/profiles` - Save search profile
- `DELETE /api/search/profiles/{id}` - Delete profile

### Compression
- `POST /api/compress/create` - Create archive
- `POST /api/compress/extract/{id}` - Extract archive
- `GET /api/compress/list/{id}` - List archive contents

## Project Structure

```
backend_fastapi/
├── app/
│   ├── __init__.py
│   ├── config.py           # Settings with pydantic
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py     # Async SQLAlchemy setup
│   │   └── models.py       # ORM models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py      # Pydantic schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py         # Auth endpoints
│   │   ├── files.py        # File endpoints
│   │   ├── folders.py      # Folder endpoints
│   │   ├── search.py       # Search endpoints
│   │   └── compression.py  # Compression endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py      # JWT/password handling
│   │   ├── file_service.py      # Async file operations
│   │   ├── compression_service.py
│   │   └── watcher_service.py
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       └── helpers.py
├── main.py                 # FastAPI application
├── requirements.txt
├── .env.example
└── README.md
```

## Migration from Flask

This backend is a migration from the Flask-based backend with the following improvements:

| Feature | Flask | FastAPI |
|---------|-------|---------|
| Async Support | No | Yes |
| Type Safety | Limited | Full Pydantic |
| API Docs | Manual | Automatic |
| Validation | Flask-WTF | Pydantic |
| Authentication | Session-based | JWT |
| Performance | Sync | Async |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DEBUG | Enable debug mode | false |
| SECRET_KEY | JWT secret key | random |
| DATABASE_URL | SQLite connection string | sqlite+aiosqlite:///./fileflow.db |
| ACCESS_TOKEN_EXPIRE_MINUTES | JWT access token lifetime | 30 |
| UPLOAD_FOLDER | File storage directory | user_files |
| MAX_FILE_SIZE | Maximum upload size (bytes) | 104857600 (100MB) |
| CORS_ORIGINS | Allowed CORS origins | ["http://localhost:3000"] |

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app
```

## License

MIT License
