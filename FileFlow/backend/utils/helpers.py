import hashlib
from pathlib import Path
from typing import List, Dict
from datetime import datetime

class Helpers:
    """Utility helper functions"""
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    @staticmethod
    def get_file_hash(filepath: str, algorithm: str = 'md5') -> str:
        """Calculate file hash"""
        hash_func = getattr(hashlib, algorithm)()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    
    @staticmethod
    def find_duplicates(directory: str) -> Dict[str, List[str]]:
        """Find duplicate files in a directory based on hash"""
        hashes = {}
        for filepath in Path(directory).rglob('*'):
            if filepath.is_file():
                file_hash = Helpers.get_file_hash(str(filepath))
                if file_hash in hashes:
                    hashes[file_hash].append(str(filepath))
                else:
                    hashes[file_hash] = [str(filepath)]
        
        # Return only duplicates
        return {k: v for k, v in hashes.items() if len(v) > 1}
    
    @staticmethod
    def format_datetime(timestamp: float) -> str:
        """Format timestamp to readable datetime"""
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def get_file_icon(mimetype: str) -> str:
        """Get Font Awesome icon class based on mimetype"""
        if not mimetype:
            return 'fa-file'
        
        type_map = {
            'image': 'fa-file-image',
            'video': 'fa-file-video',
            'audio': 'fa-file-audio',
            'pdf': 'fa-file-pdf',
            'zip': 'fa-file-archive',
            'tar': 'fa-file-archive',
            '7z': 'fa-file-archive',
            'text': 'fa-file-alt',
            'code': 'fa-file-code',
        }
        
        main_type = mimetype.split('/')[0]
        if main_type in type_map:
            return type_map[main_type]
        
        for key, icon in type_map.items():
            if key in mimetype:
                return icon
        
        return 'fa-file'
