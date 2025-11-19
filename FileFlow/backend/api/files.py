from flask import Blueprint, send_file, abort, jsonify, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from backend.models.database import db, File
from pathlib import Path

files_bp = Blueprint('files_bp', __name__)

@files_bp.route('/download_file/<int:file_id>')
@login_required
def download_file(file_id):
    try:
        file = File.query.get_or_404(file_id)
        
        if file.user_id != current_user.id:
            abort(403, description="You don't have permission to access this file")
            
        if not Path(file.filepath).exists():
            abort(404, description="File not found in storage")
            
        if file.is_folder:
            abort(400, description="Cannot download a folder")
            
        return send_file(
            file.filepath,
            as_attachment=True,
            download_name=secure_filename(file.filename)
        )
        
    except Exception as e:
        # app.logger.error(f"Error downloading file: {str(e)}")
        abort(500, description="Error occurred while downloading file")

@files_bp.route('/view_file/<int:file_id>')
@login_required
def view_file(file_id):
    try:
        file = File.query.get_or_404(file_id)
        
        if file.user_id != current_user.id:
            abort(403, description="You don't have permission to access this file")
            
        if not Path(file.filepath).exists():
            abort(404, description="File not found in storage")
            
        if file.is_folder:
            abort(400, description="Cannot view a folder")
            
        return send_file(
            file.filepath,
            as_attachment=False
        )
        
    except Exception as e:
        # app.logger.error(f"Error viewing file: {str(e)}")
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
                            if Path(item.filepath).exists():
                                Path(item.filepath).unlink()
                        except OSError as e:
                            # app.logger.error(f"Error deleting file {item.filepath}: {str(e)}")
                            pass
                    db.session.delete(item)
                
            delete_folder_contents(file.id)
        else:
            try:
                if Path(file.filepath).exists():
                    Path(file.filepath).unlink()
            except OSError as e:
                # app.logger.error(f"Error deleting file {file.filepath}: {str(e)}")
                pass
        
        db.session.delete(file)
        db.session.commit()
        return jsonify({'message': 'File deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        # app.logger.error(f"Error in delete_file: {str(e)}")
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
        abort(400)

    file_to_rename.filename = new_name
    db.session.commit()
    return jsonify({'success': True, 'new_name': new_name})

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
