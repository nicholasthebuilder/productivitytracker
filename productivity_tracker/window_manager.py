from Foundation import NSObject
from AppKit import NSWorkspace, NSApplication, NSWindow
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID
)

class WindowManager:
    def __init__(self):
        self.locked_window = None
        self.workspace = NSWorkspace.sharedWorkspace()
    
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
            # Get the window number and process ID
            window_number = window.get('kCGWindowNumber', 0)
            pid = window.get('kCGWindowOwnerPID', 0)
            
            # Force the window to stay on top
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
