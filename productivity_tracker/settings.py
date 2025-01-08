import json
from pathlib import Path

class Settings:
    def __init__(self):
        self.settings_file = Path.home() / '.productivity_tracker' / 'settings.json'
        self.defaults = {
            'start_minimized': True,
            'show_notifications': True,
            'auto_lock_windows': False
        }
        self._load()
    
    def _load(self):
        try:
            with open(self.settings_file, 'r') as f:
                self._settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._settings = self.defaults.copy()
            self._save()
    
    def _save(self):
        self.settings_file.parent.mkdir(exist_ok=True)
        with open(self.settings_file, 'w') as f:
            json.dump(self._settings, f, indent=2)
    
    def get(self, key, default=None):
        return self._settings.get(key, default)
    
    def set(self, key, value):
        self._settings[key] = value
        self._save()
