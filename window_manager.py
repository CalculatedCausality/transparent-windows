import ctypes
import time
import psutil
from settings import load_transparency_settings, save_transparency_settings

# Constants
MIN_TRANSPARENCY = int(0.1 * 255)  # 10% transparency
MAX_TRANSPARENCY = 255

# Function to set window transparency


def set_window_transparency(hwnd, transparency):
    ctypes.windll.user32.SetWindowLongW(
        hwnd, -20, ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x80000)
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, transparency, 0x2)

# Function to get the currently active window's hwnd


def get_active_window_hwnd():
    return ctypes.windll.user32.GetForegroundWindow()

# Function to get the application ID and process name for a window


def get_application_info(hwnd):
    process_id = ctypes.c_ulong()
    ctypes.windll.user32.GetWindowThreadProcessId(
        hwnd, ctypes.byref(process_id))
    process = psutil.Process(process_id.value)
    process_name = process.name()
    return process_id.value, process_name

# Function to set transparency level


def set_transparency_level(level):
    hwnd = get_active_window_hwnd()
    app_id, process_name = get_application_info(hwnd)
    if level == 0:
        transparency = MAX_TRANSPARENCY
    else:
        transparency = int(MAX_TRANSPARENCY * (level / 10))
    set_window_transparency(hwnd, transparency)

    transparency_settings = load_transparency_settings()
    app_key = f"{process_name}-{app_id}"
    transparency_settings[app_key] = transparency
    save_transparency_settings(transparency_settings)

# Function to monitor active window and restore transparency


def monitor_active_window():
    last_hwnd = None
    while True:
        hwnd = get_active_window_hwnd()
        if hwnd != last_hwnd:
            last_hwnd = hwnd
            app_id, process_name = get_application_info(hwnd)
            app_key = f"{process_name}-{app_id}"
            transparency_settings = load_transparency_settings()

            if app_key in transparency_settings:
                set_window_transparency(hwnd, transparency_settings[app_key])

        time.sleep(0.1)
