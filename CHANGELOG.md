# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.8] - 2025-10-02

### Fixed
- **Critical:** Bluetooth pairing now includes proper state settling delays (2 seconds after pair)
- **Critical:** Trust operation waits 1 second for BlueZ to propagate changes
- **Critical:** Connect operation waits 2 seconds for connection to fully establish
- **Critical:** Device removal now properly disconnects device first if connected
- Enhanced error detection for pair/trust/connect/remove operations
- Paired devices now appear correctly in paired list after pairing
- Removed devices can now be rediscovered in subsequent scans
- Removed device now properly clears from paired devices list and reloads to sync with backend
- Newly paired device now appears in paired devices list immediately
- Paired device automatically switches to paired tab after successful pairing

### Added
- Comprehensive logging for all Bluetooth operations showing command results
- Support for detecting "already paired" devices during pair operation
- Automatic disconnection step before removing paired devices
- Detailed error messages including full bluetoothctl output for troubleshooting

### Changed
- Extended automatic scan timeout from 30 seconds to 60 seconds for better device discovery
- Toast notification now shows "will auto-stop after 60s" instead of 30s
- Paired devices list automatically reloads from backend after removal
- After successful pairing, automatically switches to paired tab to show result

### Improved
- Significantly more reliable Bluetooth operation sequencing
- Proper state synchronization between bluetoothctl operations
- Better handling of Bluetooth stack timing requirements
- Scan duration confirmed at 60 seconds

### Technical Details
- Each Bluetooth operation now waits for BlueZ daemon to update its internal state
- Prevents race conditions between pair→trust→connect sequence
- Ensures device list accurately reflects current Bluetooth state
- Removes timing-dependent failures in quick operation sequences

## [1.0.7] - 2025-10-02

### Fixed
- **Critical:** Home Assistant ingress mode now works correctly
- Fixed 404 errors for CSS, JavaScript, and image assets when using ingress
- Changed all resource paths from absolute (`/static/...`) to relative (`static/...`) for ingress compatibility
- WebSocket connection properly handles Home Assistant proxy paths
- API requests now correctly use base path when running under ingress

### Improved
- Automatic base path detection for seamless ingress integration
- Enhanced debugging with base path and WebSocket URL logging
- Add-on now works both standalone and embedded in Home Assistant sidebar

## [1.0.6] - 2025-10-02

### Fixed
- **Critical:** Power button now correctly toggles Bluetooth adapter on/off with proper state display (blue when powered on)
- **Critical:** Bluetooth scanning now reliably discovers and displays nearby devices using improved polling-based approach
- Application icon in header now loads correctly from /static/icon.png
- "Scanning for devices..." message properly clears when scan stops or completes automatically

### Added
- Connect/Disconnect action buttons in device information modal
- Real-time modal updates after connection state changes
- Home Assistant ingress support for embedded UI experience
- Sidebar panel integration with mdi:bluetooth icon
- Users can now access Bluetooth Manager directly from Home Assistant sidebar without opening new tab

### Improved
- Scanning reliability completely rewritten with device polling approach instead of parsing bluetoothctl output
- Device modal intelligently shows Connect or Disconnect button based on current connection state
- Enhanced adapter power state management and synchronization
- Better user feedback when operations complete

## [1.0.5] - 2025-10-01

### Added
- **Backend:** Automatic 30-second timeout for Bluetooth scanning with proper cleanup and logging
- **Backend:** Comprehensive command logging (command, return code, stdout, stderr) for all bluetoothctl operations
- **Frontend:** Periodic connection status polling every 5 seconds for real-time paired device updates
- **Frontend:** Custom styled confirmation modal replacing native JavaScript alert()
- **Frontend:** Immediate device info modal display with loading spinner while data loads in background
- **Frontend:** Visual loading indicator on refresh button during paired device reload operations
- **Frontend:** Device-specific SVG icons indicating connection states (connected in green, disconnected in red, discovered in blue)

### Fixed
- Power button now correctly displays adapter powered state with accurate on/off text
- Discovered devices panel displays contextual messages based on whether scanning is active or not
- Scanning automatically terminates after 30 seconds to prevent indefinite execution
- Audio device filter checkbox now unchecked by default for better discoverability of all device types
- Application header displays icon.png image instead of FontAwesome Bluetooth icon

### Improved
- Enhanced error detection in adapter power commands by checking for "succeeded" in bluetoothctl output
- More responsive and polished UI with loading indicators across all asynchronous operations
- Superior user experience with styled modals, immediate feedback, and clear visual states

## [1.0.4] - 2025-10-01

### Fixed
- Corrected D-Bus socket path to `/run/dbus/system_bus_socket` (was `/host/run/dbus/...`)
- Enhanced diagnostics to check socket file existence
- Add timeout to prevent startup hangs on bluetoothctl test

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

## [1.0.8] - 2025-10-02

### Fixed
- **Critical:** Bluetooth pairing now includes proper state settling delays (2 seconds after pair)
- **Critical:** Trust operation waits 1 second for BlueZ to propagate changes
- **Critical:** Connect operation waits 2 seconds for connection to fully establish
- **Critical:** Device removal now properly disconnects device first if connected
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
- Toast notification now shows "will auto-stop after 60s" instead of 30s
- Paired devices list automatically reloads from backend after removal
- After successful pairing, automatically switches to paired tab to show result

### Improved
- More reliable Bluetooth operation sequencing with proper state settling times
- Better error messages with full context from bluetoothctl output
- Scan duration already set to 60 seconds (confirmed)
- Paired device is immediately removed from discovered devices list after pairing
- Better state management ensures UI accurately reflects backend state
- More reliable device list updates after all pairing/unpairing operations

## [1.0.7] - 2025-10-02

### Fixed
- **Critical:** Home Assistant ingress mode now works correctly
- Fixed 404 errors for CSS, JavaScript, and image assets when using ingress
- Changed all resource paths from absolute (`/static/...`) to relative (`static/...`) for ingress compatibility
- WebSocket connection properly handles Home Assistant proxy paths
- API requests now correctly use base path when running under ingress

### Improved
- Automatic base path detection for seamless ingress integration
- Enhanced debugging with base path and WebSocket URL logging
- Add-on now works both standalone and embedded in Home Assistant sidebar
