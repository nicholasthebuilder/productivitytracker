from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from datetime import datetime, timedelta
from .time_tracker import TimeTracker
from .window_manager import WindowManager
from .storage import Storage
from .icons import ICON_ACTIVE, ICON_INACTIVE
import cairosvg
import io

class ProductivityApp:
    def __init__(self):
        self.app = QApplication.instance() or QApplication([])

        # Initialize components
        self.storage = Storage()
        self.time_tracker = TimeTracker(self.storage)
        self.window_manager = WindowManager(time_tracker=self.time_tracker)

        # Create system tray icon with improved styling
        self.tray = QSystemTrayIcon()
        self.create_menu()
        self.tray.setIcon(self.create_icon(True))
        self.tray.activated.connect(self.handle_tray_activation)
        self.tray.show()

        # State
        self.is_tracking = True
        self.window_locked = False

    def create_icon(self, active):
        """Create icon from SVG with proper scaling"""
        svg_data = ICON_ACTIVE if active else ICON_INACTIVE
        png_data = cairosvg.svg2png(bytestring=svg_data.encode(), scale=2.0)
        pixmap = QPixmap()
        pixmap.loadFromData(png_data)
        return QIcon(pixmap)

    def handle_tray_activation(self, reason):
        """Handle tray icon click to show menu as dropdown"""
        if reason == QSystemTrayIcon.Trigger:
            menu = self.tray.contextMenu()
            # Position the menu below the icon
            pos = self.get_tray_position()
            menu.popup(pos)

    def get_tray_position(self):
        """Get position for dropdown menu below the tray icon"""
        geo = self.tray.geometry()
        return QPoint(geo.x(), geo.y() + geo.height())

    def create_menu(self):
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #E8E8E8;
            }
            QMenu::separator {
                height: 1px;
                background: #E8E8E8;
                margin: 4px 0px;
            }
        """)

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

        # Format system stats
        system_stats = stats['system_stats']
        total_system_time = timedelta(seconds=system_stats['total_time'])
        inactive_time = timedelta(seconds=system_stats['inactive_time'])
        active_time = timedelta(seconds=system_stats['active_time'])

        # Format browser stats
        browser_stats = []
        for domain, seconds in system_stats['browser_stats'].items():
            browser_stats.append(f"{domain}: {timedelta(seconds=seconds)}")

        message = (
            f"Productive Time:\n"
            f"- Total tracked: {total_time}\n"
            f"- Today's tracked: {today_time}\n"
            f"- Sessions today: {stats['sessions_today']}\n\n"
            f"System Activity (24h):\n"
            f"- Total time: {total_system_time}\n"
            f"- Active time: {active_time}\n"
            f"- Inactive time: {inactive_time}\n\n"
            f"Browser Activity:\n"
            + "\n".join(browser_stats)
        )

        self.tray.showMessage(
            "Productivity Statistics",
            message,
            QSystemTrayIcon.Information,
            5000
        )

    def run(self):
        self.app.exec_()