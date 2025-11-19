from flask import Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from backend.models.database import db, File
from pathlib import Path
from backend.utils.validators import Validators

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('folders_bp.dashboard'))
    
    file = request.files['file']
    folder_id = request.form.get('folder_id')
    
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('folders_bp.dashboard'))

    # Define allowed extensions and validate the file
    allowed_extensions = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'mp4', 'mov']
    if not Validators.allowed_file(file.filename, allowed_extensions):
        flash('File type not allowed')
        return redirect(url_for('folders_bp.dashboard', folder_id=folder_id))
    
    if file:
        filename = secure_filename(file.filename)
        # This needs to be adjusted based on the app factory pattern
        upload_folder = Path.cwd() / 'FileFlow' / 'user_files'
        filepath = upload_folder / str(current_user.id) / filename
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        file.save(filepath)
        
        new_file = File(filename=filename, filepath=filepath, 
                        user_id=current_user.id, 
                        parent_folder_id=folder_id)
        
        db.session.add(new_file)
        db.session.commit()
        
        flash('File uploaded successfully')
        return redirect(url_for('folders_bp.dashboard', folder_id=folder_id))
