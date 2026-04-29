from flask import Blueprint, request, jsonify
import os
import logging
from utils.auth import require_role, log_audit
from utils.models import AuditLog, db
from utils.api_utils import handle_errors

logger = logging.getLogger(__name__)
logs_bp = Blueprint('logs', __name__)

LOG_FILE = 'logs/app.log'

@logs_bp.route('/logs', methods=['GET'])
@require_role('admin')
@handle_errors
def get_logs():
    search = request.args.get('search', '').strip()
    level_filter = request.args.get('level', '').strip()
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        lines = lines[::-1]
        if search:
            lines = [line for line in lines if search.lower() in line.lower()]
        if level_filter:
            lines = [line for line in lines if f'[{level_filter}]' in line]
        total = len(lines)
        if limit > 0:
            lines = lines[offset:offset + limit]
        logger.info(f"Logs retrieved, returned: {len(lines)}, total: {total}")
        return jsonify({'logs': [line.rstrip('\n\r') for line in lines], 'total': total})
    logger.warning("Log file not found")
    return jsonify({'logs': [], 'total': 0})

@logs_bp.route('/logs/audit', methods=['GET'])
@require_role('admin')
@handle_errors
def get_audit_logs():
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))
    action_filter = request.args.get('action', '').strip()
    user_id = request.args.get('user_id', None)
    
    query = AuditLog.query
    if action_filter:
        query = query.filter(AuditLog.action.like(f'%{action_filter}%'))
    if user_id:
        query = query.filter_by(user_id=int(user_id))
    
    total = query.count()
    logs = query.order_by(AuditLog.timestamp.desc()).offset(offset).limit(limit).all()
    
    return jsonify({
        'logs': [log.to_dict() for log in logs],
        'total': total
    })

@logs_bp.route('/logs/download', methods=['GET'])
@require_role('admin')
@handle_errors
def download_logs():
    if os.path.exists(LOG_FILE):
        from flask import send_file
        logger.info("Logs downloaded")
        log_audit('logs_downloaded', 'Application logs downloaded')
        return send_file(LOG_FILE, as_attachment=True, download_name='app.log')
    raise FileNotFoundError('Log file not found')

@logs_bp.route('/logs/clear', methods=['POST'])
@require_role('admin')
@handle_errors
def clear_logs():
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write('')
    log_audit('logs_cleared', 'Application logs cleared')
    return jsonify({'success': True})