from functools import wraps
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def handle_errors(f):
    """Декоратор для обработки ошибок в API"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error in {f.__name__}: {e}")
            return jsonify({'error': str(e)}), 400
        except PermissionError as e:
            logger.warning(f"Permission error in {f.__name__}: {e}")
            return jsonify({'error': 'Permission denied'}), 403
        except FileNotFoundError as e:
            logger.warning(f"Not found in {f.__name__}: {e}")
            return jsonify({'error': 'Resource not found'}), 404
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {e}", exc_info=True)
            return jsonify({'error': 'Internal server error'}), 500
    return decorated_function

def validate_json(*required_fields):
    """Декоратор для валидации JSON данных"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data provided'}), 400
            
            missing = [field for field in required_fields if field not in data]
            if missing:
                return jsonify({'error': f'Missing required fields: {", ".join(missing)}'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_monitors_list():
    """Получить список всех мониторов (общая функция)"""
    try:
        from screeninfo import get_monitors
        monitors = get_monitors()
        if not monitors:
            return []
        return [{
            'id': i + 1,
            'name': f'Monitor {i + 1}',
            'bounds': {
                'x': m.x,
                'y': m.y,
                'width': m.width,
                'height': m.height
            }
        } for i, m in enumerate(monitors)]
    except Exception as e:
        logger.error(f"Failed to get monitors: {e}")
        raise Exception(f"Failed to get monitors: {str(e)}")
