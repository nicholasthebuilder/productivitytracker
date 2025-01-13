from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt5.QtCore import QTimer
from datetime import datetime, timedelta
from .time_tracker import TimeTracker
from .window_manager import WindowManager
from .storage import Storage

class ProductivityApp:
    def __init__(self):
        self.app = QApplication.instance() or QApplication([])

        # Initialize components
        self.storage = Storage()
        self.time_tracker = TimeTracker(self.storage)
        self.window_manager = WindowManager(time_tracker=self.time_tracker)

        # Create system tray icon
        self.tray = QSystemTrayIcon()
        self.create_menu()
        self.tray.setIcon(self.create_icon(True))
        self.tray.show()

        # State
        self.is_tracking = True
        self.window_locked = False

    def create_icon(self, active):
        from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
        pixmap = QPixmap(22, 22)
        pixmap.fill(QColor(0, 0, 0, 0))
        painter = QPainter(pixmap)
        color = QColor("green") if active else QColor("gray")
        painter.setBrush(color)
        painter.drawEllipse(6, 6, 10, 10)
        painter.end()
        return QIcon(pixmap)

    def create_menu(self):
        menu = QMenu()

        self.timer_action = menu.addAction("Auto-tracking Active")
        self.timer_action.triggered.connect(self.toggle_timer)

        self.lock_action = menu.addAction("Lock Window")
        self.lock_action.triggered.connect(self.toggle_window_lock)

        menu.addSeparator()

        stats_action = menu.addAction("Show Statistics")
        stats_action.triggered.connect(self.show_stats)

        self.tray.setContextMenu(menu)

    def toggle_timer(self):
        self.is_tracking = not self.is_tracking
        if self.is_tracking:
            self.timer_action.setText("Auto-tracking Active")
            self.tray.setIcon(self.create_icon(True))
        else:
            self.time_tracker.stop()
            self.timer_action.setText("Auto-tracking Disabled")
            self.tray.setIcon(self.create_icon(False))

    def toggle_window_lock(self):
        self.window_locked = not self.window_locked
        if self.window_locked:
            self.window_manager.lock_current_window()
            self.lock_action.setText("Unlock Window")
        else:
            self.window_manager.unlock_current_window()
            self.lock_action.setText("Lock Window")

    def show_stats(self):
        stats = self.time_tracker.get_statistics()
        total_time = timedelta(seconds=stats['total_seconds'])
        today_time = timedelta(seconds=stats['today_seconds'])

        message = (
            f"Total tracked time: {total_time}\n"
            f"Today's tracked time: {today_time}\n"
            f"Sessions today: {stats['sessions_today']}"
        )
        self.tray.showMessage(
            "Productivity Statistics",
            message,
            QSystemTrayIcon.Information,
            5000
        )

    def run(self):
        self.app.exec_()