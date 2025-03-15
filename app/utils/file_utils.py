import json
import os

CONFIG_FILE = "config.json"

def save_last_directory(directory):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"last_directory": directory}, f)

def load_last_directory():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get("last_directory", os.getcwd())
    return os.getcwd()