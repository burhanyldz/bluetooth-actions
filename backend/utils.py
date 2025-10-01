"""
Utility functions for Bluetooth Manager
"""

import re
from typing import Optional


def normalize_mac_address(mac: str) -> str:
    """
    Normalize MAC address to standard format (uppercase with colons)
    
    Args:
        mac: MAC address in any format
        
    Returns:
        Normalized MAC address (XX:XX:XX:XX:XX:XX)
    """
    # Remove any non-alphanumeric characters
    mac = re.sub(r'[^0-9A-Fa-f]', '', mac)
    
    # Ensure it's 12 characters
    if len(mac) != 12:
        raise ValueError(f"Invalid MAC address: {mac}")
    
    # Format with colons and uppercase
    mac = mac.upper()
    return ':'.join([mac[i:i+2] for i in range(0, 12, 2)])


def get_device_type_from_class(device_class: str) -> str:
    """
    Determine device type from Bluetooth class
    
    Args:
        device_class: Bluetooth device class (e.g., "0x240404")
        
    Returns:
        Human-readable device type
    """
    # Bluetooth device class mapping (simplified)
    # Format: 0xMMmmTT where MM=major, mm=minor, TT=service
    
    if not device_class or not device_class.startswith('0x'):
        return 'unknown'
    
    try:
        class_value = int(device_class, 16)
        major_class = (class_value >> 8) & 0x1F
        
        major_device_classes = {
            0x01: 'computer',
            0x02: 'phone',
            0x03: 'network',
            0x04: 'audio',  # Audio/Video
            0x05: 'peripheral',  # Keyboard, mouse
            0x06: 'imaging',
            0x07: 'wearable',
            0x08: 'toy',
            0x09: 'health'
        }
        
        return major_device_classes.get(major_class, 'unknown')
    except:
        return 'unknown'


def get_signal_strength_description(rssi: Optional[int]) -> str:
    """
    Get human-readable signal strength description
    
    Args:
        rssi: Signal strength in dBm
        
    Returns:
        Description string
    """
    if rssi is None:
        return "Unknown"
    
    if rssi >= -50:
        return "Excellent"
    elif rssi >= -60:
        return "Good"
    elif rssi >= -70:
        return "Fair"
    elif rssi >= -80:
        return "Weak"
    else:
        return "Very Weak"


def get_friendly_uuid_name(uuid: str) -> str:
    """
    Convert Bluetooth UUID to friendly name
    
    Args:
        uuid: Bluetooth service UUID
        
    Returns:
        Friendly service name
    """
    # Common Bluetooth UUIDs
    uuid_map = {
        '00001108-0000-1000-8000-00805f9b34fb': 'Headset',
        '0000110b-0000-1000-8000-00805f9b34fb': 'Audio Sink',
        '0000110c-0000-1000-8000-00805f9b34fb': 'Audio/Video Remote Control',
        '0000110e-0000-1000-8000-00805f9b34fb': 'Audio/Video Remote Control',
        '0000111e-0000-1000-8000-00805f9b34fb': 'Handsfree',
        '0000180f-0000-1000-8000-00805f9b34fb': 'Battery Service',
        '0000180a-0000-1000-8000-00805f9b34fb': 'Device Information',
        '00001812-0000-1000-8000-00805f9b34fb': 'Human Interface Device',
        '0000110a-0000-1000-8000-00805f9b34fb': 'Audio Source',
        '00001800-0000-1000-8000-00805f9b34fb': 'Generic Access',
        '00001801-0000-1000-8000-00805f9b34fb': 'Generic Attribute',
    }
    
    return uuid_map.get(uuid.lower(), uuid)


def parse_battery_percentage(battery_str: str) -> Optional[int]:
    """
    Parse battery percentage from bluetoothctl output
    
    Args:
        battery_str: Battery string from bluetoothctl (e.g., "0x46 (70)")
        
    Returns:
        Battery percentage as integer, or None
    """
    match = re.search(r'\((\d+)\)', battery_str)
    if match:
        return int(match.group(1))
    return None


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human-readable string
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "2m 30s")
    """
    if seconds < 60:
        return f"{seconds}s"
    
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    
    if minutes < 60:
        if remaining_seconds > 0:
            return f"{minutes}m {remaining_seconds}s"
        return f"{minutes}m"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    if remaining_minutes > 0:
        return f"{hours}h {remaining_minutes}m"
    return f"{hours}h"


def is_valid_mac_address(mac: str) -> bool:
    """
    Check if string is a valid MAC address
    
    Args:
        mac: String to check
        
    Returns:
        True if valid MAC address
    """
    # Pattern for MAC address with various separators or no separator
    pattern = r'^([0-9A-Fa-f]{2}[:-]?){5}([0-9A-Fa-f]{2})$'
    return bool(re.match(pattern, mac))


def sanitize_device_name(name: str) -> str:
    """
    Sanitize device name for display
    
    Args:
        name: Raw device name
        
    Returns:
        Sanitized name
    """
    if not name:
        return "Unknown Device"
    
    # Remove any control characters
    name = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', name)
    
    # Trim whitespace
    name = name.strip()
    
    if not name:
        return "Unknown Device"
    
    return name
