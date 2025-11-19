from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
try:
    from backend.models.database import db, User, File, bcrypt
    from backend.config import Config
except ImportError:
    from models.database import db, User, File, bcrypt
    from config import Config
from pathlib import Path
import os
import logging

# Initialize Flask app
app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend')
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = Path(__file__).parent / app.config['UPLOAD_FOLDER']

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route handlers
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
@app.route('/dashboard/<int:folder_id>')
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

@app.route('/download_file/<int:file_id>')
@login_required
def download_file(file_id):
    try:
        file = File.query.get_or_404(file_id)
        
        if file.user_id != current_user.id:
            abort(403, description="You don't have permission to access this file")
        
        if not os.path.exists(file.filepath):
            abort(404, description="File not found in storage")
        
        if file.is_folder:
            abort(400, description="Cannot download a folder")
        
        return send_file(
            file.filepath,
            as_attachment=True,
            download_name=secure_filename(file.filename)
        )
        
    except Exception as e:
        app.logger.error(f"Error downloading file: {str(e)}")
        abort(500, description="Error occurred while downloading file")

@app.route('/view_file/<int:file_id>')
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
        app.logger.error(f"Error viewing file: {str(e)}")
        abort(500, description="Error occurred while viewing file")

@app.route('/delete_file/<int:file_id>', methods=['DELETE'])
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
                            app.logger.error(f"Error deleting file {item.filepath}: {str(e)}")
                    db.session.delete(item)
                
            delete_folder_contents(file.id)
        else:
            try:
                if Path(file.filepath).exists():
                    Path(file.filepath).unlink()
            except OSError as e:
                app.logger.error(f"Error deleting file {file.filepath}: {str(e)}")
        
        db.session.delete(file)
        db.session.commit()
        return jsonify({'message': 'File deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error in delete_file: {str(e)}")
        return jsonify({'error': 'Failed to delete file'}), 500

@app.route('/folder/<int:folder_id>')
@login_required
def open_folder(folder_id):
    try:
        folder = File.query.get_or_404(folder_id)
        
        if folder.user_id != current_user.id:
            abort(403, description="You don't have permission to access this folder")
            
        if not folder.is_folder:
            abort(400, description="Specified ID is not a folder")
        
        contents = File.query.filter_by(parent_folder_id=folder_id).order_by(
            File.is_folder.desc(),
            File.filename
        ).all()
        
        folder_path = []
        current = folder
        while current:
            folder_path.insert(0, current)
            if current.parent_folder_id:
                current = File.query.get(current.parent_folder_id)
            else:
                break
        
        return render_template('dashboard.html', 
                             files=contents, 
                             current_folder=folder,
                             folder_path=folder_path)
                             
    except Exception as e:
        app.logger.error(f"Error in open_folder: {str(e)}")
        abort(500, description="Error occurred while opening folder")

from datetime import datetime

# ... (rest of the imports)

# ... (rest of the code)

@app.route('/create_folder', methods=['POST'])
@login_required
def create_folder():
    folder_name = request.form['folder_name']
    parent_folder_id = request.form.get('parent_folder_id')
    
    new_folder = File(filename=folder_name, 
                      filepath='', 
                      user_id=current_user.id, 
                      is_folder=True, 
                      parent_folder_id=parent_folder_id)
    
    db.session.add(new_folder)
    db.session.commit()
    
    flash('Folder created successfully')
    return redirect(url_for('folders_bp.dashboard'))

@app.route('/move_file/<int:file_id>', methods=['POST'])
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

try:
    from backend.services.compression_service import CompressionService
except ImportError:
    from services.compression_service import CompressionService

@app.route('/archive', methods=['POST'])
@login_required
def archive_files():
    data = request.get_json()
    file_ids = data.get('file_ids')
    
    files_to_archive = []
    for file_id in file_ids:
        file = File.query.get_or_404(file_id)
        if file.user_id != current_user.id:
            abort(403)
        files_to_archive.append(file.filepath)
        
    archive_name = "archive.zip"
    CompressionService.create_zip(files_to_archive, archive_name)
    
    return send_file(archive_name, as_attachment=True)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': str(error.description)}), 404

@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({'error': str(error.description)}), 403

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': str(error.description)}), 400

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': str(error.description)}), 500

def init_db():
    db.create_all()

@app.cli.command('init-db')
def init_db_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

try:
    from backend.api.auth import auth_bp
    from backend.api.files import files_bp
    from backend.api.folders import folders_bp
    from backend.api.search import search_bp
    from backend.api.upload import upload_bp
except ImportError:
    from api.auth import auth_bp
    from api.files import files_bp
    from api.folders import folders_bp
    from api.search import search_bp
    from api.upload import upload_bp

app.register_blueprint(files_bp)
app.register_blueprint(folders_bp)
app.register_blueprint(search_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(auth_bp)

import threading
try:
    from backend.services.watcher_service import start_watching
except ImportError:
    from services.watcher_service import start_watching

if __name__ == '__main__':
    watch_thread = threading.Thread(target=start_watching, args=(app.config['UPLOAD_FOLDER'],))
    watch_thread.daemon = True
    watch_thread.start()
    app.run(debug=True)