from datetime import datetime, timedelta
import json
import time
from PyQt5.QtCore import QTimer

class TimeTracker:
    def __init__(self, storage):
        self.storage = storage
        self.start_time = None
        self.is_tracking = False
        self.last_activity = time.time()
        self.productive_apps = [
            'Visual Studio Code',
            'Code',
            'claude.ai',
            'Chrome',  # We'll check URL for productive sites
            'Safari',  # We'll check URL for productive sites
            'PyCharm',
            'Terminal'
        ]
        self.current_session = None
        self.daily_stats = {
            'total_system_time': 0,
            'inactive_time': 0,
            'browser_stats': {}  # Format: {'domain': total_seconds}
        }
        self.INACTIVE_THRESHOLD = 300  # 5 minutes of no activity

        # Setup activity monitoring
        self.activity_timer = QTimer()
        self.activity_timer.timeout.connect(self.check_activity)
        self.activity_timer.start(60000)  # Check every minute

    def update_activity(self):
        """Called when mouse or keyboard activity is detected"""
        self.last_activity = time.time()

    def check_activity(self):
        """Check if system is inactive"""
        current_time = time.time()
        if current_time - self.last_activity > self.INACTIVE_THRESHOLD:
            self.daily_stats['inactive_time'] += 60  # Add one minute to inactive time

        # Update total system time
        self.daily_stats['total_system_time'] += 60

        # Reset stats if it's a new day
        today = datetime.now().date()
        if not hasattr(self, 'last_reset_date') or self.last_reset_date != today:
            self.reset_daily_stats()
            self.last_reset_date = today

    def reset_daily_stats(self):
        self.daily_stats = {
            'total_system_time': 0,
            'inactive_time': 0,
            'browser_stats': {}
        }

    def update_browser_stats(self, url, duration):
        """Update time spent on specific websites"""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        if domain not in self.daily_stats['browser_stats']:
            self.daily_stats['browser_stats'][domain] = 0
        self.daily_stats['browser_stats'][domain] += duration

    def is_productive_app(self, app_name, window_title="", url=""):
        if app_name in self.productive_apps:
            # Special check for browsers
            if app_name in ['Chrome', 'Safari']:
                if url:  # If we have URL information
                    return 'claude.ai' in url.lower()
                return 'claude.ai' in window_title.lower()
            return True
        return False

    def handle_app_switch(self, app_name, window_title="", url=""):
        if self.is_productive_app(app_name, window_title, url):
            if not self.is_tracking:
                self.start()
        else:
            if self.is_tracking:
                self.stop()

        # Update activity timestamp
        self.update_activity()

        # Track browser activity if it's Chrome
        if app_name == 'Chrome' and url:
            self.update_browser_stats(url, 1)  # Add 1 second of activity

    def start(self):
        if not self.is_tracking:
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
            'sessions_today': sessions_today,
            'system_stats': {
                'total_time': self.daily_stats['total_system_time'],
                'inactive_time': self.daily_stats['inactive_time'],
                'active_time': self.daily_stats['total_system_time'] - self.daily_stats['inactive_time'],
                'browser_stats': self.daily_stats['browser_stats']
            }
        }