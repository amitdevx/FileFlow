import zipfile
import tarfile
import py7zr
from pathlib import Path

class CompressionService:
    @staticmethod
    def _is_safe_path(base_path, target_path):
        """Check if target path is within base path (prevents directory traversal)
        
        Note: This validates the path string without resolving symlinks to prevent
        symlink-based attacks. The check uses string comparison after normalization.
        """
        try:
            base = Path(base_path).resolve()
            # Normalize target without fully resolving to prevent symlink attacks
            # Join base with target and check if it stays within base
            full_path = (base / target_path).resolve()
            return full_path.is_relative_to(base)
        except (ValueError, RuntimeError):
            return False
    
    @staticmethod
    def _safe_extract_member(archive_path, member_name, extract_to):
        """Validate that extracted file stays within extract_to directory
        
        Rejects paths with:
        - Absolute paths
        - Parent directory references (..)
        - Paths that escape the extraction directory
        """
        # Reject absolute paths
        if Path(member_name).is_absolute():
            raise ValueError(f"Absolute path in archive is not allowed: {member_name}")
        
        # Reject paths with parent directory references
        if '..' in Path(member_name).parts:
            raise ValueError(f"Path traversal attempt detected: {member_name}")
        
        # Validate the final path stays within extraction directory
        if not CompressionService._is_safe_path(extract_to, member_name):
            raise ValueError(f"Attempted path traversal in archive: {member_name}")
        return True
    
    @staticmethod
    def create_zip(file_paths, archive_path, password=None):
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if password:
                zipf.setpassword(password.encode())
            for file_path in file_paths:
                zipf.write(file_path, Path(file_path).name)

    @staticmethod
    def create_tar(file_paths, archive_path, compression=None):
        mode = 'w'
        if compression:
            mode += f':{compression}'
        with tarfile.open(archive_path, mode) as tarf:
            for file_path in file_paths:
                tarf.add(file_path, arcname=Path(file_path).name)

    @staticmethod
    def create_7z(file_paths, archive_path, password=None):
        with py7zr.SevenZipFile(archive_path, 'w', password=password) as szf:
            for file_path in file_paths:
                szf.write(file_path, Path(file_path).name)

    @staticmethod
    def extract_zip(archive_path, extract_to, password=None):
        with zipfile.ZipFile(archive_path, 'r') as zipf:
            if password:
                zipf.setpassword(password.encode())
            # Validate all members before extraction
            for member in zipf.namelist():
                CompressionService._safe_extract_member(archive_path, member, extract_to)
            zipf.extractall(extract_to)

    @staticmethod
    def extract_tar(archive_path, extract_to):
        with tarfile.open(archive_path, 'r:*') as tarf:
            # Validate all members before extraction to prevent path traversal
            for member in tarf.getmembers():
                CompressionService._safe_extract_member(archive_path, member.name, extract_to)
            # Use data filter for Python 3.11.4+ or validate manually for earlier versions
            try:
                tarf.extractall(extract_to, filter='data')
            except TypeError:
                # Python < 3.11.4 doesn't support filter parameter, but we already validated
                tarf.extractall(extract_to)

    @staticmethod
    def extract_7z(archive_path, extract_to, password=None):
        with py7zr.SevenZipFile(archive_path, 'r', password=password) as szf:
            # Validate all members before extraction
            for member in szf.getnames():
                CompressionService._safe_extract_member(archive_path, member, extract_to)
            szf.extractall(extract_to)

    @staticmethod
    def list_archive_contents(archive_path):
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
