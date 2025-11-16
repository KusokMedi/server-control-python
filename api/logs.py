from flask import Blueprint, request, jsonify
import os
import logging
from utils.logger import log_action

logger = logging.getLogger(__name__)
logs_bp = Blueprint('logs', __name__)

LOG_FILE = 'logs/actions.log'

@logs_bp.route('/logs', methods=['GET'])
def get_logs():
    try:
        search = request.args.get('search', '').strip()
        level_filter = request.args.get('level', '').strip()
        limit = int(request.args.get('limit', 0))  # 0 means all
        offset = int(request.args.get('offset', 0))
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            # Reverse to show latest first
            lines = lines[::-1]
            if search:
                lines = [line for line in lines if search.lower() in line.lower()]
            if level_filter:
                lines = [line for line in lines if f' - {level_filter} - ' in line]
            total = len(lines)
            if limit > 0:
                lines = lines[offset:offset + limit]
            logger.info(f"Logs retrieved, search: '{search}', level: '{level_filter}', limit: {limit}, offset: {offset}, returned: {len(lines)}, total: {total}")
            return jsonify({'logs': [line.rstrip('\n\r') for line in lines], 'total': total})
        logger.warning("Log file not found")
        return jsonify({'logs': [], 'total': 0})
    except Exception as e:
        logger.error(f"Error reading logs: {e}")
        return jsonify({'error': 'Failed to read logs'}), 500

@logs_bp.route('/logs/download', methods=['GET'])
def download_logs():
    try:
        if os.path.exists(LOG_FILE):
            from flask import send_file
            logger.info("Logs downloaded")
            return send_file(LOG_FILE, as_attachment=True, download_name='actions.log')
        logger.warning("Log file not found for download")
        return jsonify({'error': 'Log file not found'}), 404
    except Exception as e:
        logger.error(f"Error downloading logs: {e}")
        return jsonify({'error': 'Failed to download logs'}), 500

@logs_bp.route('/logs/clear', methods=['POST'])
def clear_logs():
    try:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write('')
        log_action("Logs cleared by admin")
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error clearing logs: {e}")
        return jsonify({'error': 'Failed to clear logs'}), 500