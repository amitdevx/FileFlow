# FileFlow Backend Migration: Flask to FastAPI

## Problem Statement
The FileFlow application currently uses Flask for the backend. We need to migrate to FastAPI to gain:
- Better performance with async/await support
- Automatic API documentation (OpenAPI/Swagger)
- Better type safety with Pydantic models
- Modern Python async capabilities for file operations
- Built-in request/response validation

## Current State
- **Backend**: Flask with Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, Flask-CORS
- **Frontend**: React (remains unchanged)
- **Database**: SQLite with SQLAlchemy ORM
- **Features**: File management, folder operations, search, compression, authentication

## Target State
- **Backend**: FastAPI with SQLAlchemy 2.0, Pydantic, python-multipart
- **Frontend**: React (no changes needed)
- **Database**: SQLite with async SQLAlchemy
- **Features**: Same functionality with improved performance and validation

## Migration Approach
1. Set up FastAPI project structure alongside Flask
2. Migrate database models to async SQLAlchemy
3. Create Pydantic schemas for request/response validation
4. Convert Flask routes to FastAPI endpoints
5. Implement async file operations
6. Migrate authentication to JWT-based system
7. Update frontend API calls (minimal changes)
8. Test and validate all functionality
9. Deprecate Flask backend

## Key Differences to Address

### Authentication
- **Flask**: Session-based with Flask-Login
- **FastAPI**: JWT tokens with OAuth2 password bearer

### Request Handling
- **Flask**: Synchronous with request object
- **FastAPI**: Async with dependency injection

### Database Operations
- **Flask**: Synchronous SQLAlchemy
- **FastAPI**: Async SQLAlchemy with asyncio

### File Uploads
- **Flask**: request.files
- **FastAPI**: UploadFile with async streaming

### Response Types
- **Flask**: jsonify, render_template
- **FastAPI**: Pydantic models, automatic JSON serialization

## Dependencies Mapping

### Current (Flask)
- flask → fastapi
- flask-sqlalchemy → sqlalchemy[asyncio] + aiosqlite
- flask-login → python-jose[cryptography] (JWT)
- flask-bcrypt → passlib[bcrypt]
- flask-cors → fastapi.middleware.cors
- flask-wtf → pydantic (built-in validation)

### Additional Dependencies
- uvicorn (ASGI server)
- python-multipart (file uploads)
- aiofiles (async file operations)
- pydantic-settings (configuration)

## Todos

See SQL database for detailed todo tracking with dependencies.

## Notes

### Compatibility Considerations
- Frontend React app requires minimal changes (mostly auth token handling)
- SQLite database schema can be reused with migrations
- File storage structure remains unchanged
- API endpoint paths should match existing Flask routes for easier migration

### Performance Benefits
- Async file operations for upload/download
- Concurrent request handling
- Streaming responses for large files
- WebSocket support for real-time file watching

### Testing Strategy
- Run both Flask and FastAPI servers during transition
- Use feature flags to route traffic
- Comprehensive API testing suite
- Load testing to validate performance improvements

### Risks and Mitigation
- **Risk**: Breaking changes in API behavior
  - **Mitigation**: Maintain API contract, extensive testing
  
- **Risk**: Authentication migration complexity
  - **Mitigation**: Implement token exchange endpoint for smooth transition
  
- **Risk**: Async complexity in file operations
  - **Mitigation**: Incremental migration, fallback to sync operations where needed

### Future Enhancements (Post-Migration)
- WebSocket support for real-time updates
- GraphQL API option
- Background task queue with Celery/ARQ
- Redis caching layer
- Multi-database support (PostgreSQL, MySQL)
