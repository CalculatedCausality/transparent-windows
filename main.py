import ctypes
import keyboard
import json
import os
import pygetwindow as gw

# Define constants
TRANSPARENCY_SETTINGS_FILE = "transparency_settings.json"
TRANSPARENCY_STEP = 25
MIN_TRANSPARENCY = 0
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

# Hotkey actions


def increase_transparency():
    hwnd = get_active_window_hwnd()
    window_title = gw.getWindowsWithTitle(gw.getActiveWindowTitle())[0].title
    current_transparency = transparency_settings.get(window_title, 255)
    new_transparency = max(
        MIN_TRANSPARENCY, current_transparency - TRANSPARENCY_STEP)
    set_window_transparency(hwnd, new_transparency)
    transparency_settings[window_title] = new_transparency


def decrease_transparency():
    hwnd = get_active_window_hwnd()
    window_title = gw.getWindowsWithTitle(gw.getActiveWindowTitle())[0].title
    current_transparency = transparency_settings.get(window_title, 255)
    new_transparency = min(
        MAX_TRANSPARENCY, current_transparency + TRANSPARENCY_STEP)
    set_window_transparency(hwnd, new_transparency)
    transparency_settings[window_title] = new_transparency


# Set hotkeys
keyboard.add_hotkey("ctrl+alt+up", increase_transparency)
keyboard.add_hotkey("ctrl+alt+down", decrease_transparency)

# Save transparency settings on exit


def save_settings():
    with open(TRANSPARENCY_SETTINGS_FILE, "w") as f:
        json.dump(transparency_settings, f)


keyboard.add_hotkey("ctrl+alt+q", save_settings)  # Save settings and exit

# Restore window transparency
for window_title, transparency in transparency_settings.items():
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        set_window_transparency(windows[0].hwnd, transparency)

# Keep the script running
keyboard.wait()
