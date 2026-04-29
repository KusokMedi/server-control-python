from flask import Blueprint, request, jsonify
import pyperclip
import logging
from utils.auth import require_auth, log_audit
from utils.api_utils import handle_errors

logger = logging.getLogger(__name__)
clipboard_bp = Blueprint('clipboard', __name__)

@clipboard_bp.route('/clipboard/read', methods=['GET'])
@require_auth
@handle_errors
def read_clipboard():
    text = pyperclip.paste()
    logger.debug("Clipboard read")
    return jsonify({'text': text})

@clipboard_bp.route('/clipboard/write', methods=['POST'])
@require_auth
@handle_errors
def write_clipboard():
    data = request.get_json()
    if not data or 'text' not in data:
        raise ValueError('Missing text')
    text = str(data['text'])
    pyperclip.copy(text)
    logger.debug(f"Clipboard written (length: {len(text)})")
    log_audit('clipboard_write', f'Length: {len(text)} characters')
    return jsonify({'success': True})

@clipboard_bp.route('/clipboard/clear', methods=['POST'])
@require_auth
@handle_errors
def clear_clipboard():
    pyperclip.copy('')
    logger.debug("Clipboard cleared")
    log_audit('clipboard_clear', 'Clipboard cleared')
    return jsonify({'success': True})