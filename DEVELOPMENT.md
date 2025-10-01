# Development Guide

This guide provides detailed information for developers working on the Bluetooth Manager add-on.

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Home Assistant OS                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Bluetooth Manager Add-on                  │  │
│  │                                                         │  │
│  │  ┌──────────────┐         ┌─────────────────────────┐ │  │
│  │  │   Frontend   │         │       Backend           │ │  │
│  │  │              │◄───────►│                         │ │  │
│  │  │ HTML/CSS/JS  │ HTTP/WS │  Python + FastAPI       │ │  │
│  │  │              │         │                         │ │  │
│  │  └──────────────┘         └───────────┬─────────────┘ │  │
│  │                                       │                │  │
│  │                                       ▼                │  │
│  │                           ┌─────────────────────────┐ │  │
│  │                           │  Bluetooth Manager      │ │  │
│  │                           │  (bluetoothctl wrapper) │ │  │
│  │                           └───────────┬─────────────┘ │  │
│  └───────────────────────────────────────┼───────────────┘  │
│                                          │                   │
│                                          ▼                   │
│                              ┌────────────────────────┐      │
│                              │   BlueZ (bluetoothd)   │      │
│                              └───────────┬────────────┘      │
└──────────────────────────────────────────┼───────────────────┘
                                          │
                                          ▼
                                ┌──────────────────┐
                                │ Bluetooth Device │
                                └──────────────────┘
```

### Component Breakdown

#### Frontend (`web/`)

**Technology:** Vanilla JavaScript, modern CSS, HTML5

**Key Components:**
- `index.html` - Main UI structure
- `css/style.css` - Styling with CSS custom properties
- `js/api.js` - API client for backend communication
- `js/app.js` - Main application logic and UI management

**Responsibilities:**
- Display device lists (paired and discovered)
- Handle user interactions (scan, pair, connect, etc.)
- Real-time UI updates via WebSocket
- Toast notifications and loading states
- Responsive design for mobile/desktop

#### Backend (`backend/`)

**Technology:** Python 3.11+, FastAPI, asyncio

**Key Components:**
- `app.py` - FastAPI application with REST and WebSocket endpoints
- `bluetooth_manager.py` - Core Bluetooth operations via bluetoothctl
- `utils.py` - Helper functions for parsing and formatting

**Responsibilities:**
- Execute bluetoothctl commands
- Parse command output
- Provide REST API for frontend
- WebSocket server for real-time updates
- Error handling and user-friendly messages

## Key Concepts

### Bluetooth Operations

The add-on uses `bluetoothctl` from the BlueZ stack to manage Bluetooth:

1. **Scanning** - Discover nearby devices
2. **Pairing** - Establish initial connection with authentication
3. **Trusting** - Allow device to auto-reconnect
4. **Connecting** - Establish active connection to paired device
5. **Disconnecting** - Close active connection
6. **Removing** - Delete pairing information

### Real-time Updates

The application uses WebSocket to push real-time updates:

```
Frontend                    Backend
   │                          │
   │──── WebSocket Open ─────►│
   │                          │
   │                          │ (Start scanning)
   │                          │
   │◄── Device Discovered ────│
   │◄── RSSI Update ──────────│
   │◄── Device Connected ─────│
   │                          │
```

### Error Handling Flow

```
User Action → Backend API → bluetoothctl command
                 │
                 ├─ Success → Return success response
                 │
                 └─ Error → Parse error message
                           → Convert to user-friendly message
                           → Return error response
                           → Frontend shows toast notification
```

## API Endpoints

### Adapter Management

```
GET  /api/adapters              # List Bluetooth adapters
GET  /api/adapters/{id}/info    # Get adapter details
POST /api/adapters/power        # Power adapter on/off
```

### Device Scanning

```
POST /api/scan/start            # Start scanning
POST /api/scan/stop             # Stop scanning
GET  /api/scan/status           # Get scan status
```

### Device Management

```
GET    /api/devices             # List all known devices
GET    /api/devices/{mac}/info  # Get device details
POST   /api/devices/{mac}/pair  # Pair with device
POST   /api/devices/{mac}/trust # Trust device
POST   /api/devices/{mac}/untrust # Untrust device
POST   /api/devices/{mac}/connect # Connect to device
POST   /api/devices/{mac}/disconnect # Disconnect from device
DELETE /api/devices/{mac}       # Remove device
```

### WebSocket

```
WebSocket /ws/scan              # Real-time updates
```

**Message Types:**
- `discovered` - New device found
- `rssi_update` - Signal strength update
- `device_connected` - Device connected
- `device_disconnected` - Device disconnected
- `device_paired` - Device paired
- `device_removed` - Device removed

## Development Workflow

### 1. Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app:app --reload --port 8099 --log-level debug
```

**Testing bluetoothctl integration:**

```python
from bluetooth_manager import BluetoothManager

bt = BluetoothManager()

# Test adapter
adapters = bt.list_adapters()
print(adapters)

# Test scan
devices = bt.get_devices()
print(devices)

# Test device info
info = bt.get_device_info('AA:BB:CC:DD:EE:FF')
print(info)
```

### 2. Frontend Development

Open `http://localhost:8099` in your browser. Use browser DevTools:

- **Console** - JavaScript errors and logs
- **Network** - API requests and WebSocket messages
- **Elements** - Inspect and modify CSS

**Debugging WebSocket:**

```javascript
// In browser console
const ws = new WebSocket('ws://localhost:8099/ws/scan');
ws.onmessage = (event) => console.log(JSON.parse(event.data));
```

### 3. Docker Development

```bash
# Build image
docker build -t bluetooth-manager-dev .

# Run with bind mounts for development
docker run -it --rm \
  --privileged \
  --network host \
  -v /var/run/dbus:/var/run/dbus \
  -v $(pwd)/backend:/app/backend \
  -v $(pwd)/web:/app/web \
  bluetooth-manager-dev
```

### 4. Testing on Home Assistant

1. Copy add-on folder to `/addons/bluetooth-manager`
2. Restart Home Assistant
3. Install from local add-ons
4. Check logs: Supervisor → Bluetooth Manager → Logs

## Common Development Tasks

### Adding a New API Endpoint

1. **Define endpoint in `backend/app.py`:**

```python
@app.post("/api/devices/{mac}/custom-action")
async def custom_action(mac: str):
    try:
        mac = mac.upper().replace('-', ':')
        success, message = bt_manager.custom_action(mac)
        if success:
            return {"success": True, "message": message}
        else:
            raise HTTPException(status_code=400, detail=message)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

2. **Implement in `bluetooth_manager.py`:**

```python
def custom_action(self, mac_address: str) -> Tuple[bool, str]:
    """
    Perform custom action on device
    
    Args:
        mac_address: MAC address of device
        
    Returns:
        Tuple of (success, message)
    """
    returncode, stdout, stderr = self.execute_command(f'custom {mac_address}')
    
    if returncode == 0:
        return True, "Action successful"
    else:
        return False, self._parse_error(stderr)
```

3. **Add to frontend API client (`web/js/api.js`):**

```javascript
async customAction(mac) {
    return this.request(`/api/devices/${mac}/custom-action`, {
        method: 'POST'
    });
}
```

4. **Use in frontend (`web/js/app.js`):**

```javascript
async performCustomAction(mac) {
    try {
        this.showLoading('Processing...');
        await this.api.customAction(mac);
        this.showToast('Success!', 'success');
    } catch (error) {
        this.showToast(`Failed: ${error.message}`, 'error');
    } finally {
        this.hideLoading();
    }
}
```

### Adding a New UI Component

1. **Add HTML structure to `index.html`**
2. **Style in `style.css`**
3. **Add logic in `app.js`**
4. **Hook up event listeners**

Example - Adding a settings panel:

```html
<!-- In index.html -->
<div id="settings-panel" class="panel hidden">
    <h2>Settings</h2>
    <!-- Settings content -->
</div>
```

```css
/* In style.css */
.panel {
    background-color: var(--card-bg);
    border-radius: 8px;
    padding: 20px;
}

.panel.hidden {
    display: none;
}
```

```javascript
// In app.js
showSettings() {
    document.getElementById('settings-panel').classList.remove('hidden');
}

hideSettings() {
    document.getElementById('settings-panel').classList.add('hidden');
}
```

## Debugging Tips

### Backend Debugging

**Enable debug logging:**
```bash
python app.py --log-level debug
```

**Check bluetoothctl output:**
```python
import subprocess
result = subprocess.run(['bluetoothctl', 'list'], capture_output=True, text=True)
print("stdout:", result.stdout)
print("stderr:", result.stderr)
print("returncode:", result.returncode)
```

**Use Python debugger:**
```python
import pdb; pdb.set_trace()
```

### Frontend Debugging

**Console logging:**
```javascript
console.log('Device:', device);
console.table(devices);  // Nice table view
console.dir(object);     // Interactive object inspection
```

**Network debugging:**
1. Open DevTools → Network tab
2. Filter by "Fetch/XHR" for API calls
3. Click request to see details
4. Check payload and response

**WebSocket debugging:**
```javascript
// Add to api.js
this.ws.onmessage = (event) => {
    console.log('WS Message:', event.data);
    const data = JSON.parse(event.data);
    // ... rest of code
};
```

## Performance Optimization

### Backend

- Use async/await for I/O operations
- Cache adapter info (don't query every request)
- Limit concurrent bluetoothctl processes
- Set appropriate timeouts

### Frontend

- Debounce frequent operations (e.g., filter changes)
- Use event delegation for dynamic content
- Minimize DOM manipulations
- Lazy load device info (only when needed)

## Security Considerations

1. **Input Validation** - Always validate MAC addresses
2. **Command Injection** - Never use user input directly in commands
3. **Rate Limiting** - Prevent API abuse
4. **Authentication** - Use Home Assistant's auth (ingress mode)

## Testing Checklist

Before committing:

- [ ] Code follows style guidelines
- [ ] All functions have docstrings
- [ ] No console errors
- [ ] No Python exceptions
- [ ] Tested on target hardware (if possible)
- [ ] Responsive design works on mobile
- [ ] WebSocket reconnection works
- [ ] Error messages are user-friendly
- [ ] Loading states show appropriately

## Useful Resources

- [BlueZ Documentation](http://www.bluez.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Home Assistant Add-on Development](https://developers.home-assistant.io/docs/add-ons)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

## Getting Help

- Check existing issues on GitHub
- Read the project documentation
- Create a new issue with details
- Join community discussions

Happy coding! 🚀
