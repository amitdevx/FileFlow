import re
from pathlib import Path


class Validators:
    """Utility class for validations"""
    
    INVALID_CHARS_PATTERN = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
    
    @staticmethod
    def is_valid_filename(filename: str) -> bool:
        """Check if filename is valid"""
        if not filename or filename in ['.', '..']:
            return False
        return not Validators.INVALID_CHARS_PATTERN.search(filename)
    
    @staticmethod
    def is_safe_path(base_path: str, target_path: str) -> bool:
        """Check if target path is within base path (prevents directory traversal)"""
        try:
            base = Path(base_path).resolve()
            target = Path(target_path).resolve()
            return target.is_relative_to(base)
        except (ValueError, RuntimeError):
            return False
    
    @staticmethod
    def validate_file_size(size: int, max_size: int = 100 * 1024 * 1024) -> bool:
        """Validate file size (default max: 100MB)"""
        return 0 < size <= max_size
    
    @staticmethod
    def allowed_file(filename: str, allowed_extensions: list[str]) -> bool:
        """Check if file extension is allowed"""
        if '.' not in filename:
            return False
        return filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename by removing/replacing invalid characters"""
        filename = Validators.INVALID_CHARS_PATTERN.sub('_', filename)
        filename = filename.strip('. ')
        return filename if filename else 'unnamed'
