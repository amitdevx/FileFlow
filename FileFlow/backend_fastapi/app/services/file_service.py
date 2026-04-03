import aiofiles
import aiofiles.os
import shutil
import mimetypes
from pathlib import Path
from typing import BinaryIO
from app.config import get_settings
from app.utils import calculate_file_hash

settings = get_settings()


class FileService:
    """Async service for handling file operations"""
    
    def __init__(self, base_upload_path: str | None = None):
        self.base_upload_path = Path(base_upload_path or settings.upload_folder)
        self.base_upload_path.mkdir(parents=True, exist_ok=True)
    
    def get_user_directory(self, user_id: int) -> Path:
        """Get user's upload directory"""
        user_dir = self.base_upload_path / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir
    
    async def save_file(
        self, 
        file_content: BinaryIO, 
        filename: str,
        user_id: int, 
        folder_path: str | None = None
    ) -> dict:
        """Save uploaded file asynchronously"""
        user_dir = self.get_user_directory(user_id)
        
        if folder_path:
            target_dir = user_dir / folder_path
            target_dir.mkdir(parents=True, exist_ok=True)
        else:
            target_dir = user_dir
        
        filepath = target_dir / filename
        
        # Handle duplicate filenames
        counter = 1
        original_stem = filepath.stem
        original_suffix = filepath.suffix
        while filepath.exists():
            filepath = target_dir / f"{original_stem}_{counter}{original_suffix}"
            counter += 1
        
        # Write file asynchronously
        async with aiofiles.open(filepath, 'wb') as f:
            content = file_content.read()
            await f.write(content)
        
        stat = filepath.stat()
        mimetype, _ = mimetypes.guess_type(str(filepath))
        
        return {
            'filename': filepath.name,
            'filepath': str(filepath),
            'size': stat.st_size,
            'mimetype': mimetype or 'application/octet-stream',
            'file_hash': calculate_file_hash(str(filepath))
        }
    
    async def delete_file(self, filepath: str) -> bool:
        """Delete a file asynchronously"""
        path = Path(filepath)
        if path.exists() and path.is_file():
            await aiofiles.os.remove(str(path))
            return True
        return False
    
    async def delete_folder(self, folderpath: str) -> bool:
        """Delete a folder and all its contents"""
        path = Path(folderpath)
        if path.exists() and path.is_dir():
            shutil.rmtree(str(path))
            return True
        return False
    
    async def move_file(self, source: str, destination: str) -> bool:
        """Move a file to a new location"""
        src_path = Path(source)
        dest_path = Path(destination)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_path), str(dest_path))
        return True
    
    async def copy_file(self, source: str, destination: str) -> bool:
        """Copy a file to a new location"""
        src_path = Path(source)
        dest_path = Path(destination)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Async copy
        async with aiofiles.open(src_path, 'rb') as src:
            async with aiofiles.open(dest_path, 'wb') as dst:
                while chunk := await src.read(8192):
                    await dst.write(chunk)
        return True
    
    async def read_file_chunks(self, filepath: str, chunk_size: int = 8192):
        """Read file in chunks for streaming responses"""
        async with aiofiles.open(filepath, 'rb') as f:
            while chunk := await f.read(chunk_size):
                yield chunk
    
    def get_file_info(self, filepath: str) -> dict:
        """Get file information"""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        stat = path.stat()
        mimetype, _ = mimetypes.guess_type(str(path))
        
        return {
            'name': path.name,
            'size': stat.st_size,
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
            'is_dir': path.is_dir(),
            'mimetype': mimetype if path.is_file() else None
        }


# Singleton instance
file_service = FileService()
