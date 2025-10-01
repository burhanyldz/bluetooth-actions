# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2025-10-01

### Fixed
- **Critical:** Use host D-Bus socket instead of starting own daemon - fixes all Bluetooth communication
- Add `host_dbus: true` configuration for proper Home Assistant Bluetooth access
- Comprehensive logging added throughout to diagnose permission and connectivity issues
- Improved error detection for adapter power commands

### Added
- Startup diagnostics to verify D-Bus and bluetoothctl connectivity
- Detailed logging in bluetooth_manager.py for all operations

## [1.0.2] - 2025-10-01

### Fixed
- Corrected bluetoothd startup path to improve compatibility with Home Assistant base images.
- Improved scanning implementation using interactive bluetoothctl mode with non-blocking reads and graceful shutdown.
- General stability and error handling improvements for adapter operations and scanning.

## [1.0.1] - 2025-10-01

### Fixed
- Use interactive bluetoothctl execution (stdin piping) to avoid intermittent errors when toggling adapter power.
- Added timeouts and improved command execution handling to reduce hangs.

## [1.0.0] - 2025-10-01

### Added
- Initial release of Bluetooth Manager add-on
- Web-based GUI for Bluetooth management
- Device scanning and discovery with real-time updates
- One-click pairing and connection
- Device management (connect, disconnect, trust, untrust, remove)
- Signal strength (RSSI) monitoring
- Battery level display for supported devices
- Audio device filtering
- Detailed device information modal
- Real-time WebSocket updates
- Responsive design for mobile and desktop
- Dark theme matching Home Assistant aesthetic
- Toast notifications for user feedback
- Loading states for async operations
- FastAPI backend with REST API
- Complete bluetoothctl integration
- Error handling with user-friendly messages

### Technical
- Python 3.11+ backend
- FastAPI web framework
- Vanilla JavaScript frontend
- WebSocket support for real-time updates
- BlueZ bluetoothctl integration
- Docker containerization
- Home Assistant add-on structure
- Comprehensive API documentation

### Documentation
- Complete README with installation instructions
- Troubleshooting guide
- API documentation
- Configuration options
- Usage examples

## [Unreleased]

### Planned Features
- Bluetooth LE (BLE) device support improvements
- Device grouping and organization
- Auto-reconnect automation
- Integration with Home Assistant media player entities
- Device connection history
- Bluetooth adapter selection (multi-adapter support)
- Custom device icons
- Device nickname/alias editing
- Export/import device configurations
- Connection scheduling
- Audio profile selection
- Volume control integration
