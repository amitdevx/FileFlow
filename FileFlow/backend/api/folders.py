from flask import Blueprint, request, flash, redirect, url_for, render_template, abort, jsonify
from flask_login import login_required, current_user
try:
    from backend.models.database import db, File
except ImportError:
    from models.database import db, File

folders_bp = Blueprint('folders_bp', __name__)

@folders_bp.route('/dashboard')
@folders_bp.route('/dashboard/<int:folder_id>')
@login_required
def dashboard(folder_id=None):
    user_files = File.query.filter_by(user_id=current_user.id, parent_folder_id=folder_id).all()
    
    breadcrumbs = []
    if folder_id:
        current_folder = File.query.get_or_404(folder_id)
        folder = current_folder
        while folder:
            breadcrumbs.append({'id': folder.id, 'name': folder.filename})
            folder = File.query.get(folder.parent_folder_id) if folder.parent_folder_id else None
        breadcrumbs.reverse()

    return render_template('dashboard.html', files=user_files, breadcrumbs=breadcrumbs, current_folder_id=folder_id)

@folders_bp.route('/create_folder', methods=['POST'])
@login_required
def create_folder():
    # Check if request is JSON (from React) or form data (from HTML form)
    if request.is_json:
        data = request.get_json()
        folder_name = data.get('folder_name')
        parent_folder_id = data.get('parent_folder_id')
    else:
        folder_name = request.form.get('folder_name')
        parent_folder_id = request.form.get('parent_folder_id')
    
    if not folder_name:
        if request.is_json:
            return jsonify({'error': 'Folder name is required'}), 400
        flash('Folder name is required')
        return redirect(url_for('folders_bp.dashboard', folder_id=parent_folder_id))
    
    new_folder = File(filename=folder_name, 
                      filepath='', 
                      user_id=current_user.id, 
                      is_folder=True, 
                      parent_folder_id=parent_folder_id if parent_folder_id else None)
    
    db.session.add(new_folder)
    db.session.commit()
    
    if request.is_json:
        return jsonify({
            'success': True,
            'folder': {
                'id': new_folder.id,
                'name': new_folder.filename,
                'is_folder': True
            }
        })
    
    flash('Folder created successfully')
    return redirect(url_for('folders_bp.dashboard', folder_id=parent_folder_id))
