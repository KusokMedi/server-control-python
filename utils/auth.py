from functools import wraps
from flask import session, redirect, url_for, jsonify, request
from utils.models import User, AuditLog, db
from datetime import datetime

def get_current_user():
    """Получить текущего пользователя из сессии"""
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

def require_auth(f):
    """Декоратор для проверки аутентификации"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or not user.is_active:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def require_role(role):
    """Декоратор для проверки роли пользователя"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user or not user.is_active:
                if request.is_json or request.path.startswith('/api/'):
                    return jsonify({'error': 'Unauthorized'}), 401
                return redirect(url_for('login'))
            if user.role != role:
                if request.is_json or request.path.startswith('/api/'):
                    return jsonify({'error': 'Forbidden'}), 403
                return jsonify({'error': 'Access denied'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def log_audit(action, details=None, user_id=None):
    """Записать действие в audit log"""
    try:
        if user_id is None:
            user = get_current_user()
            user_id = user.id if user else None
        
        log = AuditLog(
            user_id=user_id,
            action=action,
            details=details,
            ip_address=request.remote_addr if request else None
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Failed to log audit: {e}")

def login_user(user):
    """Войти в систему"""
    session['user_id'] = user.id
    session.permanent = True
    user.last_login = datetime.utcnow()
    db.session.commit()
    log_audit('login', f'User {user.username} logged in', user.id)

def logout_user():
    """Выйти из системы"""
    user = get_current_user()
    if user:
        log_audit('logout', f'User {user.username} logged out', user.id)
    session.pop('user_id', None)
