from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt

class WindowManager:
    def __init__(self, time_tracker=None):
        self.time_tracker = time_tracker
        self.locked_window = None
        self.app = QApplication.instance() or QApplication([])
        self.setup_window_tracking()

    def setup_window_tracking(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_active_window)
        self.timer.start(1000)  # Check every second

    def check_active_window(self):
        if self.time_tracker:
            window = QApplication.activeWindow()
            if window:
                app_name = window.windowTitle()
                self.time_tracker.handle_app_switch(app_name)

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