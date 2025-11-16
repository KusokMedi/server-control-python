from flask import Blueprint, request, jsonify, current_app
import pyautogui
import os
from screeninfo import get_monitors
from PIL import Image, ImageDraw
import mss
import logging

logger = logging.getLogger(__name__)
screenshots_bp = Blueprint('screenshots', __name__)

def get_monitors_list():
    """Получить список всех мониторов."""
    try:
        monitors = get_monitors()
        if not monitors:
            return []
        return [{'id': i + 1, 'name': f'Monitor {i + 1}', 'bounds': {'x': m.x, 'y': m.y, 'width': m.width, 'height': m.height}} for i, m in enumerate(monitors)]
    except Exception as e:
        raise Exception(f"Failed to get monitors: {str(e)}")

def find_monitor_by_cursor(cursor_x, cursor_y, monitors):
    """Найти монитор по координатам курсора."""
    for mon in monitors:
        if mon['bounds']['x'] <= cursor_x < mon['bounds']['x'] + mon['bounds']['width'] and mon['bounds']['y'] <= cursor_y < mon['bounds']['y'] + mon['bounds']['height']:
            return mon
    return None

def capture_screenshot(mode, monitor_id, show_cursor, cursor_style):
    """Создать скриншот в зависимости от режима и сохранить в файл."""
    try:
        monitors = get_monitors_list()
        if not monitors:
            raise Exception("No monitors detected")

        cursor_x, cursor_y = pyautogui.position()

        screenshot_dir = os.path.join(current_app.root_path, 'static', 'screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)

        paths = []

        with mss.mss() as sct:
            if mode == 'current':
                monitor = find_monitor_by_cursor(cursor_x, cursor_y, monitors)
                if not monitor:
                    raise Exception("Cursor not on any monitor")
                screenshot = sct.grab({
                    'left': monitor['bounds']['x'],
                    'top': monitor['bounds']['y'],
                    'width': monitor['bounds']['width'],
                    'height': monitor['bounds']['height']
                })
                img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
                # Координаты курсора относительно монитора
                rel_x = cursor_x - monitor['bounds']['x']
                rel_y = cursor_y - monitor['bounds']['y']

                # Добавить курсор
                if show_cursor and cursor_style == 'crosshair':
                    draw = ImageDraw.Draw(img)
                    size = 10  # Размер крестика
                    draw.line((rel_x - size, rel_y, rel_x + size, rel_y), fill='red', width=2)
                    draw.line((rel_x, rel_y - size, rel_x, rel_y + size), fill='red', width=2)

                img_path = os.path.join(screenshot_dir, 'screenshot.png')
                img.save(img_path, format='PNG')
                paths.append('/static/screenshots/screenshot.png')

            elif mode == 'all':
                # Отдельные скриншоты для каждого монитора
                for i, mon in enumerate(monitors):
                    shot = sct.grab({
                        'left': mon['bounds']['x'],
                        'top': mon['bounds']['y'],
                        'width': mon['bounds']['width'],
                        'height': mon['bounds']['height']
                    })
                    img = Image.frombytes('RGB', (shot.width, shot.height), shot.rgb)
                    # Координаты курсора абсолютные
                    rel_x = cursor_x - mon['bounds']['x']
                    rel_y = cursor_y - mon['bounds']['y']

                    # Добавить курсор
                    if show_cursor and cursor_style == 'crosshair':
                        draw = ImageDraw.Draw(img)
                        size = 10  # Размер крестика
                        draw.line((rel_x - size, rel_y, rel_x + size, rel_y), fill='red', width=2)
                        draw.line((rel_x, rel_y - size, rel_x, rel_y + size), fill='red', width=2)

                    img_path = os.path.join(screenshot_dir, f'screenshot_{i+1}.png')
                    img.save(img_path, format='PNG')
                    paths.append(f'/static/screenshots/screenshot_{i+1}.png')

            elif mode == 'selected':
                monitor = next((m for m in monitors if m['id'] == monitor_id), None)
                if not monitor:
                    raise Exception(f"Monitor with id {monitor_id} not found")
                screenshot = sct.grab({
                    'left': monitor['bounds']['x'],
                    'top': monitor['bounds']['y'],
                    'width': monitor['bounds']['width'],
                    'height': monitor['bounds']['height']
                })
                img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
                rel_x = cursor_x - monitor['bounds']['x']
                rel_y = cursor_y - monitor['bounds']['y']

                # Добавить курсор
                if show_cursor and cursor_style == 'crosshair':
                    draw = ImageDraw.Draw(img)
                    size = 10  # Размер крестика
                    draw.line((rel_x - size, rel_y, rel_x + size, rel_y), fill='red', width=2)
                    draw.line((rel_x, rel_y - size, rel_x, rel_y + size), fill='red', width=2)

                img_path = os.path.join(screenshot_dir, 'screenshot.png')
                img.save(img_path, format='PNG')
                paths.append('/static/screenshots/screenshot.png')

            else:
                raise Exception("Invalid mode")

            return paths

    except Exception as e:
        raise Exception(f"Screenshot failed: {str(e)}")

@screenshots_bp.route('/monitors', methods=['GET'])
def api_get_monitors():
    try:
        monitors = get_monitors_list()
        logger.info(f"Retrieved {len(monitors)} monitors")
        return jsonify(monitors)
    except Exception as e:
        logger.error(f"Error getting monitors: {e}")
        return jsonify({'error': 'Failed to get monitors'}), 500

@screenshots_bp.route('/screenshot', methods=['POST'])
def api_take_screenshot():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400

        mode = data.get('mode')
        if mode not in ['current', 'all', 'selected']:
            return jsonify({'error': 'Invalid mode. Allowed: current, all, selected'}), 400

        monitor_id = data.get('monitor_id')
        if mode == 'selected':
            if monitor_id is None or not isinstance(monitor_id, int):
                return jsonify({'error': 'monitor_id required and must be valid for mode=selected'}), 400
            monitors = get_monitors_list()
            if not any(m['id'] == monitor_id for m in monitors):
                return jsonify({'error': 'monitor_id required and must be valid for mode=selected'}), 400

        show_cursor = data.get('show_cursor', False)
        cursor_style = data.get('cursor_style', 'crosshair')
        if cursor_style != 'crosshair':
            return jsonify({'error': 'Invalid cursor_style. Only crosshair supported'}), 400

        img_paths = capture_screenshot(mode, monitor_id, show_cursor, cursor_style)
        logger.info(f"Screenshot taken in mode {mode}, paths: {img_paths}")
        return jsonify({'message': 'Screenshots saved successfully', 'paths': img_paths})

    except Exception as e:
        logger.error(f"Error taking screenshot: {e}")
        return jsonify({'error': 'Failed to take screenshot'}), 500
