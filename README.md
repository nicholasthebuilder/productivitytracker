# macOS Productivity Tracker

A menu bar application for tracking productivity and managing windows on macOS.

## Features

- **Automatic Time Tracking**
  - Tracks time spent in productive applications (VSCode, PyCharm, Terminal)
  - Special tracking for browser activity on productive sites (e.g., claude.ai)
  - Automatically pauses when switching to non-productive apps

- **System Activity Monitoring**
  - 24-hour system activity tracking
  - Inactive time detection (no mouse/keyboard activity)
  - Detailed browser usage statistics

- **Window Management**
  - Lock windows to keep them on top
  - Prevent windows from being sent to background

- **Statistics and Reporting**
  - Total productive time tracking
  - Daily session statistics
  - Browser activity breakdown
  - System-wide activity monitoring

## Requirements

- Python 3.x
- PyQt5
- psutil

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/productivity-tracker.git
cd productivity-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

The app will appear in your system tray with the following options:
- Auto-tracking Active/Disabled: Toggle automatic time tracking
- Lock Window: Keep current window on top
- Show Statistics: View productivity metrics

## Data Storage

All data is stored locally in `~/.productivity_tracker/`:
- `sessions.json`: Tracking session data
- `settings.json`: User preferences

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
