import zipfile
import tarfile
import py7zr
from pathlib import Path

class CompressionService:
    @staticmethod
    def _is_safe_path(base_path, target_path):
        """Check if target path is within base path (prevents directory traversal)"""
        try:
            base = Path(base_path).resolve()
            target = Path(target_path).resolve()
            return target.is_relative_to(base)
        except (ValueError, RuntimeError):
            return False
    
    @staticmethod
    def _safe_extract_member(archive_path, member_name, extract_to):
        """Validate that extracted file stays within extract_to directory"""
        target_path = Path(extract_to) / member_name
        if not CompressionService._is_safe_path(extract_to, target_path):
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
            # Use data filter for Python 3.12+ or validate manually for earlier versions
            try:
                tarf.extractall(extract_to, filter='data')
            except TypeError:
                # Python < 3.12 doesn't support filter parameter, but we already validated
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
