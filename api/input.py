from flask import Blueprint, request, jsonify
import pyautogui
import logging

logger = logging.getLogger(__name__)
input_bp = Blueprint('input', __name__)

@input_bp.route('/input/mouse/position', methods=['GET'])
def get_mouse_position():
    try:
        x, y = pyautogui.position()
        return jsonify({'x': x, 'y': y})
    except Exception as e:
        logger.error(f"Error getting mouse position: {e}")
        return jsonify({'error': 'Failed to get mouse position'}), 500

@input_bp.route('/input/mouse/move', methods=['POST'])
def move_mouse():
    try:
        data = request.get_json()
        if not data or 'x' not in data or 'y' not in data:
            return jsonify({'error': 'Missing x or y coordinates'}), 400
        x = int(data['x'])
        y = int(data['y'])
        pyautogui.moveTo(x, y)
        logger.info(f"Mouse moved to ({x}, {y})")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'error': 'Invalid coordinates'}), 400
    except Exception as e:
        logger.error(f"Error moving mouse: {e}")
        return jsonify({'error': 'Failed to move mouse'}), 500

@input_bp.route('/input/mouse/move_relative', methods=['POST'])
def move_mouse_relative():
    try:
        data = request.get_json()
        if not data or 'dx' not in data or 'dy' not in data:
            return jsonify({'error': 'Missing dx or dy'}), 400
        dx = int(data['dx'])
        dy = int(data['dy'])
        pyautogui.moveRel(dx, dy)
        logger.info(f"Mouse moved relatively by ({dx}, {dy})")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'error': 'Invalid relative coordinates'}), 400
    except Exception as e:
        logger.error(f"Error moving mouse relatively: {e}")
        return jsonify({'error': 'Failed to move mouse relatively'}), 500

@input_bp.route('/input/mouse/click', methods=['POST'])
def click_mouse():
    try:
        data = request.get_json()
        if not data:
            data = {}
        button = data.get('button', 'left')
        clicks = int(data.get('clicks', 1))
        if button not in ['left', 'right', 'middle']:
            return jsonify({'error': 'Invalid button'}), 400
        pyautogui.click(button=button, clicks=clicks)
        logger.info(f"Mouse clicked {clicks} times with {button} button")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'error': 'Invalid clicks count'}), 400
    except Exception as e:
        logger.error(f"Error clicking mouse: {e}")
        return jsonify({'error': 'Failed to click mouse'}), 500

@input_bp.route('/input/mouse/scroll', methods=['POST'])
def scroll_mouse():
    try:
        data = request.get_json()
        if not data:
            data = {}
        clicks = int(data.get('clicks', 1))
        intensity = float(data.get('intensity', 1.0))
        total_clicks = int(clicks * intensity)
        pyautogui.scroll(total_clicks)
        logger.info(f"Mouse scrolled {total_clicks} clicks")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'error': 'Invalid scroll parameters'}), 400
    except Exception as e:
        logger.error(f"Error scrolling mouse: {e}")
        return jsonify({'error': 'Failed to scroll mouse'}), 500

@input_bp.route('/input/keyboard/type', methods=['POST'])
def type_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text'}), 400
        text = str(data['text'])
        pyautogui.typewrite(text)
        logger.info(f"Typed text: {text[:50]}{'...' if len(text) > 50 else ''}")
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error typing text: {e}")
        return jsonify({'error': 'Failed to type text'}), 500

@input_bp.route('/input/keyboard/press', methods=['POST'])
def press_key():
    try:
        data = request.get_json()
        if not data or 'key' not in data:
            return jsonify({'error': 'Missing key'}), 400
        key = str(data['key'])
        pyautogui.press(key)
        logger.info(f"Pressed key: {key}")
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error pressing key: {e}")
        return jsonify({'error': 'Failed to press key'}), 500