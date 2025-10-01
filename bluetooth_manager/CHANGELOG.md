# Changelog

## 1.0.2 (2025-10-01)

### Fixed
- Corrected bluetoothd startup path to use the system bluetoothd (improves compatibility with Alpine/Home Assistant base images).
- Improved scanning implementation: use interactive bluetoothctl mode with non-blocking reads and graceful shutdown to make scan start/stop responsive and reliable.
- Better error handling and stability during scan and adapter operations.

## 1.0.1 (2025-10-01)

### Fixed
- Use interactive bluetoothctl execution (stdin piping) to avoid intermittent HTTP 500 errors when toggling adapter power.
- Added timeouts and improved command execution handling to reduce hangs and unclear failures.

## 1.0.0 (2025-10-01)

### Added
- Initial release of Bluetooth Manager add-on
- Web-based GUI for Bluetooth management
- Real-time device scanning with WebSocket updates
- One-click pairing and connection
- Device management (connect, disconnect, trust, untrust, remove)
- Signal strength (RSSI) monitoring
- Battery level display for supported devices
- Audio device filtering
- Detailed device information modal
- Responsive design for mobile and desktop
- Dark theme matching Home Assistant
- Toast notifications for user feedback
- FastAPI backend with REST API
- Complete bluetoothctl integration

### Technical
- Python 3.11+ backend with FastAPI
- Vanilla JavaScript frontend
- Multi-architecture support (amd64, armv7, aarch64, armhf, i386)
- Home Assistant Supervisor integration
- Ingress support for embedded UI
