import win32api
import win32con
import win32gui
import sys
import signal


def create_tray_icon():
    # Simple tray icon without complex menu
    try:
        # Create a simple window for tray
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = wnd_proc  # type: ignore
        wc.lpszClassName = "SimpleTray"  # type: ignore
        wc.hInstance = win32api.GetModuleHandle(None)  # type: ignore
        class_atom = win32gui.RegisterClass(wc)

        hwnd = win32gui.CreateWindow(class_atom, "SimpleTray", 0, 0, 0, 0,
                                     0, 0, 0, wc.hInstance, None)

        # Load default icon
        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        # Add to tray
        nid = (hwnd, 0,  # type: ignore
               win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
               win32con.WM_USER + 20, hicon, "WebControl")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)  # type: ignore

        print("Tray icon created. Double-click to open WebControl, "
              "Ctrl+C to exit.")

        # Message loop
        msg = win32gui.MSG()  # type: ignore
        while win32gui.GetMessage(msg, 0, 0, 0):  # type: ignore
            win32gui.TranslateMessage(msg)
            win32gui.DispatchMessage(msg)

    except Exception as e:
        print(f"Tray icon error: {e}")
        print("Running without tray icon...")


def wnd_proc(hwnd, msg, wparam, lparam):
    if msg == win32con.WM_USER + 20:
        if lparam == win32con.WM_LBUTTONDBLCLK:
            import webbrowser
            webbrowser.open('http://localhost:5000')
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)


if __name__ == '__main__':
    def signal_handler(sig, frame):
        print('Exiting WebControl...')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    create_tray_icon()


class TrayIcon:
    def run(self):
        create_tray_icon()
