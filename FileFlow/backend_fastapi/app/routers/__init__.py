from app.routers.auth import router as auth_router
from app.routers.files import router as files_router
from app.routers.folders import router as folders_router
from app.routers.search import router as search_router
from app.routers.compression import router as compression_router

__all__ = [
    "auth_router",
    "files_router",
    "folders_router",
    "search_router",
    "compression_router"
]
