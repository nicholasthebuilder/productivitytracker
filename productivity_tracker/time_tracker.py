from datetime import datetime, timedelta
import json

class TimeTracker:
    def __init__(self, storage):
        self.storage = storage
        self.start_time = None
        self.is_tracking = False
    
    def start(self):
        self.start_time = datetime.now()
        self.is_tracking = True
    
    def stop(self):
        if not self.is_tracking:
            return
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        session = {
            'start': self.start_time.isoformat(),
            'end': end_time.isoformat(),
            'duration': duration
        }
        
        self.storage.save_session(session)
        self.is_tracking = False
        self.start_time = None
    
    def get_statistics(self):
        sessions = self.storage.load_sessions()
        today = datetime.now().date()
        
        total_seconds = 0
        today_seconds = 0
        sessions_today = 0
        
        for session in sessions:
            start_time = datetime.fromisoformat(session['start'])
            duration = session['duration']
            
            total_seconds += duration
            
            if start_time.date() == today:
                today_seconds += duration
                sessions_today += 1
        
        return {
            'total_seconds': total_seconds,
            'today_seconds': today_seconds,
            'sessions_today': sessions_today
        }
