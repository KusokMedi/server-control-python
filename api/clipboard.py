from flask import Blueprint, request, jsonify
import pyperclip
import logging

logger = logging.getLogger(__name__)
clipboard_bp = Blueprint('clipboard', __name__)

@clipboard_bp.route('/clipboard/read', methods=['GET'])
def read_clipboard():
    try:
        text = pyperclip.paste()
        logger.info("Clipboard read")
        return jsonify({'text': text})
    except Exception as e:
        logger.error(f"Error reading clipboard: {e}")
        return jsonify({'error': 'Failed to read clipboard'}), 500

@clipboard_bp.route('/clipboard/write', methods=['POST'])
def write_clipboard():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text'}), 400
        text = str(data['text'])
        pyperclip.copy(text)
        logger.info(f"Clipboard written: {text[:50]}{'...' if len(text) > 50 else ''}")
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error writing to clipboard: {e}")
        return jsonify({'error': 'Failed to write to clipboard'}), 500

@clipboard_bp.route('/clipboard/clear', methods=['POST'])
def clear_clipboard():
    try:
        pyperclip.copy('')
        logger.info("Clipboard cleared")
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error clearing clipboard: {e}")
        return jsonify({'error': 'Failed to clear clipboard'}), 500