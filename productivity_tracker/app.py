import rumps
from datetime import datetime, timedelta
from .time_tracker import TimeTracker
from .window_manager import WindowManager
from .storage import Storage
from .icons import ICON_ACTIVE, ICON_INACTIVE

class ProductivityApp(rumps.App):
    def __init__(self):
        super().__init__("Productivity", icon=ICON_INACTIVE)

        # Initialize components
        self.storage = Storage()
        self.time_tracker = TimeTracker(self.storage)
        self.window_manager = WindowManager(time_tracker=self.time_tracker)

        # Setup menu items
        self.timer_button = rumps.MenuItem("Auto-tracking Active", callback=self.toggle_timer)
        self.lock_window_button = rumps.MenuItem("Lock Window", callback=self.toggle_window_lock)
        self.stats_button = rumps.MenuItem("Show Statistics", callback=self.show_stats)

        # Add menu items
        self.menu = [
            self.timer_button,
            self.lock_window_button,
            None,  # Separator
            self.stats_button
        ]

        # State
        self.is_tracking = True  # Start with auto-tracking enabled
        self.window_locked = False
        self.icon = ICON_ACTIVE

    def toggle_timer(self, sender):
        if not self.is_tracking:
            self.timer_button.title = "Auto-tracking Active"
            self.icon = ICON_ACTIVE
            self.is_tracking = True
        else:
            self.time_tracker.stop()  # Stop any ongoing tracking
            self.timer_button.title = "Auto-tracking Disabled"
            self.icon = ICON_INACTIVE
            self.is_tracking = False

    def toggle_window_lock(self, sender):
        if not self.window_locked:
            self.window_manager.lock_current_window()
            self.lock_window_button.title = "Unlock Window"
            self.window_locked = True
        else:
            self.window_manager.unlock_current_window()
            self.lock_window_button.title = "Lock Window"
            self.window_locked = False

    def show_stats(self, _):
        stats = self.time_tracker.get_statistics()
        total_time = timedelta(seconds=stats['total_seconds'])
        today_time = timedelta(seconds=stats['today_seconds'])

        message = (
            f"Total tracked time: {total_time}\n"
            f"Today's tracked time: {today_time}\n"
            f"Sessions today: {stats['sessions_today']}"
        )
        rumps.notification(
            title="Productivity Statistics",
            subtitle="Time Tracking Summary",
            message=message
        )