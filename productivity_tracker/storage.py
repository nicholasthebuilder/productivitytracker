import json
import os
from pathlib import Path

class Storage:
    def __init__(self):
        self.data_dir = Path.home() / '.productivity_tracker'
        self.sessions_file = self.data_dir / 'sessions.json'
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        self.data_dir.mkdir(exist_ok=True)
        if not self.sessions_file.exists():
            self.sessions_file.write_text('[]')
    
    def save_session(self, session):
        sessions = self.load_sessions()
        sessions.append(session)
        
        with open(self.sessions_file, 'w') as f:
            json.dump(sessions, f, indent=2)
    
    def load_sessions(self):
        try:
            with open(self.sessions_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
