import ctypes
import keyboard
import json
import os
import pygetwindow as gw

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

# Hotkey action


def set_transparency_level(level):
    hwnd = get_active_window_hwnd()
    window_title = gw.getWindowsWithTitle(gw.getActiveWindowTitle())[0].title
    transparency = int(MAX_TRANSPARENCY * (level / 10))
    if level == 0:
        transparency = MIN_TRANSPARENCY
    set_window_transparency(hwnd, transparency)
    transparency_settings[window_title] = transparency


# Set hotkeys
for i in range(10):
    keyboard.add_hotkey(
        f"ctrl+alt+shift+{i}", set_transparency_level, args=(i,))

# Save transparency settings on exit


def save_settings():
    with open(TRANSPARENCY_SETTINGS_FILE, "w") as f:
        json.dump(transparency_settings, f)


# Save settings and exit
keyboard.add_hotkey("ctrl+alt+shift+q", save_settings)

# Restore window transparency
for window_title, transparency in transparency_settings.items():
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        set_window_transparency(windows[0].hwnd, transparency)

# Keep the script running
keyboard.wait()
