import re
from pathlib import Path
from typing import List

class Validators:
    """Utility class for validations"""
    
    @staticmethod
    def is_valid_filename(filename: str) -> bool:
        """Check if filename is valid"""
        if not filename or filename in ['.', '..']:
            return False
        # Check for invalid characters
        invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
        return not re.search(invalid_chars, filename)
    
    @staticmethod
    def is_safe_path(base_path: str, target_path: str) -> bool:
        """Check if target path is within base path (prevents directory traversal)"""
        try:
            base = Path(base_path).resolve()
            target = Path(target_path).resolve()
            return target.is_relative_to(base)
        except:
            return False
    
    @staticmethod
    def validate_file_size(size: int, max_size: int = 100 * 1024 * 1024) -> bool:
        """Validate file size (default max: 100MB)"""
        return 0 < size <= max_size
    
    @staticmethod
    def allowed_file(filename: str, allowed_extensions: List[str]) -> bool:
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename by removing/replacing invalid characters"""
        # Replace invalid characters with underscore
        filename = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', filename)
        # Remove leading/trailing spaces and dots
        filename = filename.strip('. ')
        return filename if filename else 'unnamed'
