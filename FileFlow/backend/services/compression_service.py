import zipfile
import tarfile
import py7zr
from pathlib import Path

class CompressionService:
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
            zipf.extractall(extract_to)

    @staticmethod
    def extract_tar(archive_path, extract_to):
        with tarfile.open(archive_path, 'r:*') as tarf:
            tarf.extractall(extract_to)

    @staticmethod
    def extract_7z(archive_path, extract_to, password=None):
        with py7zr.SevenZipFile(archive_path, 'r', password=password) as szf:
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
