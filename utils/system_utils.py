import psutil
import win32api
import win32con
import win32gui
import win32process
import win32clipboard
import pyautogui
import os
import subprocess
import threading
import time
from PIL import ImageGrab
import requests
from utils.logger import log_action

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
            except (OSError, PermissionError):
                continue  # Skip inaccessible items
        return sorted(items, key=lambda x: (not x['is_dir'], x['name'].lower()))
    except (OSError, PermissionError):
        return []

def create_folder(path, name):
    try:
        os.makedirs(os.path.join(path, name))
        log_action('Create folder', f'{os.path.join(path, name)}')
        return True
    except:
        return False

def delete_item(path):
    try:
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)
        log_action('Delete item', path)
        return True
    except:
        return False

def rename_item(old_path, new_name):
    try:
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        os.rename(old_path, new_path)
        log_action('Rename item', f'{old_path} -> {new_path}')
        return True
    except:
        return False

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ''

def write_file(path, content):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        log_action('Edit file', path)
        return True
    except:
        return False

def run_file(path):
    try:
        process = subprocess.Popen([path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        log_action('Run file', path)
        return process.pid
    except:
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
        except:
            pass
    return processes

def kill_process(pid):
    try:
        psutil.Process(pid).terminate()
        log_action('Kill process', f'PID: {pid}')
        return True
    except:
        return False

# Monitoring
def get_system_info():
    cpu = psutil.cpu_percent(interval=1)
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

def get_ips():
    try:
        internal = psutil.net_if_addrs()['Ethernet'][0].address if 'Ethernet' in psutil.net_if_addrs() else 'N/A'
        external = requests.get('https://api.ipify.org').text
    except:
        internal = 'N/A'
        external = 'N/A'
    return {'internal': internal, 'external': external}

# Windows
def get_windows():
    windows = []
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                rect = win32gui.GetWindowRect(hwnd)
                windows.append({
                    'hwnd': hwnd,
                    'title': title,
                    'x': rect[0],
                    'y': rect[1],
                    'w': rect[2] - rect[0],
                    'h': rect[3] - rect[1]
                })
    win32gui.EnumWindows(callback, windows)
    return windows

def hide_window(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    log_action('Hide window', f'HWND: {hwnd}')

def show_window(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    log_action('Show window', f'HWND: {hwnd}')

def close_window(hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    log_action('Close window', f'HWND: {hwnd}')

def minimize_window(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    log_action('Minimize window', f'HWND: {hwnd}')

def maximize_window(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    log_action('Maximize window', f'HWND: {hwnd}')

def restore_window(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    log_action('Restore window', f'HWND: {hwnd}')

def move_window(hwnd, x, y):
    win32gui.SetWindowPos(hwnd, None, x, y, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)
    log_action('Move window', f'HWND: {hwnd} to ({x}, {y})')

def resize_window(hwnd, w, h):
    win32gui.SetWindowPos(hwnd, None, 0, 0, w, h, win32con.SWP_NOMOVE | win32con.SWP_NOZORDER)
    log_action('Resize window', f'HWND: {hwnd} to {w}x{h}')

def activate_window(hwnd):
    win32gui.SetForegroundWindow(hwnd)
    log_action('Activate window', f'HWND: {hwnd}')

# Input
def move_mouse(x, y):
    pyautogui.moveTo(x, y)
    log_action('Move mouse', f'to ({x}, {y})')

def click_mouse(button='left', clicks=1):
    pyautogui.click(button=button, clicks=clicks)
    log_action('Click mouse', f'{button} {clicks} times')

def scroll_mouse(x, y, clicks):
    pyautogui.scroll(clicks, x, y)
    log_action('Scroll mouse', f'at ({x}, {y}) {clicks}')

def press_key(key):
    pyautogui.press(key)
    log_action('Press key', key)

def type_text(text):
    pyautogui.typewrite(text)
    log_action('Type text', text)

# Screenshots
def take_screenshot():
    img = ImageGrab.grab()
    path = f'static/screenshots/screenshot_{int(time.time())}.png'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    log_action('Screenshot', 'full screen')
    return path

def take_monitor_screenshot(monitor):
    try:
        import screeninfo
        monitors = screeninfo.get_monitors()
        if monitor < len(monitors):
            m = monitors[monitor]
            img = ImageGrab.grab(bbox=(m.x, m.y, m.x + m.width, m.y + m.height))
            path = f'static/screenshots/monitor_{monitor}_{int(time.time())}.png'
            os.makedirs(os.path.dirname(path), exist_ok=True)
            img.save(path)
            log_action('Screenshot', f'monitor {monitor}')
            return path
    except ImportError:
        # Fallback to full screen if screeninfo not available
        return take_screenshot()
    return None

# Clipboard
def get_clipboard():
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData(win32con.CF_TEXT).decode('utf-8')
    except:
        data = ''
    win32clipboard.CloseClipboard()
    return data

def set_clipboard(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_TEXT, text.encode('utf-8'))
    win32clipboard.CloseClipboard()
    log_action('Set clipboard', text)

def clear_clipboard():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()
    log_action('Clear clipboard')

# Virtual consoles
running_processes = {}

def start_process_console(path):
    pid = run_file(path)
    if pid:
        running_processes[pid] = {'process': psutil.Process(pid), 'output': []}
    return pid

def get_process_output(pid):
    if pid in running_processes:
        proc = running_processes[pid]['process']
        try:
            output = proc.stdout.read()
            if output:
                running_processes[pid]['output'].append(output)
        except:
            pass
        return '\n'.join(running_processes[pid]['output'])
    return ''

def stop_process_console(pid):
    if pid in running_processes:
        running_processes[pid]['process'].terminate()
        del running_processes[pid]
        log_action('Stop console', f'PID: {pid}')