from flask import Blueprint, request, jsonify
from utils.models import db, User
from utils.auth import require_role, log_audit, get_current_user
from utils.api_utils import handle_errors
import logging

logger = logging.getLogger(__name__)
users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
@require_role('admin')
def list_users():
    """Список всех пользователей"""
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        return jsonify({'error': 'Failed to list users'}), 500

@users_bp.route('/users', methods=['POST'])
@require_role('admin')
def create_user():
    """Создать нового пользователя"""
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing username or password'}), 400
        
        username = data['username'].strip()
        password = data['password']
        role = data.get('role', 'user')
        
        if not username or len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        if role not in ['admin', 'user']:
            return jsonify({'error': 'Invalid role'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'User already exists'}), 400
        
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        log_audit('user_created', f'User {username} created with role {role}')
        logger.info(f"User {username} created")
        
        return jsonify(user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating user: {e}")
        return jsonify({'error': 'Failed to create user'}), 500

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@require_role('admin')
def update_user(user_id):
    """Обновить пользователя"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        current_user = get_current_user()
        if user.id == current_user.id and 'role' in data:
            return jsonify({'error': 'Cannot change own role'}), 400
        
        if 'password' in data and data['password']:
            if len(data['password']) < 6:
                return jsonify({'error': 'Password must be at least 6 characters'}), 400
            user.set_password(data['password'])
            log_audit('user_password_changed', f'Password changed for user {user.username}')
        
        if 'role' in data:
            if data['role'] not in ['admin', 'user']:
                return jsonify({'error': 'Invalid role'}), 400
            old_role = user.role
            user.role = data['role']
            log_audit('user_role_changed', f'Role changed for user {user.username} from {old_role} to {user.role}')
        
        if 'is_active' in data:
            if user.id == current_user.id:
                return jsonify({'error': 'Cannot deactivate yourself'}), 400
            user.is_active = bool(data['is_active'])
            log_audit('user_status_changed', f'User {user.username} {"activated" if user.is_active else "deactivated"}')
        
        if 'language' in data:
            if data['language'] not in ['ru', 'en']:
                return jsonify({'error': 'Invalid language'}), 400
            user.language = data['language']
            log_audit('user_language_changed', f'Language changed for user {user.username} to {user.language}')
        
        db.session.commit()
        logger.info(f"User {user.username} updated")
        
        return jsonify(user.to_dict())
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating user: {e}")
        return jsonify({'error': 'Failed to update user'}), 500

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@require_role('admin')
def delete_user(user_id):
    """Удалить пользователя"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        current_user = get_current_user()
        if user.id == current_user.id:
            return jsonify({'error': 'Cannot delete yourself'}), 400
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        log_audit('user_deleted', f'User {username} deleted')
        logger.info(f"User {username} deleted")
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting user: {e}")
        return jsonify({'error': 'Failed to delete user'}), 500

@users_bp.route('/users/me', methods=['GET'])
def get_current_user_info():
    """Получить информацию о текущем пользователе"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(user.to_dict())
