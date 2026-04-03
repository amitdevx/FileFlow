import zipfile
import tarfile
import py7zr
from pathlib import Path


class CompressionService:
    """Service for handling compression operations"""
    
    @staticmethod
    def _is_safe_path(base_path: str, target_path: str) -> bool:
        """Check if target path is within base path (prevents directory traversal)"""
        try:
            base = Path(base_path).resolve()
            full_path = (base / target_path).resolve()
            return full_path.is_relative_to(base)
        except (ValueError, RuntimeError):
            return False
    
    @staticmethod
    def _validate_member(archive_path: str, member_name: str, extract_to: str) -> bool:
        """Validate that extracted file stays within extract_to directory"""
        if Path(member_name).is_absolute():
            raise ValueError(f"Absolute path in archive is not allowed: {member_name}")
        
        if '..' in Path(member_name).parts:
            raise ValueError(f"Path traversal attempt detected: {member_name}")
        
        if not CompressionService._is_safe_path(extract_to, member_name):
            raise ValueError(f"Attempted path traversal in archive: {member_name}")
        
        return True
    
    @staticmethod
    def create_zip(file_paths: list[str], archive_path: str, password: str | None = None) -> None:
        """Create a ZIP archive"""
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if password:
                zipf.setpassword(password.encode())
            for file_path in file_paths:
                zipf.write(file_path, Path(file_path).name)
    
    @staticmethod
    def create_tar(file_paths: list[str], archive_path: str, compression: str | None = None) -> None:
        """Create a TAR archive with optional compression"""
        mode = 'w'
        if compression:
            mode += f':{compression}'
        with tarfile.open(archive_path, mode) as tarf:
            for file_path in file_paths:
                tarf.add(file_path, arcname=Path(file_path).name)
    
    @staticmethod
    def create_7z(file_paths: list[str], archive_path: str, password: str | None = None) -> None:
        """Create a 7Z archive"""
        with py7zr.SevenZipFile(archive_path, 'w', password=password) as szf:
            for file_path in file_paths:
                szf.write(file_path, Path(file_path).name)
    
    @staticmethod
    def extract_zip(archive_path: str, extract_to: str, password: str | None = None) -> None:
        """Extract a ZIP archive"""
        with zipfile.ZipFile(archive_path, 'r') as zipf:
            if password:
                zipf.setpassword(password.encode())
            for member in zipf.namelist():
                CompressionService._validate_member(archive_path, member, extract_to)
            zipf.extractall(extract_to)
    
    @staticmethod
    def extract_tar(archive_path: str, extract_to: str) -> None:
        """Extract a TAR archive"""
        with tarfile.open(archive_path, 'r:*') as tarf:
            for member in tarf.getmembers():
                CompressionService._validate_member(archive_path, member.name, extract_to)
            try:
                tarf.extractall(extract_to, filter='data')
            except TypeError:
                tarf.extractall(extract_to)
    
    @staticmethod
    def extract_7z(archive_path: str, extract_to: str, password: str | None = None) -> None:
        """Extract a 7Z archive"""
        with py7zr.SevenZipFile(archive_path, 'r', password=password) as szf:
            for member in szf.getnames():
                CompressionService._validate_member(archive_path, member, extract_to)
            szf.extractall(extract_to)
    
    @staticmethod
    def list_archive_contents(archive_path: str) -> list[str]:
        """List contents of an archive"""
        ext = Path(archive_path).suffix.lower()
        
        if ext == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zf:
                return zf.namelist()
        elif ext in ['.tar', '.gz', '.bz2', '.xz']:
            with tarfile.open(archive_path, 'r:*') as tf:
                return tf.getnames()
        elif ext == '.7z':
            with py7zr.SevenZipFile(archive_path, 'r') as szf:
                return szf.getnames()
        else:
            raise ValueError("Unsupported archive format")


# Singleton instance
compression_service = CompressionService()
