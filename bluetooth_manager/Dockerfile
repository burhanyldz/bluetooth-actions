ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM $BUILD_FROM

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    bluez \
    bluez-deprecated \
    dbus \
    bash

# Set working directory
WORKDIR /app

# Copy backend files
COPY backend/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY web/ ./web/
COPY run.sh /

# Make run script executable
RUN chmod +x /run.sh

# Expose port
EXPOSE 8099

# Labels
LABEL \
    io.hass.name="Bluetooth Manager" \
    io.hass.description="Web-based GUI for managing Bluetooth connections" \
    io.hass.version="1.0.0" \
    io.hass.type="addon" \
    io.hass.arch="armhf|armv7|aarch64|amd64|i386"

# Start script
CMD ["/run.sh"]
