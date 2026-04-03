import hashlib
import mimetypes
from pathlib import Path


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def calculate_file_hash(filepath: str, algorithm: str = "sha256") -> str:
    """Calculate hash of a file"""
    hash_func = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def get_mimetype(filepath: str) -> str:
    """Get mimetype of a file"""
    mimetype, _ = mimetypes.guess_type(filepath)
    return mimetype or "application/octet-stream"


def get_file_extension(filename: str) -> str:
    """Get file extension"""
    return Path(filename).suffix.lower().lstrip('.')


def is_image(mimetype: str | None) -> bool:
    """Check if file is an image"""
    return mimetype is not None and mimetype.startswith("image/")


def is_video(mimetype: str | None) -> bool:
    """Check if file is a video"""
    return mimetype is not None and mimetype.startswith("video/")


def is_audio(mimetype: str | None) -> bool:
    """Check if file is audio"""
    return mimetype is not None and mimetype.startswith("audio/")


def is_pdf(mimetype: str | None) -> bool:
    """Check if file is a PDF"""
    return mimetype == "application/pdf"


def is_text(mimetype: str | None) -> bool:
    """Check if file is text"""
    return mimetype is not None and mimetype.startswith("text/")


def is_archive(mimetype: str | None) -> bool:
    """Check if file is an archive"""
    archive_types = [
        "application/zip",
        "application/x-tar",
        "application/x-7z-compressed",
        "application/gzip",
        "application/x-bzip2"
    ]
    return mimetype in archive_types
