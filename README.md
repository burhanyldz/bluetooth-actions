# Bluetooth Manager - Home Assistant Add-on

A comprehensive web-based GUI for managing Bluetooth connections in Home Assistant OS. This add-on provides an intuitive interface for pairing, connecting, and managing Bluetooth devices without requiring SSH or command-line access.

## Features

- 🔍 **Device Scanning** - Discover nearby Bluetooth devices in real-time
- 🔗 **Easy Pairing** - Pair and connect to devices with a single click
- 📱 **Device Management** - Connect, disconnect, trust, and remove devices
- 📊 **Status Monitoring** - View connection status, signal strength (RSSI), and battery levels
- 🎧 **Audio Device Focus** - Filter and prioritize Bluetooth audio devices
- 🌐 **Web Interface** - Modern, responsive UI accessible from any device
- ⚡ **Real-time Updates** - WebSocket-based live status updates

## Screenshots

*Coming soon*

## Installation

### Method 1: Add Repository to Home Assistant

1. In Home Assistant, navigate to **Supervisor** → **Add-on Store**
2. Click the **⋮** menu in the top right and select **Repositories**
3. Add this repository URL: `https://github.com/burhanyldz/bluetooth-actions`
4. Find **Bluetooth Manager** in the add-on store and click **Install**

### Method 2: Manual Installation

1. Copy the `bluetooth-manager` folder to your Home Assistant's `/addons` directory
2. Restart Home Assistant
3. Navigate to **Supervisor** → **Add-on Store**
4. Find **Bluetooth Manager** and click **Install**

## Configuration

The add-on supports the following configuration options:

```yaml
log_level: info
port: 8099
```

### Options

- **log_level** (optional): Set the logging level
  - Options: `debug`, `info`, `warning`, `error`
  - Default: `info`

- **port** (optional): Port for the web interface
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
2. Click **Start Scan** in the add-on interface
3. Wait for your device to appear in the Discovered Devices list
4. Click **Pair & Connect** on your device
5. The device will be paired, trusted, and connected automatically

### Managing Devices

- **Connect/Disconnect**: Toggle connection status from the device card
- **View Details**: Click the info button (i) to see detailed device information
- **Trust/Untrust**: Control whether devices can auto-reconnect
- **Remove**: Delete a device from the paired list

## Technical Details

### Architecture

- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: Vanilla JavaScript with modern CSS
- **Bluetooth Interface**: Uses `bluetoothctl` from BlueZ
- **Communication**: REST API + WebSocket for real-time updates

### Requirements

- Home Assistant OS with Bluetooth support
- Built-in Bluetooth adapter or USB Bluetooth dongle
- Home Assistant Supervisor

### Supported Devices

This add-on supports both:
- **Classic Bluetooth (BR/EDR)**: Audio devices, keyboards, mice, etc.
- **Bluetooth Low Energy (BLE)**: Sensors, smart devices, etc.

Tested with:
- Bluetooth speakers and headphones
- Bluetooth keyboards and mice
- Smartphones and tablets

## Troubleshooting

### Device Not Found

- Ensure the device is in pairing mode
- Make sure the device is close to your Home Assistant
- Try stopping and restarting the scan
- Check if the Bluetooth adapter is powered on

### Connection Failed

- Remove the device and try pairing again
- Restart the Bluetooth service by toggling adapter power
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

- `GET /api/adapters` - List Bluetooth adapters
- `GET /api/devices` - List all known devices
- `GET /api/devices/{mac}/info` - Get device details
- `POST /api/devices/{mac}/pair` - Pair with device
- `POST /api/devices/{mac}/connect` - Connect to device
- `POST /api/devices/{mac}/disconnect` - Disconnect from device
- `DELETE /api/devices/{mac}` - Remove device
- `WebSocket /ws/scan` - Real-time scan updates

See the full API documentation at `http://homeassistant.local:8099/docs`

## Development

### Building Locally

```bash
# Clone the repository
git clone https://github.com/burhanyldz/bluetooth-actions.git
cd bluetooth-actions

# Build the Docker image
docker build -t bluetooth-manager .

# Run locally
docker run -it --rm \
  --privileged \
  --network host \
  -v /var/run/dbus:/var/run/dbus \
  bluetooth-manager
```

### Testing

```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt

# Run the backend
python app.py --port 8099 --log-level debug

# Access the UI at http://localhost:8099
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for [Home Assistant](https://www.home-assistant.io/)
- Uses [BlueZ](http://www.bluez.org/) Bluetooth stack
- Powered by [FastAPI](https://fastapi.tiangolo.com/)

## Support

If you find this add-on useful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs and issues
- 💡 Suggesting new features
- 📖 Improving documentation

## Changelog

### Version 1.0.0 (Initial Release)

- ✨ Device scanning and discovery
- 🔗 One-click pairing and connection
- 📊 Real-time status updates via WebSocket
- 🎨 Modern, responsive web interface
- 🔋 Battery level display for supported devices
- 📡 Signal strength (RSSI) monitoring
- 🎧 Audio device filtering
- 🔒 Device trust management

---

**Note**: This add-on requires Home Assistant OS and will not work on Home Assistant Container or Home Assistant Core installations without additional setup.
