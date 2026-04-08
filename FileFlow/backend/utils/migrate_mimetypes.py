"""
Utility script to migrate existing files and populate missing MIME types.
Run this after updating to the new version to fix files uploaded before the MIME type fix.

Usage:
    python migrate_mimetypes.py
    
    Or from Flask shell:
    from backend.utils.migrate_mimetypes import migrate_all_files
    migrate_all_files()
"""

from pathlib import Path
from mimetypes import guess_type
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate_all_files(db=None, File=None):
    """
    Migrate all files in database to have MIME types set.
    If called from Flask shell, db and File will be injected.
    """
    try:
        if db is None or File is None:
            # Import locally if not provided
            try:
                from backend.models.database import db, File
            except ImportError:
                from models.database import db, File
        
        files = File.query.filter_by(is_folder=False).all()
        updated_count = 0
        error_count = 0
        
        logger.info(f"Starting migration of {len(files)} files...")
        
        for file in files:
            try:
                # Skip if already has MIME type
                if file.mimetype and file.mimetype != 'application/octet-stream':
                    logger.debug(f"File {file.id} already has MIME type: {file.mimetype}")
                    continue
                
                # Try to guess MIME type from file extension
                filepath = Path(file.filepath)
                if filepath.exists():
                    mimetype, _ = guess_type(str(filepath))
                    if not mimetype:
                        mimetype = 'application/octet-stream'
                else:
                    logger.warning(f"File not found on disk: {file.filepath}")
                    mimetype = 'application/octet-stream'
                
                # Update database
                file.mimetype = mimetype
                db.session.add(file)
                updated_count += 1
                logger.info(f"Updated file {file.id}: {file.filename} -> {mimetype}")
                
            except Exception as e:
                error_count += 1
                logger.error(f"Error updating file {file.id}: {str(e)}", exc_info=True)
        
        # Commit all changes
        db.session.commit()
        logger.info(f"Migration complete: {updated_count} files updated, {error_count} errors")
        return {
            'success': True,
            'updated': updated_count,
            'errors': error_count
        }
        
    except Exception as e:
        if db:
            db.session.rollback()
        logger.error(f"Migration failed: {str(e)}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == '__main__':
    # Can be run as standalone script
    result = migrate_all_files()
    print(result)
