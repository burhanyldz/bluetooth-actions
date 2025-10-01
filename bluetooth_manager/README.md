# Bluetooth Manager

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg

A comprehensive web-based GUI for managing Bluetooth connections in Home Assistant OS.

## About

This add-on provides an intuitive interface for pairing, connecting, and managing Bluetooth devices without requiring SSH or command-line access.

## Features

- 🔍 **Device Scanning** - Discover nearby Bluetooth devices in real-time
- 🔗 **Easy Pairing** - Pair and connect to devices with a single click
- 📱 **Device Management** - Connect, disconnect, trust, and remove devices
- 📊 **Status Monitoring** - View connection status, signal strength (RSSI), and battery levels
- 🎧 **Audio Device Focus** - Filter and prioritize Bluetooth audio devices
- 🌐 **Web Interface** - Modern, responsive UI accessible from any device
- ⚡ **Real-time Updates** - WebSocket-based live status updates

## Installation

1. Add this repository to your Home Assistant add-on store:
   - Click button below or manually add: `https://github.com/burhanyldz/bluetooth-actions`

   [![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fburhanyldz%2Fbluetooth-actions)

2. Find "Bluetooth Manager" in the add-on store
3. Click "Install"
4. Start the add-on
5. Click "Open Web UI"

## Configuration

```yaml
log_level: info
port: 8099
```

### Options

- **log_level**: Set the logging level (`debug`, `info`, `warning`, `error`)
- **port**: Port for the web interface (default: 8099)

## Usage

1. **Enable Bluetooth** - Toggle the power button in the header
2. **Scan for devices** - Click "Start Scan"
3. **Pair and connect** - Click "Pair & Connect" on discovered devices
4. **Manage devices** - Use the Paired Devices tab to connect/disconnect

## Support

For issues, questions, or feature requests, please visit the [GitHub repository](https://github.com/burhanyldz/bluetooth-actions/issues).

## License

MIT License - see [LICENSE](https://github.com/burhanyldz/bluetooth-actions/blob/main/LICENSE) for details.
