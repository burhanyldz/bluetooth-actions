#!/usr/bin/with-contenv bashio

# Get configuration
PORT=$(bashio::config 'port')
LOG_LEVEL=$(bashio::config 'log_level')

bashio::log.info "Starting Bluetooth Manager on port ${PORT}..."

# Start D-Bus if not running
if ! pgrep -x "dbus-daemon" > /dev/null; then
    bashio::log.info "Starting D-Bus..."
    mkdir -p /var/run/dbus
    dbus-daemon --system --nofork --nopidfile &
    sleep 2
fi

# Start Bluetooth service if not running
if ! pgrep -x "bluetoothd" > /dev/null; then
    bashio::log.info "Starting Bluetooth service..."
    /usr/libexec/bluetooth/bluetoothd &
    sleep 2
fi

# Start Python backend
bashio::log.info "Starting backend server..."
cd /app
python3 backend/app.py --port ${PORT} --log-level ${LOG_LEVEL}
