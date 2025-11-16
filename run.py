from app import app
from tray import TrayIcon
from threading import Thread
import time
import socket
import subprocess

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def check_and_start_rbtray():
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq RBTray.exe'], capture_output=True, text=True, timeout=5)
        if 'RBTray.exe' not in result.stdout:
            subprocess.Popen(['RBTray.exe'])
            print("RBTray started.")
        else:
            print("RBTray already running.")
    except Exception as e:
        print(f"Error checking RBTray: {e}")

def run_tray():
    tray = TrayIcon()
    tray.run()

if __name__ == '__main__':
    check_and_start_rbtray()

    local_ip = get_local_ip()
    print("WebControl started on:")
    print("  Local: http://127.0.0.1:5000")
    print(f"  Network: http://{local_ip}:5000")
    print("  Default password: 123456789")
    print("  Press Ctrl+C to exit")
    print()

    # Start tray icon in background
    tray_thread = Thread(target=run_tray, daemon=True)
    tray_thread.start()

    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)