# Changelog

## 1.0.4 (2025-10-01)

### Fixed
- Corrected D-Bus socket path from `/host/run/dbus/system_bus_socket` to `/run/dbus/system_bus_socket` (Home Assistant mounts it at /run/dbus when host_dbus is enabled)
- Enhanced startup diagnostics to check if D-Bus socket file exists and list available files
- Add timeout to bluetoothctl test command to prevent hangs
- Better error messages showing actual socket paths

## 1.0.3 (2025-10-01)

### Fixed
- **Critical:** Use host D-Bus socket instead of starting own D-Bus daemon (fixes all Bluetooth communication issues)
- Add `host_dbus: true` to config.yaml for proper D-Bus access
- Add comprehensive logging throughout bluetoothctl execution to help diagnose issues
- Improve error detection for adapter power commands (check for "succeeded" in output)
- Add startup diagnostics to test D-Bus and bluetoothctl connectivity

### Added
- Detailed logging in all Bluetooth operations to help troubleshoot permission and connectivity issues
- Startup tests to verify D-Bus connection and bluetoothctl availability

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
