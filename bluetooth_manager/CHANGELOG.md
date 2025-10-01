# Changelog

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
