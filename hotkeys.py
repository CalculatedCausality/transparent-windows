import keyboard

from window_manager import set_transparency_level


# Function to register hotkeys
def register_hotkeys():
    for i in range(10):
        keyboard.add_hotkey(
            f"ctrl+alt+shift+{i}", set_transparency_level, args=(i,))
