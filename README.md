# Bluetooth Actions - Home Assistant Add-on Repository

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fburhanyldz%2Fbluetooth-actions)

Home Assistant add-on repository for Bluetooth device management.

## Add-ons in this Repository

### 🔵 Bluetooth Manager

A comprehensive web-based GUI for managing Bluetooth connections in Home Assistant OS. This add-on provides an intuitive interface for pairing, connecting, and managing Bluetooth devices without requiring SSH or command-line access.

**Features:**
- 🔍 Real-time device scanning
- 🔗 One-click pairing and connection
- 📱 Device management (connect, disconnect, trust, remove)
- 📊 Status monitoring with battery level and signal strength
- 🌐 Modern, responsive web interface
- ⚡ WebSocket-based live updates

[📖 Full Documentation →](bluetooth_manager/README.md)

## Installation

Click the badge above or follow these steps:

1. In Home Assistant, navigate to **Supervisor** → **Add-on Store**
2. Click the **⋮** menu in the top right and select **Repositories**
3. Add this repository URL: `https://github.com/burhanyldz/bluetooth-actions`
4. Click **Save**
5. Find **Bluetooth Manager** in the add-on store and click **Install**

## Configuration

Each add-on has its own configuration options. See the individual add-on documentation for details.
  - Default: `8099`

## Usage

1. **Start the add-on** from the Supervisor page
2. **Access the interface** by clicking "Open Web UI" or navigating to `http://homeassistant.local:8099`
3. **Enable Bluetooth** by toggling the power button in the header
4. **Scan for devices** by clicking "Start Scan"
5. **Pair and connect** to discovered devices with one click
6. **Manage devices** from the Paired Devices tab

### Pairing a Bluetooth Device

1. Put your Bluetooth device in pairing mode
## Usage

See the [Bluetooth Manager documentation](bluetooth_manager/README.md) for detailed usage instructions.

**Quick Start:**
1. Open the add-on web interface
2. Click "Start Scan" to discover devices
3. Click "Pair & Connect" on your device
4. Manage your devices from the interface

## Support

- 📖 [Full Documentation](bluetooth_manager/README.md)
- 🔧 [Development Guide](DEVELOPMENT.md)
- 🤝 [Contributing Guidelines](CONTRIBUTING.md)
- 🐛 [Issue Tracker](https://github.com/burhanyldz/bluetooth-actions/issues)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**Made for Home Assistant** 🏠
- Check if the device is already connected to another system
- Verify the device has sufficient battery

### Adapter Not Ready

- Restart the add-on
- Power cycle the Bluetooth adapter
- Check Home Assistant logs for Bluetooth service errors
- Verify your hardware has a working Bluetooth adapter

### Can't Access Web Interface

- Ensure the add-on is running (check Supervisor → Bluetooth Manager)
- Verify the port is not blocked by a firewall
- Try accessing via `http://homeassistant.local:8099`
- Check the add-on logs for errors

## API Documentation

The add-on provides a REST API for advanced integrations:

### Endpoints

**Made for Home Assistant** 🏠
