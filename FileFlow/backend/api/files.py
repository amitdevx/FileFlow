from flask import Blueprint, send_file, abort, jsonify, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
try:
    from backend.models.database import db, File
    from backend.utils.validators import Validators
except ImportError:
    from models.database import db, File
    from utils.validators import Validators
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

files_bp = Blueprint('files_bp', __name__)

@files_bp.route('/api/files')
@login_required
def get_files():
    """JSON API endpoint to get files for the current user"""
    folder_id = request.args.get('folder_id', type=int)
    user_files = File.query.filter_by(user_id=current_user.id, parent_folder_id=folder_id).order_by(
        File.is_folder.desc(),
        File.filename
    ).all()
    
    files_list = []
    for f in user_files:
        files_list.append({
            'id': f.id,
            'name': f.filename,
            'filename': f.filename,
            'is_folder': f.is_folder,
            'size': f.filesize if hasattr(f, 'filesize') else 0,
            'created_at': f.created_at.isoformat() if hasattr(f, 'created_at') and f.created_at else None,
            'parent_folder_id': f.parent_folder_id
        })
    
    return jsonify(files_list)

@files_bp.route('/api/breadcrumbs/<int:folder_id>')
@login_required
def get_breadcrumbs(folder_id):
    """Get breadcrumb trail for a folder"""
    breadcrumbs = []
    folder = File.query.get(folder_id)
    
    while folder:
        if folder.user_id != current_user.id:
            break
        breadcrumbs.append({'id': folder.id, 'name': folder.filename})
        folder = File.query.get(folder.parent_folder_id) if folder.parent_folder_id else None
    
    breadcrumbs.reverse()
    return jsonify(breadcrumbs)

@files_bp.route('/download_file/<int:file_id>')
@login_required
def download_file(file_id):
    try:
        file = File.query.get_or_404(file_id)
        
        if file.user_id != current_user.id:
            abort(403, description="You don't have permission to access this file")
            
        filepath = Path(file.filepath)
        if not filepath.exists():
            logger.warning(f"File not found on disk: {file.filepath}")
            abort(404, description="File not found in storage")
            
        if file.is_folder:
            abort(400, description="Cannot download a folder")
        
        mimetype = file.mimetype or 'application/octet-stream'
        return send_file(
            str(filepath),
            as_attachment=True,
            download_name=secure_filename(file.filename),
            mimetype=mimetype
        )
        
    except Exception as e:
        logger.error(f"Error downloading file {file_id}: {str(e)}", exc_info=True)
        abort(500, description="Error occurred while downloading file")

@files_bp.route('/view_file/<int:file_id>')
@login_required
def view_file(file_id):
    try:
        file = File.query.get_or_404(file_id)
        
        if file.user_id != current_user.id:
            abort(403, description="You don't have permission to access this file")
            
        filepath = Path(file.filepath)
        if not filepath.exists():
            logger.warning(f"File not found on disk: {file.filepath}")
            abort(404, description="File not found in storage")
            
        if file.is_folder:
            abort(400, description="Cannot view a folder")
        
        mimetype = file.mimetype or 'application/octet-stream'
        return send_file(
            str(filepath),
            as_attachment=False,
            mimetype=mimetype
        )
        
    except Exception as e:
        logger.error(f"Error viewing file {file_id}: {str(e)}", exc_info=True)
        abort(500, description="Error occurred while viewing file")

@files_bp.route('/delete_file/<int:file_id>', methods=['DELETE'])
@login_required
def delete_file(file_id):
    try:
        file = File.query.get_or_404(file_id)
        
        if file.user_id != current_user.id:
            abort(403, description="You don't have permission to delete this file")
        
        if file.is_folder:
            def delete_folder_contents(folder_id):
                contents = File.query.filter_by(parent_folder_id=folder_id).all()
                for item in contents:
                    if item.is_folder:
                        delete_folder_contents(item.id)
                    else:
                        try:
                            filepath = Path(item.filepath)
                            if filepath.exists():
                                filepath.unlink()
                        except OSError as e:
                            logger.warning(f"Error deleting file {item.filepath}: {str(e)}")
                            pass
                    db.session.delete(item)
                
            delete_folder_contents(file.id)
        else:
            try:
                filepath = Path(file.filepath)
                if filepath.exists():
                    filepath.unlink()
            except OSError as e:
                logger.warning(f"Error deleting file {file.filepath}: {str(e)}")
                pass
        
        db.session.delete(file)
        db.session.commit()
        return jsonify({'message': 'File deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error in delete_file: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to delete file'}), 500

@files_bp.route('/rename_file/<int:file_id>', methods=['POST'])
@login_required
def rename_file(file_id):
    file_to_rename = File.query.get_or_404(file_id)
    if file_to_rename.user_id != current_user.id:
        abort(403)

    data = request.get_json()
    new_name = data.get('new_name')

    if not new_name:
        abort(400, description="New name is required")
    
    # Validate and sanitize the filename
    if not Validators.is_valid_filename(new_name):
        abort(400, description="Invalid filename")
    
    # Sanitize the filename to remove any dangerous characters
    sanitized_name = Validators.sanitize_filename(new_name)
    
    file_to_rename.filename = sanitized_name
    db.session.commit()
    return jsonify({'success': True, 'new_name': sanitized_name})

@files_bp.route('/move_file/<int:file_id>', methods=['POST'])
@login_required
def move_file(file_id):
    file_to_move = File.query.get_or_404(file_id)
    if file_to_move.user_id != current_user.id:
        abort(403)

    data = request.get_json()
    destination_folder_id = data.get('destination_folder_id')

    if destination_folder_id:
        destination_folder = File.query.get_or_404(destination_folder_id)
        if not destination_folder.is_folder or destination_folder.user_id != current_user.id:
            abort(400)
        file_to_move.parent_folder_id = destination_folder_id
    else:  # Move to root
        file_to_move.parent_folder_id = None

    db.session.commit()
    return jsonify({'success': True})
