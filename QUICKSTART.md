# Quick Start Guide

## For End Users

### Installation

1. **Add Repository** (if not already added):
   - Go to Supervisor → Add-on Store → ⋮ → Repositories
   - Add: `https://github.com/burhanyldz/bluetooth-actions`

2. **Install Add-on**:
   - Find "Bluetooth Manager" in the add-on store
   - Click "Install"
   - Wait for installation to complete

3. **Configure** (optional):
   ```yaml
   log_level: info
   port: 8099
   ```

4. **Start**:
   - Click "Start"
   - Enable "Start on boot" (optional)
   - Click "Open Web UI"

### Basic Usage

#### Pairing a Device

1. **Put device in pairing mode** (check device manual)
2. **Click "Start Scan"** in the add-on
3. **Wait** for your device to appear
4. **Click "Pair & Connect"**
5. Done! ✅

#### Managing Devices

- **Connect**: Click the "Connect" button on a disconnected device
- **Disconnect**: Click the "Disconnect" button on a connected device
- **View Info**: Click the ℹ️ button to see details
- **Remove**: Click the 🗑️ button to unpair

#### Troubleshooting

**Device not found?**
- Ensure device is in pairing mode
- Check if Bluetooth adapter is powered on
- Try moving device closer
- Restart the scan

**Can't connect?**
- Try removing and re-pairing
- Toggle adapter power off and on
- Restart the add-on
- Check device battery

**No Web UI?**
- Check if add-on is running
- Verify port 8099 is not blocked
- Try `http://homeassistant.local:8099`
- Check add-on logs

---

## For Developers

### Project Structure

```
bluetooth-actions/
├── backend/              # Python backend
│   ├── app.py           # FastAPI server
│   ├── bluetooth_manager.py  # BT operations
│   ├── utils.py         # Helper functions
│   └── requirements.txt # Dependencies
├── web/                 # Frontend
│   ├── index.html      # Main UI
│   ├── css/style.css   # Styles
│   └── js/
│       ├── api.js      # API client
│       └── app.js      # App logic
├── config.yaml         # HA add-on config
├── config.json         # Add-on metadata
├── Dockerfile          # Container
└── run.sh             # Startup script
```

### Quick Setup

```bash
# Clone
git clone https://github.com/burhanyldz/bluetooth-actions.git
cd bluetooth-actions

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py --port 8099

# Open http://localhost:8099
```

### Docker Build

```bash
# Single architecture
docker build -t bluetooth-manager .

# Multi-architecture
./build.sh
```

### Testing

```bash
# Run backend
cd backend
python app.py --log-level debug

# Test API
curl http://localhost:8099/api/adapters

# Test WebSocket
wscat -c ws://localhost:8099/ws/scan
```

### Key Commands

**Backend:**
```bash
# Install deps
pip install -r requirements.txt

# Run server
python app.py --port 8099 --log-level debug

# Format code
black *.py

# Type check
mypy *.py
```

**Docker:**
```bash
# Build
docker build -t bluetooth-manager .

# Run
docker run -it --rm --privileged --network host \
  -v /var/run/dbus:/var/run/dbus bluetooth-manager

# Build all architectures
./build.sh
```

**Git:**
```bash
# Create feature branch
git checkout -b feature/my-feature

# Commit
git add .
git commit -m "Add feature: description"

# Push
git push origin feature/my-feature
```

### API Quick Reference

```bash
# List adapters
GET /api/adapters

# Start scan
POST /api/scan/start

# Stop scan
POST /api/scan/stop

# List devices
GET /api/devices

# Device info
GET /api/devices/{mac}/info

# Pair device
POST /api/devices/{mac}/pair

# Connect device
POST /api/devices/{mac}/connect

# Disconnect device
POST /api/devices/{mac}/disconnect

# Remove device
DELETE /api/devices/{mac}

# WebSocket
WS /ws/scan
```

### Common Tasks

**Add new endpoint:**
1. Add route in `backend/app.py`
2. Implement in `bluetooth_manager.py`
3. Add to `web/js/api.js`
4. Use in `web/js/app.js`

**Add UI component:**
1. Add HTML to `index.html`
2. Style in `css/style.css`
3. Add logic in `js/app.js`
4. Hook up events

**Debug backend:**
```python
# Add breakpoint
import pdb; pdb.set_trace()

# Enable debug logging
python app.py --log-level debug
```

**Debug frontend:**
```javascript
// Console logging
console.log('Data:', data);
console.table(devices);

// Network tab in DevTools
// WebSocket messages
```

### File Reference

| File | Purpose |
|------|---------|
| `backend/app.py` | FastAPI server & endpoints |
| `backend/bluetooth_manager.py` | Bluetooth operations |
| `backend/utils.py` | Helper functions |
| `web/index.html` | UI structure |
| `web/css/style.css` | Styling |
| `web/js/api.js` | API client |
| `web/js/app.js` | Application logic |
| `config.yaml` | Add-on configuration |
| `config.json` | Add-on metadata |
| `Dockerfile` | Container definition |
| `run.sh` | Startup script |

### Resources

- 📖 [README.md](README.md) - Full documentation
- 🔧 [DEVELOPMENT.md](DEVELOPMENT.md) - Developer guide
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guide
- 📝 [CHANGELOG.md](CHANGELOG.md) - Version history
- 🐛 [Issues](https://github.com/burhanyldz/bluetooth-actions/issues) - Bug reports

### Support

- 💬 Create an issue on GitHub
- 📧 Contact maintainer
- 💡 Feature requests welcome

---

**Happy coding! 🎉**
