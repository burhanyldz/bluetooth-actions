#!/usr/bin/with-contenv bashio

# Get configuration
PORT=$(bashio::config 'port')
LOG_LEVEL=$(bashio::config 'log_level')

bashio::log.info "Starting Bluetooth Manager on port ${PORT}..."

# Use host D-Bus - Home Assistant mounts it at /run/dbus when host_dbus: true is set
export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/run/dbus/system_bus_socket

bashio::log.info "D-Bus socket: ${DBUS_SYSTEM_BUS_ADDRESS}"
bashio::log.info "Checking if D-Bus socket exists..."

# Check if socket exists
if [ -S /run/dbus/system_bus_socket ]; then
    bashio::log.info "✓ D-Bus socket file exists"
else
    bashio::log.error "✗ D-Bus socket NOT found at /run/dbus/system_bus_socket"
    bashio::log.error "Available files in /run/dbus/:"
    ls -la /run/dbus/ || bashio::log.error "Cannot list /run/dbus/"
fi

# Test D-Bus connection
bashio::log.info "Testing D-Bus connection..."
if dbus-send --system --print-reply --dest=org.freedesktop.DBus /org/freedesktop/DBus org.freedesktop.DBus.ListNames > /dev/null 2>&1; then
    bashio::log.info "✓ D-Bus connection successful"
else
    bashio::log.warning "⚠ D-Bus connection test failed"
fi

# Test bluetoothctl availability
if command -v bluetoothctl > /dev/null 2>&1; then
    bashio::log.info "✓ bluetoothctl is available"
    # Test basic command
    bashio::log.info "Testing bluetoothctl communication..."
    if timeout 5 bluetoothctl list > /tmp/bt_test.log 2>&1; then
        bashio::log.info "✓ bluetoothctl can communicate with Bluetooth daemon"
        bashio::log.info "Bluetooth adapters:"
        cat /tmp/bt_test.log
    else
        bashio::log.warning "⚠ bluetoothctl test failed or timed out"
        bashio::log.warning "Output:"
        cat /tmp/bt_test.log 2>/dev/null || bashio::log.warning "No output"
    fi
else
    bashio::log.error "✗ bluetoothctl not found!"
fi

# Start Python backend
bashio::log.info "Starting backend server..."
cd /app
python3 backend/app.py --port ${PORT} --log-level ${LOG_LEVEL}
