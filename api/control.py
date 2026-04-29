from flask import Blueprint, request, jsonify
import base64
import io
from PIL import Image, ImageDraw
import mss
import pyautogui
import logging
from utils.auth import require_auth, log_audit
from utils.api_utils import handle_errors, get_monitors_list

logger = logging.getLogger(__name__)
control_bp = Blueprint('control', __name__)

@control_bp.route('/monitors', methods=['GET'])
@require_auth
@handle_errors
def api_get_monitors():
    monitors = get_monitors_list()
    logger.info(f"Retrieved {len(monitors)} monitors for control")
    return jsonify(monitors)

@control_bp.route('/stream', methods=['POST'])
@require_auth
@handle_errors
def api_get_stream_frame():
    data = request.get_json()
    if not data:
        raise ValueError('Invalid JSON')

    monitor_id = int(data.get('monitor_id', 1))
    show_cursor = data.get('show_cursor', True)

    monitors = get_monitors_list()
    if not monitors:
        raise Exception('No monitors detected')

    monitor = next((m for m in monitors if m['id'] == monitor_id), None)
    if not monitor:
        raise ValueError(f'Monitor {monitor_id} not found')

    try:
        cursor_x, cursor_y = pyautogui.position()
    except Exception:
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
