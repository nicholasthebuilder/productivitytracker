from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
import psutil
import time

class WindowManager:
    def __init__(self, time_tracker=None):
        self.time_tracker = time_tracker
        self.locked_window = None
        self.app = QApplication.instance() or QApplication([])
        self.last_mouse_pos = None
        self.last_activity_time = time.time()
        self.setup_window_tracking()

    def setup_window_tracking(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_active_window)
        self.timer.start(1000)  # Check every second

        # Setup mouse/keyboard tracking
        self.activity_timer = QTimer()
        self.activity_timer.timeout.connect(self.check_system_activity)
        self.activity_timer.start(1000)  # Check every second

    def check_system_activity(self):
        """Check for mouse and keyboard activity"""
        current_pos = QApplication.desktop().cursor().pos()

        # Check if mouse has moved
        if self.last_mouse_pos != current_pos:
            self.last_mouse_pos = current_pos
            self.update_activity()

        # Note: Keyboard activity is checked through window focus changes

    def update_activity(self):
        """Update the last activity timestamp"""
        self.last_activity_time = time.time()
        if self.time_tracker:
            self.time_tracker.update_activity()

    def get_chrome_url(self):
        """Attempt to get the current Chrome URL"""
        # This is a placeholder - in a real implementation, 
        # we would need to use browser-specific APIs or automation
        return ""

    def check_active_window(self):
        if self.time_tracker:
            window = QApplication.activeWindow()
            if window:
                app_name = window.windowTitle()
                url = ""

                # If it's Chrome, try to get the current URL
                if "Chrome" in app_name:
                    url = self.get_chrome_url()

                self.time_tracker.handle_app_switch(app_name, window.windowTitle(), url)
                self.update_activity()

    def lock_current_window(self):
        window = QApplication.activeWindow()
        if window:
            self.locked_window = window
            window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
            window.show()

    def unlock_current_window(self):
        if self.locked_window:
            self.locked_window.setWindowFlags(self.locked_window.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.locked_window.show()
            self.locked_window = None