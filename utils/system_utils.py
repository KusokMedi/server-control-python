import psutil
import pyautogui
import os
import subprocess
import shutil
import logging
import platform

logger = logging.getLogger(__name__)

IS_WINDOWS = platform.system() == 'Windows'
IS_LINUX = platform.system() == 'Linux'

if IS_WINDOWS:
    import win32api
    import win32con
    import win32gui
    import win32clipboard

# File operations
def list_dir(path):
    try:
        if not os.path.exists(path):
            return []
        items = []
        for item in os.listdir(path):
            try:
                full_path = os.path.join(path, item)
                is_dir = os.path.isdir(full_path)
                size = os.path.getsize(full_path) if not is_dir else 0
                items.append({
                    'name': item,
                    'is_dir': is_dir,
                    'size': size,
                    'path': full_path
                })
            except (OSError, PermissionError) as e:
                logger.warning(f"Cannot access {item}: {e}")
                continue
        return sorted(items, key=lambda x: (not x['is_dir'], x['name'].lower()))
    except (OSError, PermissionError) as e:
        logger.error(f"Cannot list directory {path}: {e}")
        return []

def create_folder(path, name):
    try:
        new_path = os.path.join(path, name)
        os.makedirs(new_path)
        logger.info(f'Created folder: {new_path}')
        return True
    except Exception as e:
        logger.error(f"Failed to create folder {name} in {path}: {e}")
        return False

def delete_item(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        logger.info(f'Deleted item: {path}')
        return True
    except Exception as e:
        logger.error(f"Failed to delete {path}: {e}")
        return False

def rename_item(old_path, new_name):
    try:
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        os.rename(old_path, new_path)
        logger.info(f'Renamed: {old_path} -> {new_path}')
        return True
    except Exception as e:
        logger.error(f"Failed to rename {old_path}: {e}")
        return False

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read file {path}: {e}")
            return ''
    except Exception as e:
        logger.error(f"Failed to read file {path}: {e}")
        return ''

def write_file(path, content):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f'Wrote to file: {path}')
        return True
    except Exception as e:
        logger.error(f"Failed to write file {path}: {e}")
        return False

def run_file(path):
    try:
        process = subprocess.Popen([path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logger.info(f'Started process: {path} (PID: {process.pid})')
        return process.pid
    except Exception as e:
        logger.error(f"Failed to run file {path}: {e}")
        return None

# Processes
def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cpu_percent', 'memory_percent', 'num_threads']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'exe': proc.info['exe'],
                'cpu': proc.info['cpu_percent'],
                'memory': proc.info['memory_percent'],
                'threads': proc.info['num_threads']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            continue
    return processes

def kill_process(pid):
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        logger.info(f'Terminated process PID: {pid}')
        return True
    except psutil.NoSuchProcess:
        logger.warning(f"Process {pid} not found")
        return False
    except Exception as e:
        logger.error(f"Failed to kill process {pid}: {e}")
        return False

# Monitoring
def get_system_info():
    cpu = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    return {
        'cpu': cpu,
        'memory': memory.percent,
        'disk': disk.percent,
        'net_sent': net.bytes_sent,
        'net_recv': net.bytes_recv
    }

# Windows management (Windows only)
def get_windows():
    if not IS_WINDOWS:
        logger.warning("Window management is only available on Windows")
        return []
    
    windows = []
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                try:
                    rect = win32gui.GetWindowRect(hwnd)
                    windows.append({
                        'hwnd': hwnd,
                        'title': title,
                        'x': rect[0],
                        'y': rect[1],
                        'w': rect[2] - rect[0],
                        'h': rect[3] - rect[1]
                    })
                except Exception as e:
                    logger.warning(f"Cannot get window rect for {hwnd}: {e}")
    win32gui.EnumWindows(callback, windows)
    return windows

def hide_window(hwnd):
    if not IS_WINDOWS:
        raise NotImplementedError("Window management is only available on Windows")
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        logger.info(f'Hidden window HWND: {hwnd}')
    except Exception as e:
        logger.error(f"Failed to hide window {hwnd}: {e}")
        raise

def show_window(hwnd):
    if not IS_WINDOWS:
        raise NotImplementedError("Window management is only available on Windows")
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        logger.info(f'Shown window HWND: {hwnd}')
    except Exception as e:
        logger.error(f"Failed to show window {hwnd}: {e}")
        raise

def close_window(hwnd):
    if not IS_WINDOWS:
        raise NotImplementedError("Window management is only available on Windows")
    try:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        logger.info(f'Closed window HWND: {hwnd}')
    except Exception as e:
        logger.error(f"Failed to close window {hwnd}: {e}")
        raise

def minimize_window(hwnd):
    if not IS_WINDOWS:
        raise NotImplementedError("Window management is only available on Windows")
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        logger.info(f'Minimized window HWND: {hwnd}')
    except Exception as e:
        logger.error(f"Failed to minimize window {hwnd}: {e}")
        raise

def maximize_window(hwnd):
    if not IS_WINDOWS:
        raise NotImplementedError("Window management is only available on Windows")
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        logger.info(f'Maximized window HWND: {hwnd}')
    except Exception as e:
        logger.error(f"Failed to maximize window {hwnd}: {e}")
        raise

def restore_window(hwnd):
    if not IS_WINDOWS:
        raise NotImplementedError("Window management is only available on Windows")
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        logger.info(f'Restored window HWND: {hwnd}')
    except Exception as e:
        logger.error(f"Failed to restore window {hwnd}: {e}")
        raise

def move_window(hwnd, x, y):
    if not IS_WINDOWS:
        raise NotImplementedError("Window management is only available on Windows")
    try:
        win32gui.SetWindowPos(hwnd, None, x, y, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)
        logger.info(f'Moved window HWND: {hwnd} to ({x}, {y})')
    except Exception as e:
        logger.error(f"Failed to move window {hwnd}: {e}")
        raise

def resize_window(hwnd, w, h):
    if not IS_WINDOWS:
        raise NotImplementedError("Window management is only available on Windows")
    try:
        win32gui.SetWindowPos(hwnd, None, 0, 0, w, h, win32con.SWP_NOMOVE | win32con.SWP_NOZORDER)
        logger.info(f'Resized window HWND: {hwnd} to {w}x{h}')
    except Exception as e:
        logger.error(f"Failed to resize window {hwnd}: {e}")
        raise

def activate_window(hwnd):
    if not IS_WINDOWS:
        raise NotImplementedError("Window management is only available on Windows")
    try:
        win32gui.SetForegroundWindow(hwnd)
        logger.info(f'Activated window HWND: {hwnd}')
    except Exception as e:
        logger.error(f"Failed to activate window {hwnd}: {e}")
        raise

# Input (cross-platform via pyautogui)
def move_mouse(x, y):
    try:
        pyautogui.moveTo(x, y)
        logger.debug(f'Moved mouse to ({x}, {y})')
    except Exception as e:
        logger.error(f"Failed to move mouse: {e}")
        raise

def click_mouse(button='left', clicks=1):
    try:
        pyautogui.click(button=button, clicks=clicks)
        logger.debug(f'Clicked mouse: {button} {clicks} times')
    except Exception as e:
        logger.error(f"Failed to click mouse: {e}")
        raise

def scroll_mouse(clicks):
    try:
        pyautogui.scroll(clicks)
        logger.debug(f'Scrolled mouse: {clicks}')
    except Exception as e:
        logger.error(f"Failed to scroll mouse: {e}")
        raise

def press_key(key):
    try:
        pyautogui.press(key)
        logger.debug(f'Pressed key: {key}')
    except Exception as e:
        logger.error(f"Failed to press key: {e}")
        raise

def type_text(text):
    try:
        pyautogui.write(text, interval=0.01)
        logger.debug(f'Typed text (length: {len(text)})')
    except Exception as e:
        logger.error(f"Failed to type text: {e}")
        raise

# Clipboard (cross-platform via pyperclip)
def get_clipboard():
    try:
        import pyperclip
        return pyperclip.paste()
    except Exception as e:
        logger.error(f"Failed to get clipboard: {e}")
        return ''

def set_clipboard(text):
    try:
        import pyperclip
        pyperclip.copy(text)
        logger.debug('Set clipboard')
    except Exception as e:
        logger.error(f"Failed to set clipboard: {e}")
        raise

def clear_clipboard():
    try:
        import pyperclip
        pyperclip.copy('')
        logger.debug('Cleared clipboard')
    except Exception as e:
        logger.error(f"Failed to clear clipboard: {e}")
        raise