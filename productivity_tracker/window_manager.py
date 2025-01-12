from Foundation import NSObject
from AppKit import NSWorkspace, NSApplication, NSWindow
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID
)

class WindowManager:
    def __init__(self, time_tracker=None):
        self.locked_window = None
        self.workspace = NSWorkspace.sharedWorkspace()
        self.time_tracker = time_tracker
        self.setup_workspace_notifications()

    def setup_workspace_notifications(self):
        notification_center = self.workspace.notificationCenter()
        notification_center.addObserver_selector_name_object_(
            self,
            'activeApplicationChanged:',
            'NSWorkspaceDidActivateApplicationNotification',
            None
        )

    def activeApplicationChanged_(self, notification):
        if self.time_tracker:
            active_app = self.workspace.frontmostApplication()
            app_name = active_app.localizedName()
            window = self.get_frontmost_window()
            window_title = window.get('kCGWindowName', '') if window else ''
            self.time_tracker.handle_app_switch(app_name, window_title)

    def get_frontmost_window(self):
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID
        )

        for window in window_list:
            if window.get('kCGWindowLayer', 0) == 0:
                return window
        return None

    def lock_current_window(self):
        window = self.get_frontmost_window()
        if window:
            self.locked_window = window
            window_number = window.get('kCGWindowNumber', 0)
            pid = window.get('kCGWindowOwnerPID', 0)

            app = NSApplication.sharedApplication()
            windows = app.windows()
            for w in windows:
                if w.windowNumber() == window_number:
                    w.setLevel_(3)  # NSFloatingWindowLevel
                    break

    def unlock_current_window(self):
        if self.locked_window:
            window_number = self.locked_window.get('kCGWindowNumber', 0)
            app = NSApplication.sharedApplication()
            windows = app.windows()
            for w in windows:
                if w.windowNumber() == window_number:
                    w.setLevel_(0)  # NSNormalWindowLevel
                    break
            self.locked_window = None