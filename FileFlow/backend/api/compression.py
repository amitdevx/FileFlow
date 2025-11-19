from flask import Blueprint, request, jsonify, send_file
from flask_login import login_required, current_user
try:
    from backend.services.compression_service import CompressionService
    from backend.models.database import db, File
except ImportError:
    from services.compression_service import CompressionService
    from models.database import db, File
from pathlib import Path

compression_bp = Blueprint('compression_bp', __name__)

@compression_bp.route('/api/compress/create', methods=['POST'])
@login_required
def create_archive():
    """Create a compressed archive"""
    data = request.get_json()
    file_ids = data.get('file_ids', [])
    archive_name = data.get('archive_name', 'archive')
    format_type = data.get('format', 'zip')  # zip, tar, 7z
    password = data.get('password')
    
    # Get file paths
    files = File.query.filter(File.id.in_(file_ids), File.user_id == current_user.id).all()
    file_paths = [f.filepath for f in files if not f.is_folder]
    
    if not file_paths:
        return jsonify({'error': 'No valid files selected'}), 400
    
    # Create output path
    output_dir = Path('FileFlow/user_files') / str(current_user.id)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{archive_name}.{format_type}"
    
    try:
        if format_type == 'zip':
            CompressionService.create_zip(file_paths, str(output_path), password)
        elif format_type in ['tar', 'tar.gz', 'tar.bz2']:
            compression = format_type.split('.')[-1] if '.' in format_type else None
            CompressionService.create_tar(file_paths, str(output_path), compression)
        elif format_type == '7z':
            CompressionService.create_7z(file_paths, str(output_path), password)
        else:
            return jsonify({'error': 'Unsupported format'}), 400
        
        # Add to database
        new_file = File(
            filename=f"{archive_name}.{format_type}",
            filepath=str(output_path),
            user_id=current_user.id,
            filesize=output_path.stat().st_size,
            mimetype='application/zip' if format_type == 'zip' else 'application/x-tar'
        )
        db.session.add(new_file)
        db.session.commit()
        
        return jsonify({'success': True, 'file_id': new_file.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@compression_bp.route('/api/compress/extract/<int:file_id>', methods=['POST'])
@login_required
def extract_archive(file_id):
    """Extract a compressed archive"""
    file = File.query.get_or_404(file_id)
    
    if file.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    password = data.get('password')
    
    # Create extraction directory
    extract_dir = Path(file.filepath).parent / Path(file.filepath).stem
    extract_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        ext = Path(file.filepath).suffix.lower()
        
        if ext == '.zip':
            CompressionService.extract_zip(file.filepath, str(extract_dir), password)
        elif ext in ['.tar', '.gz', '.bz2', '.xz']:
            CompressionService.extract_tar(file.filepath, str(extract_dir))
        elif ext == '.7z':
            CompressionService.extract_7z(file.filepath, str(extract_dir), password)
        else:
            return jsonify({'error': 'Unsupported archive format'}), 400
        
        # Add extracted folder to database
        folder = File(
            filename=Path(file.filepath).stem,
            filepath=str(extract_dir),
            user_id=current_user.id,
            is_folder=True,
            parent_folder_id=file.parent_folder_id
        )
        db.session.add(folder)
        db.session.commit()
        
        return jsonify({'success': True, 'folder_id': folder.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@compression_bp.route('/api/compress/list/<int:file_id>', methods=['GET'])
@login_required
def list_archive_contents(file_id):
    """List contents of an archive"""
    file = File.query.get_or_404(file_id)
    
    if file.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        contents = CompressionService.list_archive_contents(file.filepath)
        return jsonify({'success': True, 'contents': contents})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
