from flask import Flask, jsonify
from flask_login import LoginManager
from flask_compress import Compress
try:
    from backend.models.database import db, User, bcrypt
    from backend.config import Config
except ImportError:
    from models.database import db, User, bcrypt
    from config import Config
from pathlib import Path
import logging

# Initialize Flask app
app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend',
            static_url_path='/static')
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = Path(__file__).parent / app.config['UPLOAD_FOLDER']

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize compression for faster downloads
Compress(app)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Template filters
@app.template_filter('format_filesize')
def format_filesize(size):
    """Format file size in human-readable format."""
    try:
        size = int(size)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    except (ValueError, TypeError):
        return "0 B"



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
    from backend.api.compression import compression_bp
except ImportError:
    from api.auth import auth_bp
    from api.files import files_bp
    from api.folders import folders_bp
    from api.search import search_bp
    from api.upload import upload_bp
    from api.compression import compression_bp

app.register_blueprint(files_bp)
app.register_blueprint(folders_bp)
app.register_blueprint(search_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(compression_bp)

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