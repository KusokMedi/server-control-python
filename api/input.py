from flask import Blueprint, request, jsonify
import pyautogui
import logging
from utils.auth import require_auth, log_audit
from utils.api_utils import handle_errors

logger = logging.getLogger(__name__)
input_bp = Blueprint('input', __name__)

@input_bp.route('/input/mouse/position', methods=['GET'])
@require_auth
@handle_errors
def get_mouse_position():
    x, y = pyautogui.position()
    return jsonify({'x': x, 'y': y})

@input_bp.route('/input/mouse/move', methods=['POST'])
@require_auth
@handle_errors
def move_mouse():
    data = request.get_json()
    if not data or 'x' not in data or 'y' not in data:
        raise ValueError('Missing x or y coordinates')
    x = int(data['x'])
    y = int(data['y'])
    pyautogui.moveTo(x, y)
    logger.debug(f"Mouse moved to ({x}, {y})")
    return jsonify({'success': True})

@input_bp.route('/input/mouse/move_relative', methods=['POST'])
@require_auth
@handle_errors
def move_mouse_relative():
    data = request.get_json()
    if not data or 'dx' not in data or 'dy' not in data:
        raise ValueError('Missing dx or dy')
    dx = int(data['dx'])
    dy = int(data['dy'])
    pyautogui.moveRel(dx, dy)
    logger.debug(f"Mouse moved relatively by ({dx}, {dy})")
    return jsonify({'success': True})

@input_bp.route('/input/mouse/click', methods=['POST'])
@require_auth
@handle_errors
def click_mouse():
    data = request.get_json() or {}
    button = data.get('button', 'left')
    clicks = int(data.get('clicks', 1))
    if button not in ['left', 'right', 'middle']:
        raise ValueError('Invalid button')
    pyautogui.click(button=button, clicks=clicks)
    logger.debug(f"Mouse clicked {clicks} times with {button} button")
    log_audit('mouse_click', f'Button: {button}, Clicks: {clicks}')
    return jsonify({'success': True})

@input_bp.route('/input/mouse/scroll', methods=['POST'])
@require_auth
@handle_errors
def scroll_mouse():
    data = request.get_json() or {}
    clicks = int(data.get('clicks', 1))
    intensity = float(data.get('intensity', 1.0))
    total_clicks = int(clicks * intensity)
    pyautogui.scroll(total_clicks)
    logger.debug(f"Mouse scrolled {total_clicks} clicks")
    return jsonify({'success': True})

@input_bp.route('/input/keyboard/type', methods=['POST'])
@require_auth
@handle_errors
def type_text():
    data = request.get_json()
    if not data or 'text' not in data:
        raise ValueError('Missing text')
    text = str(data['text'])
    pyautogui.write(text, interval=0.01)
    logger.debug(f"Typed text (length: {len(text)})")
    log_audit('keyboard_type', f'Length: {len(text)} characters')
    return jsonify({'success': True})

@input_bp.route('/input/keyboard/press', methods=['POST'])
@require_auth
@handle_errors
def press_key():
    data = request.get_json()
    if not data or 'key' not in data:
        raise ValueError('Missing key')
    key = str(data['key'])
    pyautogui.press(key)
    logger.debug(f"Pressed key: {key}")
    log_audit('keyboard_press', f'Key: {key}')
    return jsonify({'success': True})