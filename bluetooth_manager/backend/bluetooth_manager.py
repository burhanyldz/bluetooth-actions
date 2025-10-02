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
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            logger.info(f"Executing bluetoothctl command: {command}")
            
            # Use echo piping for non-interactive commands
            process = subprocess.Popen(
                ['bluetoothctl'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=subprocess.os.environ.copy()
            )
            
            # Send command and exit
            stdout, stderr = process.communicate(
                input=f"{command}\nexit\n",
                timeout=timeout
            )
            
            logger.info(f"Command '{command}' - Return code: {process.returncode}")
            logger.debug(f"Command '{command}' - Stdout: {stdout[:200]}")
            if stderr:
                logger.warning(f"Command '{command}' - Stderr: {stderr[:200]}")
            
            return process.returncode, stdout, stderr
        except subprocess.TimeoutExpired:
            logger.error(f"Command '{command}' timed out after {timeout}s")
            process.kill()
            return -1, "", "Command timed out"
        except Exception as e:
            logger.error(f"Command '{command}' failed with exception: {e}")
            return -1, "", str(e)
    
    def list_adapters(self) -> List[Dict]:
        """
        Get list of Bluetooth adapters
        
        Returns:
            List of adapter dictionaries with 'id', 'name', 'mac' keys
        """
        import logging
        logger = logging.getLogger(__name__)
        
        returncode, stdout, stderr = self.execute_command('list')
        logger.info(f"list_adapters - Found output length: {len(stdout)} chars")
        
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
        import logging
        logger = logging.getLogger(__name__)
        
        cmd = f'show {adapter_id}' if adapter_id else 'show'
        returncode, stdout, stderr = self.execute_command(cmd)
        logger.info(f"get_adapter_info - Output: {stdout[:300]}")
        
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
        import logging
        logger = logging.getLogger(__name__)
        
        command = 'power on' if power_on else 'power off'
        logger.info(f"Setting adapter power: {command}")
        returncode, stdout, stderr = self.execute_command(command)
        
        logger.info(f"set_adapter_power result - returncode: {returncode}, stdout: {stdout}, stderr: {stderr}")
        
        if returncode == 0 or "succeeded" in stdout.lower() or "changing" in stdout.lower():
            status = "on" if power_on else "off"
            return True, f"Adapter powered {status}"
        else:
            error_msg = self._parse_error(stderr) if stderr else stdout
            logger.error(f"Power command failed: {error_msg}")
            return False, error_msg
    
    async def start_scan_async(self, callback: Callable[[Dict], None]) -> None:
        """
        Start Bluetooth scanning and call callback with discovered devices
        
        Args:
            callback: Async function to call with device updates
        """
        import logging
        logger = logging.getLogger(__name__)
        
        if self.scanning:
            logger.warning("Scan already running")
            return
        
        self.scanning = True
        logger.info("Starting Bluetooth scan...")
        
        # Start scan with regular bluetoothctl command
        returncode, stdout, stderr = self.execute_command('scan on')
        if returncode != 0 and "failed" in stderr.lower():
            logger.error(f"Failed to start scan: {stderr}")
            self.scanning = False
            return
        
        logger.info("Scan started successfully")
        
        # Keep track of seen devices
        seen_devices = set()
        scan_start_time = asyncio.get_event_loop().time()
        max_scan_duration = 60  # 60 seconds max scan
        
        try:
            while self.scanning:
                # Check if scan duration exceeded
                if asyncio.get_event_loop().time() - scan_start_time > max_scan_duration:
                    logger.info("Scan duration limit reached (60s), stopping...")
                    self.scanning = False
                    break
                
                # Get current devices list
                devices = self.get_devices()
                
                for device in devices:
                    mac = device['mac']
                    if mac not in seen_devices:
                        seen_devices.add(mac)
                        logger.info(f"Discovered device: {mac} - {device['name']}")
                        
                        # Get device info to check if it's paired
                        info = self.get_device_info(mac)
                        
                        # Only send unpaired devices as "discovered"
                        if not info.get('paired', False):
                            await callback({
                                'type': 'discovered',
                                'mac': mac,
                                'name': device['name'],
                                'rssi': info.get('rssi'),
                                'discovered_at': datetime.now().isoformat()
                            })
                
                # Wait a bit before next poll
                await asyncio.sleep(2)
                
        except Exception as e:
            logger.error(f"Scan error: {e}")
        finally:
            logger.info("Stopping scan...")
            # Stop scan
            returncode, stdout, stderr = self.execute_command('scan off')
            if returncode == 0:
                logger.info("Scan stopped successfully")
            else:
                logger.error(f"Error stopping scan: {stderr}")
            self.scanning = False
            logger.info("Scan complete")
    
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
            try:
                # Try to gracefully stop
                self.scan_process.terminate()
            except:
                pass
            self.scan_process = None
        
        return True, "Scan stopped"
    
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
        import time
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"Attempting to pair with device: {mac_address}")
        returncode, stdout, stderr = self.execute_command(f'pair {mac_address}', timeout=60)
        
        logger.info(f"Pair command result - returncode: {returncode}, stdout: {stdout}, stderr: {stderr}")
        
        if returncode == 0 or 'Pairing successful' in stdout or 'already paired' in stdout.lower():
            # Wait for pairing to settle
            logger.info("Pairing successful, waiting 2 seconds for state to settle...")
            time.sleep(2)
            return True, "Device paired successfully"
        else:
            error_msg = self._parse_error(stderr + stdout)
            logger.error(f"Pairing failed: {error_msg}")
            return False, error_msg
    
    def trust_device(self, mac_address: str) -> Tuple[bool, str]:
        """
        Trust a device (allow auto-reconnection)
        
        Args:
            mac_address: MAC address of the device
            
        Returns:
            Tuple of (success, message)
        """
        import time
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"Trusting device: {mac_address}")
        returncode, stdout, stderr = self.execute_command(f'trust {mac_address}')
        
        logger.info(f"Trust command result - returncode: {returncode}, stdout: {stdout}, stderr: {stderr}")
        
        if returncode == 0 or 'trust succeeded' in stdout.lower():
            # Small delay for trust to settle
            time.sleep(1)
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
        import time
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"Connecting to device: {mac_address}")
        returncode, stdout, stderr = self.execute_command(f'connect {mac_address}', timeout=60)
        
        logger.info(f"Connect command result - returncode: {returncode}, stdout: {stdout}, stderr: {stderr}")
        
        if returncode == 0 or 'Connection successful' in stdout or 'Connected: yes' in stdout:
            # Wait for connection to fully establish
            time.sleep(2)
            return True, "Connected successfully"
        else:
            error_msg = self._parse_error(stderr + stdout)
            logger.error(f"Connection failed: {error_msg}")
            return False, error_msg
    
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
        import time
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"Removing device: {mac_address}")
        
        # First disconnect if connected
        device_info = self.get_device_info(mac_address)
        if device_info.get('connected', False):
            logger.info(f"Device is connected, disconnecting first...")
            self.disconnect_device(mac_address)
            time.sleep(1)
        
        returncode, stdout, stderr = self.execute_command(f'remove {mac_address}')
        
        logger.info(f"Remove command result - returncode: {returncode}, stdout: {stdout}, stderr: {stderr}")
        
        if returncode == 0 or 'Device has been removed' in stdout:
            # Wait for removal to settle
            time.sleep(1)
            return True, "Device removed"
        else:
            error_msg = self._parse_error(stderr)
            logger.error(f"Remove failed: {error_msg}")
            return False, error_msg
    
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
