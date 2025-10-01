# Bluetooth Manager Documentation

## Installation

1. Add the repository to Home Assistant:
   - Navigate to **Supervisor** → **Add-on Store**
   - Click **⋮** → **Repositories**
   - Add: `https://github.com/burhanyldz/bluetooth-actions`

2. Install the add-on:
   - Find "Bluetooth Manager" in the store
   - Click **Install**

3. Configure (optional):
   ```yaml
   log_level: info
   port: 8099
   ```

4. Start the add-on and open the Web UI

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `log_level` | list | `info` | Logging level: `debug`, `info`, `warning`, `error` |
| `port` | int | `8099` | Port for web interface |

## Usage Guide

### Pairing a Device

1. Put your Bluetooth device in pairing mode (check device manual)
2. Click **Start Scan** in the add-on interface
3. Wait for your device to appear in the Discovered Devices list
4. Click **Pair & Connect** on your device
5. Device will be automatically paired, trusted, and connected

### Managing Devices

- **Connect/Disconnect**: Toggle connection from the device card
- **View Details**: Click the info button (ℹ️) to see device information
- **Trust/Untrust**: Control auto-reconnection in device details
- **Remove**: Click the trash button (🗑️) to unpair device

## Troubleshooting

### Device Not Found

- Ensure device is in pairing mode
- Move device closer to Home Assistant
- Check if Bluetooth adapter is powered on
- Restart the scan

### Connection Failed

- Remove device and try pairing again
- Toggle adapter power off and on
- Restart the add-on
- Check device battery

### Adapter Not Ready

- Restart the add-on
- Power cycle the Bluetooth adapter
- Check Home Assistant logs
- Verify hardware has Bluetooth

### Can't Access Web UI

- Ensure add-on is running
- Check port is not blocked
- Try direct URL: `http://homeassistant.local:8099`
- Check add-on logs for errors

## Technical Details

### Architecture

- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: Vanilla JavaScript
- **Bluetooth**: BlueZ bluetoothctl
- **Communication**: REST API + WebSocket

### API Endpoints

```
GET  /api/adapters              - List Bluetooth adapters
GET  /api/devices               - List all known devices
GET  /api/devices/{mac}/info    - Get device details
POST /api/devices/{mac}/pair    - Pair with device
POST /api/devices/{mac}/connect - Connect to device
POST /api/devices/{mac}/disconnect - Disconnect
DELETE /api/devices/{mac}       - Remove device
WebSocket /ws/scan              - Real-time updates
```

### Supported Devices

- Bluetooth speakers and headphones
- Bluetooth keyboards and mice
- Smartphones and tablets
- Most Classic Bluetooth (BR/EDR) devices
- Many Bluetooth Low Energy (BLE) devices

### Requirements

- Home Assistant OS with Supervisor
- Bluetooth adapter (built-in or USB)
- BlueZ Bluetooth stack

## Support

- [GitHub Issues](https://github.com/burhanyldz/bluetooth-actions/issues) - Bug reports
- [Documentation](https://github.com/burhanyldz/bluetooth-actions) - Full docs
- [Contributing Guide](https://github.com/burhanyldz/bluetooth-actions/blob/main/CONTRIBUTING.md) - Help improve

## License

MIT License - Free and open source
