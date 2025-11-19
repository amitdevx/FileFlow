from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from backend.models.database import db, File, SearchProfile
from sqlalchemy import or_, and_
from datetime import datetime

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/api/search', methods=['POST'])
@login_required
def search_files():
    """Advanced file search"""
    data = request.get_json()
    query = data.get('query', '')
    file_types = data.get('file_types', [])
    size_min = data.get('size_min')
    size_max = data.get('size_max')
    date_from = data.get('date_from')
    date_to = data.get('date_to')
    
    # Base query
    search_query = File.query.filter_by(user_id=current_user.id)
    
    # Text search
    if query:
        search_query = search_query.filter(
            or_(
                File.filename.ilike(f'%{query}%'),
                File.tags.ilike(f'%{query}%')
            )
        )
    
    # File type filter
    if file_types:
        type_conditions = [File.mimetype.ilike(f'{ft}%') for ft in file_types]
        search_query = search_query.filter(or_(*type_conditions))
    
    # Size filter
    if size_min is not None:
        search_query = search_query.filter(File.filesize >= size_min)
    if size_max is not None:
        search_query = search_query.filter(File.filesize <= size_max)
    
    # Date filter
    if date_from:
        search_query = search_query.filter(File.created_at >= datetime.fromisoformat(date_from))
    if date_to:
        search_query = search_query.filter(File.created_at <= datetime.fromisoformat(date_to))
    
    results = search_query.all()
    return jsonify([file.to_dict() for file in results])

@search_bp.route('/api/search/profiles', methods=['GET'])
@login_required
def get_search_profiles():
    """Get saved search profiles"""
    profiles = SearchProfile.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'query': p.query,
        'file_types': p.file_types.split(',') if p.file_types else [],
        'size_min': p.size_min,
        'size_max': p.size_max,
        'date_from': p.date_from.isoformat() if p.date_from else None,
        'date_to': p.date_to.isoformat() if p.date_to else None
    } for p in profiles])

@search_bp.route('/api/search/profiles', methods=['POST'])
@login_required
def save_search_profile():
    """Save a search profile"""
    data = request.get_json()
    
    profile = SearchProfile(
        name=data['name'],
        user_id=current_user.id,
        query=data.get('query'),
        file_types=','.join(data.get('file_types', [])),
        size_min=data.get('size_min'),
        size_max=data.get('size_max'),
        date_from=datetime.fromisoformat(data['date_from']) if data.get('date_from') else None,
        date_to=datetime.fromisoformat(data['date_to']) if data.get('date_to') else None
    )
    
    db.session.add(profile)
    db.session.commit()
    
    return jsonify({'success': True, 'id': profile.id})

@search_bp.route('/api/search/profiles/<int:profile_id>', methods=['DELETE'])
@login_required
def delete_search_profile(profile_id):
    """Delete a search profile"""
    profile = SearchProfile.query.get_or_404(profile_id)
    if profile.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(profile)
    db.session.commit()
    
    return jsonify({'success': True})
