"""
Bluetooth Manager Module
Handles all Bluetooth operations via bluetoothctl commands
"""

import subprocess
import re
import asyncio
import time
from typing import Dict, List, Optional, Tuple, Callable
from datetime import datetime


class BluetoothManager:
    """Manages Bluetooth operations using bluetoothctl"""
    
    # Regex patterns for parsing bluetoothctl output
    DEVICE_NEW_PATTERN = re.compile(r'\[NEW\] Device ([0-9A-F:]{17}) (.+)')
    DEVICE_CHG_PATTERN = re.compile(r'\[CHG\] Device ([0-9A-F:]{17})')
    RSSI_PATTERN = re.compile(r'RSSI: (0x[0-9a-f]+) \((-?\d+)\)')
    
    # Device info patterns
    INFO_PATTERNS = {
        'name': re.compile(r'Name: (.+)'),
        'alias': re.compile(r'Alias: (.+)'),
        'paired': re.compile(r'Paired: (yes|no)'),
        'bonded': re.compile(r'Bonded: (yes|no)'),
        'trusted': re.compile(r'Trusted: (yes|no)'),
        'blocked': re.compile(r'Blocked: (yes|no)'),
        'connected': re.compile(r'Connected: (yes|no)'),
        'battery': re.compile(r'Battery Percentage: 0x[0-9a-f]+ \((\d+)\)'),
        'rssi': re.compile(r'RSSI: 0x[0-9a-f]+ \((-?\d+)\)'),
        'class': re.compile(r'Class: (0x[0-9a-f]+)'),
        'icon': re.compile(r'Icon: (.+)'),
    }
    
    def __init__(self):
        self.scanning = False
        self.scan_process = None
        
    def execute_command(self, command: str, timeout: int = 30) -> Tuple[int, str, str]:
        """
        Execute a bluetoothctl command and return exit code, stdout, stderr
        
        Args:
            command: The command to execute (without 'bluetoothctl')
            timeout: Command timeout in seconds
            
        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        try:
            result = subprocess.run(
                ['bluetoothctl', '--'] + command.split(),
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)
    
    def list_adapters(self) -> List[Dict]:
        """
        Get list of Bluetooth adapters
        
        Returns:
            List of adapter dictionaries with 'id', 'name', 'mac' keys
        """
        returncode, stdout, stderr = self.execute_command('list')
        
        adapters = []
        for line in stdout.split('\n'):
            # Format: "Controller MAC_ADDRESS NAME [default]"
            match = re.search(r'Controller ([0-9A-F:]{17}) (.+?)( \[default\])?$', line)
            if match:
                mac, name, is_default = match.groups()
                adapters.append({
                    'id': mac,
                    'name': name.strip(),
                    'mac': mac,
                    'default': is_default is not None
                })
        
        return adapters
    
    def get_adapter_info(self, adapter_id: Optional[str] = None) -> Dict:
        """
        Get detailed information about a Bluetooth adapter
        
        Args:
            adapter_id: MAC address of adapter (None for default)
            
        Returns:
            Dictionary with adapter information
        """
        cmd = f'show {adapter_id}' if adapter_id else 'show'
        returncode, stdout, stderr = self.execute_command(cmd)
        
        info = {'id': adapter_id}
        for line in stdout.split('\n'):
            if 'Name:' in line:
                info['name'] = line.split('Name:')[1].strip()
            elif 'Alias:' in line:
                info['alias'] = line.split('Alias:')[1].strip()
            elif 'Powered:' in line:
                info['powered'] = 'yes' in line.lower()
            elif 'Discoverable:' in line:
                info['discoverable'] = 'yes' in line.lower()
            elif 'Pairable:' in line:
                info['pairable'] = 'yes' in line.lower()
        
        return info
    
    def set_adapter_power(self, power_on: bool) -> Tuple[bool, str]:
        """
        Power on/off the Bluetooth adapter
        
        Args:
            power_on: True to power on, False to power off
            
        Returns:
            Tuple of (success, message)
        """
        command = 'power on' if power_on else 'power off'
        returncode, stdout, stderr = self.execute_command(command)
        
        if returncode == 0:
            status = "on" if power_on else "off"
            return True, f"Adapter powered {status}"
        else:
            return False, self._parse_error(stderr)
    
    async def start_scan_async(self, callback: Callable[[Dict], None]) -> None:
        """
        Start Bluetooth scanning and call callback with discovered devices
        
        Args:
            callback: Async function to call with device updates
        """
        if self.scanning:
            return
        
        self.scanning = True
        
        try:
            # Start scan process
            process = await asyncio.create_subprocess_exec(
                'bluetoothctl', 'scan', 'on',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            self.scan_process = process
            
            # Read output line by line
            while self.scanning:
                line = await process.stdout.readline()
                if not line:
                    break
                
                line = line.decode('utf-8').strip()
                
                # Parse device discovery
                match = self.DEVICE_NEW_PATTERN.search(line)
                if match:
                    mac, name = match.groups()
                    await callback({
                        'type': 'discovered',
                        'mac': mac,
                        'name': name,
                        'discovered_at': datetime.now().isoformat()
                    })
                
                # Parse RSSI updates
                if self.DEVICE_CHG_PATTERN.search(line):
                    mac_match = self.DEVICE_CHG_PATTERN.search(line)
                    rssi_match = self.RSSI_PATTERN.search(line)
                    if mac_match and rssi_match:
                        mac = mac_match.group(1)
                        rssi_int = rssi_match.group(2)
                        await callback({
                            'type': 'rssi_update',
                            'mac': mac,
                            'rssi': int(rssi_int)
                        })
        
        except Exception as e:
            print(f"Scan error: {e}")
        finally:
            if self.scan_process:
                self.scan_process.terminate()
    
    def stop_scan(self) -> Tuple[bool, str]:
        """
        Stop Bluetooth scanning
        
        Returns:
            Tuple of (success, message)
        """
        if not self.scanning:
            return True, "Scan already stopped"
        
        self.scanning = False
        
        if self.scan_process:
            self.scan_process.terminate()
            self.scan_process = None
        
        # Also send bluetoothctl command
        returncode, stdout, stderr = self.execute_command('scan off')
        
        if returncode == 0:
            return True, "Scan stopped"
        else:
            return False, self._parse_error(stderr)
    
    def get_devices(self) -> List[Dict]:
        """
        Get list of all known devices
        
        Returns:
            List of device dictionaries
        """
        returncode, stdout, stderr = self.execute_command('devices')
        
        devices = []
        for line in stdout.split('\n'):
            # Format: "Device MAC_ADDRESS NAME"
            match = re.search(r'Device ([0-9A-F:]{17}) (.+)', line)
            if match:
                mac, name = match.groups()
                devices.append({
                    'mac': mac,
                    'name': name.strip()
                })
        
        return devices
    
    def get_device_info(self, mac_address: str) -> Dict:
        """
        Get detailed information about a device
        
        Args:
            mac_address: MAC address of the device
            
        Returns:
            Dictionary with device information
        """
        returncode, stdout, stderr = self.execute_command(f'info {mac_address}')
        
        if returncode != 0:
            return {'error': self._parse_error(stderr)}
        
        info = {'mac': mac_address}
        
        for key, pattern in self.INFO_PATTERNS.items():
            for line in stdout.split('\n'):
                match = pattern.search(line)
                if match:
                    value = match.group(1)
                    if key in ['paired', 'bonded', 'trusted', 'blocked', 'connected']:
                        info[key] = value.lower() == 'yes'
                    elif key in ['battery', 'rssi']:
                        info[key] = int(value)
                    else:
                        info[key] = value
                    break
        
        # Extract UUIDs
        info['uuids'] = []
        in_uuid_section = False
        for line in stdout.split('\n'):
            if 'UUID:' in line:
                in_uuid_section = True
                uuid_match = re.search(r'UUID: (.+?) \((.+?)\)', line)
                if uuid_match:
                    info['uuids'].append({
                        'uuid': uuid_match.group(1),
                        'name': uuid_match.group(2)
                    })
            elif in_uuid_section and line.strip() and not line.startswith('\t'):
                in_uuid_section = False
        
        return info
    
    def pair_device(self, mac_address: str) -> Tuple[bool, str]:
        """
        Pair with a device
        
        Args:
            mac_address: MAC address of the device
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = self.execute_command(f'pair {mac_address}', timeout=60)
        
        if returncode == 0 or 'Pairing successful' in stdout:
            return True, "Device paired successfully"
        else:
            return False, self._parse_error(stderr + stdout)
    
    def trust_device(self, mac_address: str) -> Tuple[bool, str]:
        """
        Trust a device (allow auto-reconnection)
        
        Args:
            mac_address: MAC address of the device
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = self.execute_command(f'trust {mac_address}')
        
        if returncode == 0:
            return True, "Device trusted"
        else:
            return False, self._parse_error(stderr)
    
    def untrust_device(self, mac_address: str) -> Tuple[bool, str]:
        """
        Untrust a device
        
        Args:
            mac_address: MAC address of the device
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = self.execute_command(f'untrust {mac_address}')
        
        if returncode == 0:
            return True, "Device untrusted"
        else:
            return False, self._parse_error(stderr)
    
    def connect_device(self, mac_address: str) -> Tuple[bool, str]:
        """
        Connect to a device
        
        Args:
            mac_address: MAC address of the device
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = self.execute_command(f'connect {mac_address}', timeout=60)
        
        if returncode == 0 or 'Connection successful' in stdout:
            return True, "Connected successfully"
        else:
            return False, self._parse_error(stderr + stdout)
    
    def disconnect_device(self, mac_address: str) -> Tuple[bool, str]:
        """
        Disconnect from a device
        
        Args:
            mac_address: MAC address of the device
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = self.execute_command(f'disconnect {mac_address}')
        
        if returncode == 0 or 'Successful disconnected' in stdout:
            return True, "Disconnected successfully"
        else:
            return False, self._parse_error(stderr + stdout)
    
    def remove_device(self, mac_address: str) -> Tuple[bool, str]:
        """
        Remove a device (unpair)
        
        Args:
            mac_address: MAC address of the device
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = self.execute_command(f'remove {mac_address}')
        
        if returncode == 0:
            return True, "Device removed"
        else:
            return False, self._parse_error(stderr)
    
    def _parse_error(self, error_output: str) -> str:
        """
        Convert bluetoothctl errors to user-friendly messages
        
        Args:
            error_output: Error output from bluetoothctl
            
        Returns:
            User-friendly error message
        """
        error_lower = error_output.lower()
        
        if "page timeout" in error_lower or "page-timeout" in error_lower:
            return "Device not found or not responding. Make sure the device is in pairing mode and nearby."
        elif "already exists" in error_lower or "already paired" in error_lower:
            return "Device is already paired."
        elif "not ready" in error_lower:
            return "Bluetooth adapter not ready. Try powering it off and on again."
        elif "not available" in error_lower:
            return "Device not available. Make sure it's powered on."
        elif "connection refused" in error_lower:
            return "Connection refused by device."
        elif "authentication failed" in error_lower:
            return "Authentication failed. Try removing and re-pairing the device."
        elif "failed" in error_lower:
            return f"Operation failed: {error_output[:100]}"
        elif error_output:
            return error_output[:200]
        else:
            return "Unknown error occurred"
