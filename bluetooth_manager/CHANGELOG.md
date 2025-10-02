# Changelog

## 1.0.8 (2025-10-02)

### Fixed
- **Critical:** Pairing now includes proper delays for Bluetooth state to settle (2 second wait after pair)
- **Critical:** Trust operation includes 1 second delay for state propagation
- **Critical:** Connect operation includes 2 second delay for connection to fully establish
- **Critical:** Remove device now disconnects first if connected, then waits for state to settle
- Enhanced error detection for pair/trust/connect/remove operations
- Paired devices now appear correctly in paired list after pairing
- Removed devices can now be discovered again in scan results
- Removed device now properly clears from paired devices list and reloads to sync with backend
- Newly paired device now appears in paired devices list immediately
- Paired device automatically switches to paired tab after successful pairing

### Added
- Comprehensive logging for all Bluetooth operations (pair, trust, connect, disconnect, remove)
- Detection of "already paired" state during pairing
- Automatic disconnection before device removal

### Changed
- Extended scan duration from 30 seconds to 60 seconds for better device discovery
- After pairing, device is removed from discovered devices list
- After removing, paired devices list is reloaded from backend

### Improved
- More reliable Bluetooth operation sequencing with proper state settling times
- Better error messages with full context from bluetoothctl output
- Scan duration already set to 60 seconds (confirmed)
- Better state synchronization between frontend and backend after device operations
- More reliable device list updates after pairing/unpairing operations

## 1.0.7 (2025-10-02)

### Fixed
- **Critical:** Ingress mode now works correctly with proper asset loading
- Changed all resource paths from absolute (`/static/...`) to relative (`static/...`)
- WebSocket connection now correctly handles ingress proxy paths
- API requests now use proper base path for ingress support

### Improved
- Better path detection for Home Assistant ingress integration
- Debug logging for base path and WebSocket URL

## 1.0.6 (2025-10-02)

### Fixed
- **Critical:** Power button now correctly toggles adapter on/off and displays accurate state (blue when on)
- **Critical:** Scanning now properly discovers and displays devices using polling approach
- Icon display in header (now served from /static/icon.png)
- "Scanning for devices..." message now clears when scan stops or completes

### Added
- Connect/Disconnect buttons in device info modal that update in real-time
- Home Assistant ingress support with sidebar panel (mdi:bluetooth icon)
- Panel integration allows using add-on without opening new tab

### Improved
- Scanning reliability with simpler poll-based device discovery
- Device modal now shows appropriate connection action buttons based on state
- Better state management for adapter power status

## 1.0.5 (2025-10-01)

### Added
- **Backend:** Automatic 30-second timeout for Bluetooth scanning with proper cleanup
- **Backend:** Comprehensive logging for all bluetoothctl commands (command, return code, stdout, stderr)
- **Frontend:** Periodic connection status checks every 5 seconds for paired devices
- **Frontend:** Custom confirmation modal replacing native JavaScript alert()
- **Frontend:** Device info modal now displays immediately with loading spinner while data loads
- **Frontend:** Refresh button shows loading indicator during paired device reload
- **Frontend:** Device-specific SVG icons showing connection states (connected, disconnected, discovered)

### Fixed
- Power button now correctly reflects adapter powered state with proper on/off text
- Discovered devices panel shows contextual messages based on scanning state
- Scanning automatically stops after 30 seconds to prevent indefinite runs
- Audio device filter is now unchecked by default
- Header now displays icon.png instead of FontAwesome icon

### Improved
- Better error detection in adapter power commands (checks for "succeeded" in output)
- More responsive UI with loading indicators across all async operations
- Enhanced user experience with styled modals and immediate feedback

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
