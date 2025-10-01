# Installation Guide - Bluetooth Manager Add-on

This guide provides detailed instructions for installing and configuring the Bluetooth Manager add-on in Home Assistant.

## Prerequisites

Before installing, ensure you have:

- ✅ **Home Assistant OS** (Supervisor installation)
- ✅ **Bluetooth adapter** (built-in or USB dongle)
- ✅ **Network access** to your Home Assistant instance
- ✅ **Administrator access** to Home Assistant

> **Note:** This add-on requires Home Assistant OS with Supervisor. It will not work on Home Assistant Core or Container installations without modifications.

## Installation Methods

### Method 1: Add Repository (Recommended)

1. **Open Home Assistant**
   - Navigate to your Home Assistant web interface
   - Default: `http://homeassistant.local:8123`

2. **Access Add-on Store**
   - Click on **Supervisor** in the sidebar
   - Click on **Add-on Store** tab

3. **Add Repository**
   - Click the **⋮** (three dots) menu in the top-right corner
   - Select **Repositories**
   - Add this URL: `https://github.com/burhanyldz/bluetooth-actions`
   - Click **Add**

4. **Find the Add-on**
   - Refresh the page if needed
   - Scroll down to find **Bluetooth Manager**
   - Or use the search box

5. **Install**
   - Click on **Bluetooth Manager**
   - Click **Install**
   - Wait for installation to complete (may take a few minutes)

### Method 2: Manual Installation

1. **Access Home Assistant File System**
   - Via SSH, Samba share, or File Editor add-on
   - Navigate to `/addons/` directory

2. **Copy Add-on Files**
   ```bash
   cd /addons
   git clone https://github.com/burhanyldz/bluetooth-actions.git
   # Or manually copy the bluetooth-actions folder
   ```

3. **Restart Home Assistant**
   - Go to **Configuration** → **Server Controls**
   - Click **Restart**
   - Wait for restart to complete

4. **Find the Add-on**
   - Go to **Supervisor** → **Add-on Store**
   - Look under **Local add-ons**
   - Click on **Bluetooth Manager**

5. **Install**
   - Click **Install**
   - Wait for installation to complete

## Configuration

### Basic Configuration

The add-on works out of the box with default settings. Optional configuration:

1. **Go to Add-on Page**
   - Supervisor → Bluetooth Manager

2. **Configuration Tab**
   - Click on **Configuration** tab

3. **Edit Settings** (optional)
   ```yaml
   log_level: info
   port: 8099
   ```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `log_level` | list | `info` | Logging level: `debug`, `info`, `warning`, `error` |
| `port` | int | `8099` | Port for web interface |

### Example Configurations

**Development/Debugging:**
```yaml
log_level: debug
port: 8099
```

**Production:**
```yaml
log_level: info
port: 8099
```

**Custom Port:**
```yaml
log_level: info
port: 8888
```

## Starting the Add-on

1. **Start Add-on**
   - Go to **Supervisor** → **Bluetooth Manager**
   - Click **Start**
   - Wait for the add-on to start (check logs for "Started")

2. **Enable Auto-Start** (Optional)
   - Toggle **Start on boot** to ON
   - The add-on will start automatically with Home Assistant

3. **Show in Sidebar** (Optional)
   - Toggle **Show in sidebar** to ON
   - Quick access icon appears in HA sidebar

4. **Access Web UI**
   - Click **Open Web UI**
   - Or navigate to: `http://homeassistant.local:8099`

## Verification

### Check Installation

1. **View Logs**
   - Go to **Supervisor** → **Bluetooth Manager**
   - Click **Log** tab
   - Look for successful startup messages:
     ```
     [INFO] Starting Bluetooth Manager on port 8099...
     [INFO] Starting D-Bus...
     [INFO] Starting Bluetooth service...
     [INFO] Starting backend server...
     ```

2. **Test Web Interface**
   - Click **Open Web UI**
   - You should see the Bluetooth Manager interface
   - Check that adapter name appears in header

3. **Test Bluetooth**
   - Power on the Bluetooth adapter (if not already on)
   - Click **Start Scan**
   - Put a Bluetooth device in pairing mode
   - Verify device appears in discovered list

## Troubleshooting Installation

### Add-on Not Found

**Problem:** Can't find the add-on in the store

**Solutions:**
- Refresh the page
- Check repository was added correctly
- Verify you're running Home Assistant OS with Supervisor
- Check network connectivity
- Try manual installation method

### Installation Failed

**Problem:** Installation fails or hangs

**Solutions:**
- Check available disk space
- Check internet connectivity
- Review Supervisor logs
- Try restarting Home Assistant
- Clear browser cache

### Add-on Won't Start

**Problem:** Add-on starts but immediately stops

**Solutions:**

1. **Check Logs:**
   ```
   Supervisor → Bluetooth Manager → Log tab
   ```

2. **Common Issues:**
   - **No Bluetooth adapter:** Verify hardware
   - **Port conflict:** Change port in configuration
   - **Permission issues:** Restart Home Assistant

3. **Verify Bluetooth Hardware:**
   ```bash
   # Via SSH
   hciconfig
   # or
   bluetoothctl list
   ```

### Can't Access Web UI

**Problem:** "Open Web UI" doesn't work

**Solutions:**
- Verify add-on is running (green status)
- Check port is correct in configuration
- Try direct URL: `http://homeassistant.local:8099`
- Check firewall settings
- Try different browser
- Check if port is in use by another service

### Permission Errors

**Problem:** Bluetooth operations fail with permission errors

**Solutions:**
- Verify add-on has required privileges (configured in config.yaml)
- Restart the add-on
- Restart Home Assistant
- Check D-Bus is running

## Post-Installation Setup

### 1. Initial Configuration

1. **Open Web Interface**
   - Click "Open Web UI" or go to port 8099

2. **Verify Adapter**
   - Check adapter name appears in header
   - Click power button to ensure it's on

3. **Test Scanning**
   - Click "Start Scan"
   - Verify scanning indicator appears

### 2. Pair First Device

1. **Prepare Device**
   - Put Bluetooth device in pairing mode
   - Refer to device manual for instructions

2. **Scan for Device**
   - Click "Start Scan"
   - Wait for device to appear

3. **Pair Device**
   - Click "Pair & Connect" on your device
   - Wait for pairing to complete
   - Device should appear in "Paired Devices"

### 3. Configure Auto-Start (Optional)

Enable **Start on boot** so the add-on starts automatically with Home Assistant.

## Updating the Add-on

### Automatic Updates

1. **Enable Automatic Updates**
   - Go to Supervisor → Bluetooth Manager
   - Toggle **Auto update** to ON

### Manual Update

1. **Check for Updates**
   - Go to Supervisor → Dashboard
   - Look for update notification badge

2. **Update Add-on**
   - Go to Supervisor → Bluetooth Manager
   - Click **Update** button
   - Wait for update to complete
   - Restart if prompted

## Uninstalling

### Remove Add-on

1. **Stop Add-on**
   - Go to Supervisor → Bluetooth Manager
   - Click **Stop**

2. **Uninstall**
   - Click **Uninstall** button
   - Confirm removal

3. **Remove Repository** (Optional)
   - Go to Supervisor → Add-on Store
   - Click ⋮ → Repositories
   - Remove the repository URL

### Clean Up

After uninstalling:
- Bluetooth devices remain paired in Home Assistant OS
- Use `bluetoothctl` via SSH to remove devices if needed

## Hardware Compatibility

### Supported Adapters

**Built-in Bluetooth:**
- Raspberry Pi 3 Model B/B+
- Raspberry Pi 4 Model B
- Raspberry Pi Zero W/WH
- Other ARM boards with integrated Bluetooth

**USB Bluetooth Adapters:**
- Most USB Bluetooth 4.0+ adapters
- Adapters with Broadcom chipsets
- Adapters with Intel chipsets
- Adapters with Realtek chipsets

### Verified Hardware

| Hardware | Status | Notes |
|----------|--------|-------|
| Raspberry Pi 4 | ✅ Working | Built-in Bluetooth |
| Raspberry Pi 3 | ✅ Working | Built-in Bluetooth |
| Generic USB BT 4.0 | ✅ Working | Most adapters work |
| Intel NUC | ✅ Working | With USB adapter |

## Network Configuration

### Default Ports

- **Web Interface:** 8099
- **API:** 8099
- **WebSocket:** 8099

### Firewall Rules

If using a firewall, allow:
- Port 8099 TCP (or your configured port)
- Local network access

## Security Considerations

### Access Control

The add-on uses Home Assistant's ingress mode for authentication:
- Automatically uses HA authentication
- No separate login required
- Access controlled by HA user permissions

### Network Security

- Add-on runs on local network only
- Does not expose ports to internet by default
- Uses Home Assistant's SSL if configured

## Getting Help

### Support Resources

1. **Documentation**
   - README.md - User guide
   - QUICKSTART.md - Quick reference
   - TROUBLESHOOTING section in README

2. **Community**
   - GitHub Issues - Bug reports
   - GitHub Discussions - Questions
   - Home Assistant Community Forum

3. **Logs**
   - Always check logs first
   - Include logs when reporting issues

### Reporting Issues

When reporting problems, include:
- Home Assistant version
- Add-on version
- Hardware (Raspberry Pi model, etc.)
- Error messages from logs
- Steps to reproduce

## Next Steps

After successful installation:

1. ✅ Read the [README.md](README.md) for usage instructions
2. ✅ Check [QUICKSTART.md](QUICKSTART.md) for common tasks
3. ✅ Pair your Bluetooth devices
4. ✅ Explore device management features
5. ✅ Configure auto-start if desired

---

**Congratulations!** You've successfully installed the Bluetooth Manager add-on. Enjoy easier Bluetooth management in Home Assistant! 🎉
