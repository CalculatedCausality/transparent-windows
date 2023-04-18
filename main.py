import sys
import threading

import keyboard
import pystray
from PIL import Image

from hotkeys import register_hotkeys
from settings import clear_transparency_settings
from window_manager import monitor_active_window

# Load the icon for the system tray
icon_path = "icon.ico"
icon_image = Image.open(icon_path)


# Function to start the application
def start_app(icon, item):
    icon.stop()


# Function to clear all saved transparency settings
def clear_saved_transparency(icon, item):
    clear_transparency_settings()


# Create system tray icon menu
menu = (
    pystray.MenuItem('Clear Saved Transparency', clear_saved_transparency),
    pystray.MenuItem('Exit', sys.exit(0))
)

# Create system tray icon
tray_icon = pystray.Icon("transparent_windows",
                         icon_image, "Transparent Windows", menu)

# Register hotkeys
register_hotkeys()

# Start monitoring active window in a separate thread
monitor_thread = threading.Thread(target=monitor_active_window, daemon=True)
monitor_thread.start()

# Run the system tray icon
tray_icon.run()
