from flask import Blueprint, request, jsonify, current_app
import base64
import io
from PIL import Image, ImageDraw
import mss
import pyautogui
from screeninfo import get_monitors
import logging
from utils.logger import log_action

logger = logging.getLogger(__name__)
control_bp = Blueprint('control', __name__)

def get_monitors_list():
    """Получить список всех мониторов."""
    try:
        monitors = get_monitors()
        if not monitors:
            return []
        return [{'id': i + 1, 'name': f'Monitor {i + 1}', 'bounds': {'x': m.x, 'y': m.y, 'width': m.width, 'height': m.height}} for i, m in enumerate(monitors)]
    except Exception as e:
        raise Exception(f"Failed to get monitors: {str(e)}")

@control_bp.route('/monitors', methods=['GET'])
def api_get_monitors():
    try:
        monitors = get_monitors_list()
        logger.info(f"Retrieved {len(monitors)} monitors for control")
        log_action(f"Retrieved {len(monitors)} monitors for control")
        return jsonify(monitors)
    except Exception as e:
        logger.error(f"Error getting monitors for control: {e}")
        return jsonify({'error': 'Failed to get monitors'}), 500

@control_bp.route('/stream', methods=['POST'])
def api_get_stream_frame():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400

        monitor_id = int(data.get('monitor_id', 1))
        show_cursor = data.get('show_cursor', True)

        monitors = get_monitors_list()
        if not monitors:
            return jsonify({'error': 'No monitors detected'}), 400

        monitor = next((m for m in monitors if m['id'] == monitor_id), None)
        if not monitor:
            return jsonify({'error': f'Monitor {monitor_id} not found'}), 400

        try:
            cursor_x, cursor_y = pyautogui.position()
        except Exception as e:
            cursor_x, cursor_y = 0, 0

        with mss.mss() as sct:
            screenshot = sct.grab({
                'left': monitor['bounds']['x'],
                'top': monitor['bounds']['y'],
                'width': monitor['bounds']['width'],
                'height': monitor['bounds']['height']
            })
            img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)

            if show_cursor:
                rel_x = cursor_x - monitor['bounds']['x']
                rel_y = cursor_y - monitor['bounds']['y']
                if 0 <= rel_x < img.width and 0 <= rel_y < img.height:
                    draw = ImageDraw.Draw(img)
                    size = 10
                    draw.line((rel_x - size, rel_y, rel_x + size, rel_y), fill='red', width=2)
                    draw.line((rel_x, rel_y - size, rel_x, rel_y + size), fill='red', width=2)

            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=80)
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            return jsonify({
                'image': f'data:image/jpeg;base64,{img_base64}',
                'width': img.width,
                'height': img.height
            })

    except Exception as e:
        logger.error(f"Error getting stream frame: {e}")
        return jsonify({'error': f'Failed to get stream frame: {str(e)}'}), 500
