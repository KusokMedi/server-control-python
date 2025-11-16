from flask import Blueprint, request, jsonify
import win32gui
import win32con
import logging

logger = logging.getLogger(__name__)
windows_bp = Blueprint('windows', __name__)

def enum_windows_callback(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title:
            windows.append({
                'hwnd': hwnd,
                'title': title,
                'class': win32gui.GetClassName(hwnd)
            })

@windows_bp.route('/windows', methods=['GET'])
def list_windows():
    try:
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        logger.info(f"Listed {len(windows)} windows")
        return jsonify(windows)
    except Exception as e:
        logger.error(f"Error listing windows: {e}")
        return jsonify({'error': 'Failed to list windows'}), 500

@windows_bp.route('/windows/hide', methods=['POST'])
def hide_window():
    try:
        data = request.get_json()
        if not data or 'hwnd' not in data:
            return jsonify({'error': 'Missing hwnd'}), 400
        hwnd = int(data['hwnd'])
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        logger.info(f"Window {hwnd} hidden")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'error': 'Invalid hwnd'}), 400
    except Exception as e:
        logger.error(f"Error hiding window {hwnd}: {e}")
        return jsonify({'error': 'Failed to hide window'}), 500

@windows_bp.route('/windows/show', methods=['POST'])
def show_window():
    try:
        data = request.get_json()
        if not data or 'hwnd' not in data:
            return jsonify({'error': 'Missing hwnd'}), 400
        hwnd = int(data['hwnd'])
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        logger.info(f"Window {hwnd} shown")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'error': 'Invalid hwnd'}), 400
    except Exception as e:
        logger.error(f"Error showing window {hwnd}: {e}")
        return jsonify({'error': 'Failed to show window'}), 500

@windows_bp.route('/windows/minimize', methods=['POST'])
def minimize_window():
    try:
        data = request.get_json()
        if not data or 'hwnd' not in data:
            return jsonify({'error': 'Missing hwnd'}), 400
        hwnd = int(data['hwnd'])
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        logger.info(f"Window {hwnd} minimized")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'error': 'Invalid hwnd'}), 400
    except Exception as e:
        logger.error(f"Error minimizing window {hwnd}: {e}")
        return jsonify({'error': 'Failed to minimize window'}), 500

@windows_bp.route('/windows/maximize', methods=['POST'])
def maximize_window():
    try:
        data = request.get_json()
        if not data or 'hwnd' not in data:
            return jsonify({'error': 'Missing hwnd'}), 400
        hwnd = int(data['hwnd'])
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        logger.info(f"Window {hwnd} maximized")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'error': 'Invalid hwnd'}), 400
    except Exception as e:
        logger.error(f"Error maximizing window {hwnd}: {e}")
        return jsonify({'error': 'Failed to maximize window'}), 500

@windows_bp.route('/windows/restore', methods=['POST'])
def restore_window():
    try:
        data = request.get_json()
        if not data or 'hwnd' not in data:
            return jsonify({'error': 'Missing hwnd'}), 400
        hwnd = int(data['hwnd'])
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        logger.info(f"Window {hwnd} restored")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'error': 'Invalid hwnd'}), 400
    except Exception as e:
        logger.error(f"Error restoring window {hwnd}: {e}")
        return jsonify({'error': 'Failed to restore window'}), 500

@windows_bp.route('/windows/move', methods=['POST'])
def move_window():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['hwnd', 'x', 'y', 'width', 'height']):
            return jsonify({'error': 'Missing required fields'}), 400
        hwnd = int(data['hwnd'])
        x = int(data['x'])
        y = int(data['y'])
        width = int(data['width'])
        height = int(data['height'])
        win32gui.MoveWindow(hwnd, x, y, width, height, True)
        logger.info(f"Window {hwnd} moved to ({x}, {y}) size {width}x{height}")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'error': 'Invalid parameters'}), 400
    except Exception as e:
        logger.error(f"Error moving window {hwnd}: {e}")
        return jsonify({'error': 'Failed to move window'}), 500

@windows_bp.route('/windows/focus', methods=['POST'])
def focus_window():
    try:
        data = request.get_json()
        if not data or 'hwnd' not in data:
            return jsonify({'error': 'Missing hwnd'}), 400
        hwnd = int(data['hwnd'])
        win32gui.SetForegroundWindow(hwnd)
        logger.info(f"Window {hwnd} focused")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'error': 'Invalid hwnd'}), 400
    except Exception as e:
        logger.error(f"Error focusing window {hwnd}: {e}")
        return jsonify({'error': 'Failed to focus window'}), 500

@windows_bp.route('/windows/close', methods=['POST'])
def close_window():
    try:
        data = request.get_json()
        if not data or 'hwnd' not in data:
            return jsonify({'error': 'Missing hwnd'}), 400
        hwnd = int(data['hwnd'])
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        logger.info(f"Window {hwnd} closed")
        return jsonify({'success': True})
    except ValueError:
        return jsonify({'error': 'Invalid hwnd'}), 400
    except Exception as e:
        logger.error(f"Error closing window {hwnd}: {e}")
        return jsonify({'error': 'Failed to close window'}), 500