import json
import os

# Constants
TRANSPARENCY_SETTINGS_FILE = "transparency_settings.json"


# Function to load transparency settings from file
def load_transparency_settings():
    if os.path.exists(TRANSPARENCY_SETTINGS_FILE):
        with open(TRANSPARENCY_SETTINGS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}


# Function to save transparency settings to file
def save_transparency_settings(transparency_settings):
    with open(TRANSPARENCY_SETTINGS_FILE, "w") as f:
        json.dump(transparency_settings, f)


# Function to clear all saved transparency settings
def clear_transparency_settings():
    if os.path.exists(TRANSPARENCY_SETTINGS_FILE):
        os.remove(TRANSPARENCY_SETTINGS_FILE)
