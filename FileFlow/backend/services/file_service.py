from pathlib import Path
import os
import shutil
import mimetypes
from typing import Optional, List, Dict
from werkzeug.utils import secure_filename

class FileService:
    """Service for handling file operations"""
    
    def __init__(self, base_upload_path: str):
        self.base_upload_path = Path(base_upload_path)
        self.base_upload_path.mkdir(parents=True, exist_ok=True)
    
    def get_user_directory(self, user_id: int) -> Path:
        """Get user's upload directory"""
        user_dir = self.base_upload_path / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir
    
    def save_file(self, file, user_id: int, folder_path: Optional[str] = None) -> Dict[str, str]:
        """Save uploaded file"""
        filename = secure_filename(file.filename)
        user_dir = self.get_user_directory(user_id)
        
        if folder_path:
            target_dir = user_dir / folder_path
            target_dir.mkdir(parents=True, exist_ok=True)
        else:
            target_dir = user_dir
        
        filepath = target_dir / filename
        file.save(str(filepath))
        
        return {
            'filename': filename,
            'filepath': str(filepath),
            'size': filepath.stat().st_size,
            'mimetype': mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        }
    
    def delete_file(self, filepath: str) -> bool:
        """Delete a file"""
        try:
            path = Path(filepath)
            if path.exists() and path.is_file():
                path.unlink()
                return True
            return False
        except Exception as e:
            raise Exception(f"Error deleting file: {str(e)}")
    
    def delete_folder(self, folderpath: str) -> bool:
        """Delete a folder and all its contents"""
        try:
            path = Path(folderpath)
            if path.exists() and path.is_dir():
                shutil.rmtree(str(path))
                return True
            return False
        except Exception as e:
            raise Exception(f"Error deleting folder: {str(e)}")
    
    def move_file(self, source: str, destination: str) -> bool:
        """Move a file to a new location"""
        try:
            src_path = Path(source)
            dest_path = Path(destination)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dest_path))
            return True
        except Exception as e:
            raise Exception(f"Error moving file: {str(e)}")
    
    def copy_file(self, source: str, destination: str) -> bool:
        """Copy a file to a new location"""
        try:
            src_path = Path(source)
            dest_path = Path(destination)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src_path), str(dest_path))
            return True
        except Exception as e:
            raise Exception(f"Error copying file: {str(e)}")
    
    def get_file_info(self, filepath: str) -> Dict:
        """Get file information"""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        stat = path.stat()
        return {
            'name': path.name,
            'size': stat.st_size,
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
            'is_dir': path.is_dir(),
            'mimetype': mimetypes.guess_type(str(path))[0] if path.is_file() else None
        }
