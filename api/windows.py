from flask import Blueprint, request, jsonify
import logging
import platform
from utils.auth import require_auth, log_audit
from utils.api_utils import handle_errors

logger = logging.getLogger(__name__)
windows_bp = Blueprint('windows', __name__)

IS_WINDOWS = platform.system() == 'Windows'

if IS_WINDOWS:
    import win32gui
    import win32con

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
@require_auth
@handle_errors
def list_windows():
    if not IS_WINDOWS:
        return jsonify({'error': 'Window management is only available on Windows', 'windows': []})
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    logger.info(f"Listed {len(windows)} windows")
    return jsonify(windows)

@windows_bp.route('/windows/hide', methods=['POST'])
@require_auth
@handle_errors
def hide_window():
    if not IS_WINDOWS:
        raise NotImplementedError('Window management is only available on Windows')
    
    data = request.get_json()
    if not data or 'hwnd' not in data:
        raise ValueError('Missing hwnd')
    hwnd = int(data['hwnd'])
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    logger.info(f"Window {hwnd} hidden")
    log_audit('window_hidden', f'HWND: {hwnd}')
    return jsonify({'success': True})

@windows_bp.route('/windows/show', methods=['POST'])
@require_auth
@handle_errors
def show_window():
    if not IS_WINDOWS:
        raise NotImplementedError('Window management is only available on Windows')
    
    data = request.get_json()
    if not data or 'hwnd' not in data:
        raise ValueError('Missing hwnd')
    hwnd = int(data['hwnd'])
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    logger.info(f"Window {hwnd} shown")
    log_audit('window_shown', f'HWND: {hwnd}')
    return jsonify({'success': True})

@windows_bp.route('/windows/minimize', methods=['POST'])
@require_auth
@handle_errors
def minimize_window():
    if not IS_WINDOWS:
        raise NotImplementedError('Window management is only available on Windows')
    
    data = request.get_json()
    if not data or 'hwnd' not in data:
        raise ValueError('Missing hwnd')
    hwnd = int(data['hwnd'])
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    logger.info(f"Window {hwnd} minimized")
    log_audit('window_minimized', f'HWND: {hwnd}')
    return jsonify({'success': True})

@windows_bp.route('/windows/maximize', methods=['POST'])
@require_auth
@handle_errors
def maximize_window():
    if not IS_WINDOWS:
        raise NotImplementedError('Window management is only available on Windows')
    
    data = request.get_json()
    if not data or 'hwnd' not in data:
        raise ValueError('Missing hwnd')
    hwnd = int(data['hwnd'])
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    logger.info(f"Window {hwnd} maximized")
    log_audit('window_maximized', f'HWND: {hwnd}')
    return jsonify({'success': True})

@windows_bp.route('/windows/restore', methods=['POST'])
@require_auth
@handle_errors
def restore_window():
    if not IS_WINDOWS:
        raise NotImplementedError('Window management is only available on Windows')
    
    data = request.get_json()
    if not data or 'hwnd' not in data:
        raise ValueError('Missing hwnd')
    hwnd = int(data['hwnd'])
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    logger.info(f"Window {hwnd} restored")
    log_audit('window_restored', f'HWND: {hwnd}')
    return jsonify({'success': True})

@windows_bp.route('/windows/move', methods=['POST'])
@require_auth
@handle_errors
def move_window():
    if not IS_WINDOWS:
        raise NotImplementedError('Window management is only available on Windows')
    
    data = request.get_json()
    if not data or not all(k in data for k in ['hwnd', 'x', 'y', 'width', 'height']):
        raise ValueError('Missing required fields')
    hwnd = int(data['hwnd'])
    x = int(data['x'])
    y = int(data['y'])
    width = int(data['width'])
    height = int(data['height'])
    win32gui.MoveWindow(hwnd, x, y, width, height, True)
    logger.info(f"Window {hwnd} moved to ({x}, {y}) size {width}x{height}")
    log_audit('window_moved', f'HWND: {hwnd}, Position: ({x}, {y}), Size: {width}x{height}')
    return jsonify({'success': True})

@windows_bp.route('/windows/focus', methods=['POST'])
@require_auth
@handle_errors
def focus_window():
    if not IS_WINDOWS:
        raise NotImplementedError('Window management is only available on Windows')
    
    data = request.get_json()
    if not data or 'hwnd' not in data:
        raise ValueError('Missing hwnd')
    hwnd = int(data['hwnd'])
    win32gui.SetForegroundWindow(hwnd)
    logger.info(f"Window {hwnd} focused")
    log_audit('window_focused', f'HWND: {hwnd}')
    return jsonify({'success': True})

@windows_bp.route('/windows/close', methods=['POST'])
@require_auth
@handle_errors
def close_window():
    if not IS_WINDOWS:
        raise NotImplementedError('Window management is only available on Windows')
    
    data = request.get_json()
    if not data or 'hwnd' not in data:
        raise ValueError('Missing hwnd')
    hwnd = int(data['hwnd'])
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    logger.info(f"Window {hwnd} closed")
    log_audit('window_closed', f'HWND: {hwnd}')
    return jsonify({'success': True})