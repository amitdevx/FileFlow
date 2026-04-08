from flask import Blueprint, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from mimetypes import guess_type
try:
    from backend.models.database import db, File
    from backend.utils.validators import Validators
except ImportError:
    from models.database import db, File
    from utils.validators import Validators
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    # Check if this is an AJAX/API request
    is_api_request = request.headers.get('Accept') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if 'file' not in request.files:
        if is_api_request:
            return jsonify({'error': 'No file part'}), 400
        flash('No file part')
        return redirect(url_for('folders_bp.dashboard'))
    
    file = request.files['file']
    folder_id = request.form.get('folder_id')
    
    if file.filename == '':
        if is_api_request:
            return jsonify({'error': 'No selected file'}), 400
        flash('No selected file')
        return redirect(url_for('folders_bp.dashboard'))

    # Define allowed extensions and validate the file
    allowed_extensions = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'mp4', 'mov', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'mp3', 'wav', 'avi', 'mkv', 'html', 'css', 'js', 'py', 'json', 'xml', 'csv']
    if not Validators.allowed_file(file.filename, allowed_extensions):
        if is_api_request:
            return jsonify({'error': 'File type not allowed'}), 400
        flash('File type not allowed')
        if folder_id:
            try:
                return redirect(url_for('folders_bp.dashboard', folder_id=int(folder_id)))
            except (ValueError, TypeError):
                return redirect(url_for('folders_bp.dashboard'))
        else:
            return redirect(url_for('folders_bp.dashboard'))
    
    if file:
        try:
            filename = secure_filename(file.filename)
            # This needs to be adjusted based on the app factory pattern
            upload_folder = Path.cwd() / 'FileFlow' / 'user_files'
            filepath = upload_folder / str(current_user.id) / filename
            
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            file.save(filepath)
            logger.info(f"File saved: {filepath}")
            
            # Get file size
            file_size = filepath.stat().st_size if filepath.exists() else 0
            
            # Get MIME type
            mimetype, _ = guess_type(filepath)
            if not mimetype:
                mimetype = 'application/octet-stream'
            
            # Convert folder_id to int if it exists
            parent_folder_id = None
            if folder_id:
                try:
                    parent_folder_id = int(folder_id)
                except (ValueError, TypeError):
                    parent_folder_id = None
            
            new_file = File(filename=filename, filepath=str(filepath), 
                            user_id=current_user.id, 
                            parent_folder_id=parent_folder_id,
                            filesize=file_size,
                            mimetype=mimetype)
            
            db.session.add(new_file)
            db.session.commit()
            logger.info(f"File record created: {new_file.id} - {filename}")
            
            if is_api_request:
                return jsonify({
                    'success': True,
                    'file': {
                        'id': new_file.id,
                        'name': new_file.filename,
                        'is_folder': False,
                        'size': file_size
                    }
                })
            
            flash('File uploaded successfully')
            if parent_folder_id:
                return redirect(url_for('folders_bp.dashboard', folder_id=parent_folder_id))
            else:
                return redirect(url_for('folders_bp.dashboard'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error uploading file: {str(e)}", exc_info=True)
            if is_api_request:
                return jsonify({'error': f'Upload failed: {str(e)}'}), 500
            flash(f'Error uploading file: {str(e)}')
            return redirect(url_for('folders_bp.dashboard'))
