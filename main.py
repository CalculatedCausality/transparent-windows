import time
import threading
import ctypes
import keyboard
import json
import os
import sys
import pygetwindow as gw
import win32gui

# Set the working directory to the script's location
script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(script_directory)

# Define constants
TRANSPARENCY_SETTINGS_FILE = "transparency_settings.json"
MIN_TRANSPARENCY = int(0.1 * 255)  # 10% transparency
MAX_TRANSPARENCY = 255

# Load transparency settings from file
if os.path.exists(TRANSPARENCY_SETTINGS_FILE):
    with open(TRANSPARENCY_SETTINGS_FILE, "r") as f:
        transparency_settings = json.load(f)
else:
    transparency_settings = {}

# Function to set window transparency


def set_window_transparency(hwnd, transparency):
    ctypes.windll.user32.SetWindowLongW(
        hwnd, -20, ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x80000)
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, transparency, 0x2)

# Function to get the currently active window's hwnd


def get_active_window_hwnd():
    return ctypes.windll.user32.GetForegroundWindow()

# Function to save transparency settings


def save_settings():
    with open(TRANSPARENCY_SETTINGS_FILE, "w") as f:
        json.dump(transparency_settings, f)

# Hotkey action


def set_transparency_level(level):
    hwnd = get_active_window_hwnd()
    window_title = gw.getWindowsWithTitle(gw.getActiveWindowTitle())[0].title
    if level == 0:
        transparency = MAX_TRANSPARENCY
    else:
        transparency = int(MAX_TRANSPARENCY * (level / 10))
    set_window_transparency(hwnd, transparency)
    transparency_settings[window_title] = transparency
    save_settings()  # Save settings automatically after changing transparency


# Set hotkeys
for i in range(10):
    keyboard.add_hotkey(
        f"ctrl+alt+shift+{i}", set_transparency_level, args=(i,))


# Function to monitor active window and restore transparency
def monitor_active_window():
    last_hwnd = None
    while True:
        hwnd = get_active_window_hwnd()
        if hwnd != last_hwnd:
            last_hwnd = hwnd
            windows = gw.getWindowsWithTitle(gw.getActiveWindowTitle())
            if windows:  # Check if the list is not empty
                window_title = windows[0].title
                transparency = transparency_settings.get(window_title)
                if transparency is not None:
                    set_window_transparency(hwnd, transparency)
        time.sleep(0.1)


# Start monitoring active window in a separate thread
monitor_thread = threading.Thread(target=monitor_active_window, daemon=True)
monitor_thread.start()

# Keep the script running
keyboard.wait()
