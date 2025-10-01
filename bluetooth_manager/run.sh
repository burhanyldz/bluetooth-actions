#!/usr/bin/with-contenv bashio

# Get configuration
PORT=$(bashio::config 'port')
LOG_LEVEL=$(bashio::config 'log_level')

bashio::log.info "Starting Bluetooth Manager on port ${PORT}..."

# Use host D-Bus (critical for Home Assistant Bluetooth access)
export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

bashio::log.info "D-Bus socket: ${DBUS_SYSTEM_BUS_ADDRESS}"

# Test D-Bus connection
if dbus-send --system --print-reply --dest=org.freedesktop.DBus /org/freedesktop/DBus org.freedesktop.DBus.ListNames > /dev/null 2>&1; then
    bashio::log.info "✓ D-Bus connection successful"
else
    bashio::log.warning "⚠ D-Bus connection test failed - Bluetooth may not work"
fi

# Test bluetoothctl availability
if command -v bluetoothctl > /dev/null 2>&1; then
    bashio::log.info "✓ bluetoothctl is available"
    # Test basic command
    if bluetoothctl list > /dev/null 2>&1; then
        bashio::log.info "✓ bluetoothctl can communicate with Bluetooth daemon"
    else
        bashio::log.warning "⚠ bluetoothctl cannot communicate with Bluetooth daemon"
    fi
else
    bashio::log.error "✗ bluetoothctl not found!"
fi

# Start Python backend
bashio::log.info "Starting backend server..."
cd /app
python3 backend/app.py --port ${PORT} --log-level ${LOG_LEVEL}
