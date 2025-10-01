/**
 * Bluetooth Manager Application
 * Main application logic and UI management
 */

class BluetoothManager {
    constructor() {
        // Get base path for ingress support (e.g., /api/hassio_ingress/...)
        const basePath = window.location.pathname.replace(/\/+$/, '').replace(/\/index\.html$/, '');
        this.api = new BluetoothAPI(basePath);
        this.pairedDevices = new Map();
        this.discoveredDevices = new Map();
        this.scanning = false;
        this.currentAdapter = null;
        this.currentDeviceMac = null;
        this.statusCheckInterval = null;
        
        console.log('Base path:', basePath);
        
        this.init();
    }

    async init() {
        console.log('Initializing Bluetooth Manager...');
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Connect WebSocket
        this.api.connectWebSocket(this.handleWebSocketMessage.bind(this));
        
        // Start ping interval
        setInterval(() => this.api.sendPing(), 30000);
        
        // Load initial data
        await this.loadAdapterInfo();
        await this.loadPairedDevices();
        
        // Start periodic status check for paired devices (every 5 seconds)
        this.statusCheckInterval = setInterval(() => {
            if (!this.scanning) {
                this.loadPairedDevices();
            }
        }, 5000);
    }

    setupEventListeners() {
        // Scan button
        document.getElementById('scan-btn').addEventListener('click', () => {
            this.toggleScan();
        });

        // Power toggle
        document.getElementById('power-toggle').addEventListener('click', () => {
            this.togglePower();
        });

        // Refresh paired devices
        document.getElementById('refresh-paired').addEventListener('click', () => {
            this.loadPairedDevices();
        });

        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.closest('.tab-btn').dataset.tab);
            });
        });

        // Filter audio devices
        document.getElementById('filter-audio').addEventListener('change', () => {
            this.renderDiscoveredDevices();
        });

        // Modal close
        document.querySelector('.modal-close').addEventListener('click', () => {
            this.closeModal();
        });
        document.getElementById('modal-close-btn').addEventListener('click', () => {
            this.closeModal();
        });

        // Modal actions
        document.getElementById('modal-connect-btn').addEventListener('click', () => {
            this.modalConnect();
        });
        document.getElementById('modal-disconnect-btn').addEventListener('click', () => {
            this.modalDisconnect();
        });
        document.getElementById('modal-trust-btn').addEventListener('click', () => {
            this.toggleTrust();
        });
        document.getElementById('modal-remove-btn').addEventListener('click', () => {
            this.removeDeviceFromModal();
        });

        // Close modal on background click
        document.getElementById('device-modal').addEventListener('click', (e) => {
            if (e.target.id === 'device-modal') {
                this.closeModal();
            }
        });
    }

    // Adapter Management
    async loadAdapterInfo() {
        try {
            const adapters = await this.api.getAdapters();
            if (adapters.length === 0) {
                this.showToast('No Bluetooth adapter found', 'error');
                return;
            }
            
            const adapterId = adapters[0].id;
            const info = await this.api.getAdapterInfo(adapterId);
            this.currentAdapter = info;  // Store the full adapter info
            
            const adapterName = document.getElementById('adapter-name');
            adapterName.textContent = info.alias || info.name || 'Bluetooth Adapter';
            
            const powerBtn = document.getElementById('power-toggle');
            // Check powered status from info
            if (info.powered === true || info.powered === 'yes') {
                powerBtn.classList.add('active');
                powerBtn.innerHTML = '<i class="fas fa-power-off"></i> Power Off';
            } else {
                powerBtn.classList.remove('active');
                powerBtn.innerHTML = '<i class="fas fa-power-off"></i> Power On';
            }
        } catch (error) {
            this.showToast('Failed to load adapter info', 'error');
            console.error('Error loading adapter:', error);
        }
    }

    async togglePower() {
        const isOn = this.currentAdapter?.powered === true || this.currentAdapter?.powered === 'yes';
        
        try {
            this.showLoading('Toggling power...');
            await this.api.setAdapterPower(!isOn);
            await this.loadAdapterInfo();  // This will update currentAdapter
            this.showToast(`Adapter powered ${!isOn ? 'on' : 'off'}`, 'success');
        } catch (error) {
            this.showToast(`Failed to toggle power: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async togglePower() {
        const isOn = this.currentAdapter?.powered || false;
        
        try {
            this.showLoading('Toggling power...');
            await this.api.setAdapterPower(!isOn);
            await this.loadAdapterInfo();
            this.showToast(`Adapter powered ${!isOn ? 'on' : 'off'}`, 'success');
        } catch (error) {
            this.showToast(`Failed to toggle power: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }

    // Scanning
    async toggleScan() {
        if (this.scanning) {
            await this.stopScan();
        } else {
            await this.startScan();
        }
    }

    async startScan() {
        try {
            await this.api.startScan();
            this.scanning = true;
            this.updateScanButton();
            this.discoveredDevices.clear();
            this.renderDiscoveredDevices();
            this.showToast('Scanning started (will auto-stop after 30s)', 'info');
            
            // Auto-switch to discovered tab
            this.switchTab('discovered');
            
            // Auto-stop scan after 30 seconds
            setTimeout(async () => {
                if (this.scanning) {
                    await this.stopScan();
                    this.showToast('Scan completed', 'success');
                }
            }, 30000);
        } catch (error) {
            this.showToast(`Failed to start scan: ${error.message}`, 'error');
        }
    }

    async stopScan() {
        try {
            await this.api.stopScan();
            this.scanning = false;
            this.updateScanButton();
            this.renderDiscoveredDevices();  // Update UI to remove scanning message
            this.showToast('Scanning stopped', 'info');
        } catch (error) {
            this.showToast(`Failed to stop scan: ${error.message}`, 'error');
        }
    }

    updateScanButton() {
        const btn = document.getElementById('scan-btn');
        const status = document.getElementById('scan-status');
        
        if (this.scanning) {
            btn.innerHTML = '<i class="fas fa-stop"></i> Stop Scan';
            btn.classList.add('active');
            status.classList.remove('hidden');
        } else {
            btn.innerHTML = '<i class="fas fa-search"></i> Start Scan';
            btn.classList.remove('active');
            status.classList.add('hidden');
        }
    }

    // Device Management
    async loadPairedDevices() {
        const refreshBtn = document.getElementById('refresh-paired');
        try {
            // Add loading indicator
            refreshBtn.innerHTML = '<i class="fas fa-sync fa-spin"></i>';
            refreshBtn.disabled = true;
            
            const response = await this.api.getDevices();
            this.pairedDevices.clear();
            
            for (const device of response.devices) {
                if (device.paired) {
                    this.pairedDevices.set(device.mac, device);
                }
            }
            
            this.renderPairedDevices();
        } catch (error) {
            this.showToast('Failed to load devices', 'error');
            console.error('Error loading devices:', error);
        } finally {
            // Restore button
            refreshBtn.innerHTML = '<i class="fas fa-sync"></i>';
            refreshBtn.disabled = false;
        }
    }

    async pairAndConnect(mac) {
        try {
            this.showLoading('Pairing device...');
            
            // Pair
            await this.api.pairDevice(mac);
            
            // Trust
            await this.api.trustDevice(mac);
            
            // Connect
            await this.api.connectDevice(mac);
            
            // Reload devices
            await this.loadPairedDevices();
            
            this.showToast('Device paired and connected!', 'success');
        } catch (error) {
            this.showToast(`Failed to pair: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async connectDevice(mac) {
        try {
            this.showLoading('Connecting...');
            await this.api.connectDevice(mac);
            await this.loadPairedDevices();
        } catch (error) {
            this.showToast(`Failed to connect: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async disconnectDevice(mac) {
        try {
            this.showLoading('Disconnecting...');
            await this.api.disconnectDevice(mac);
            await this.loadPairedDevices();
        } catch (error) {
            this.showToast(`Failed to disconnect: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async removeDevice(mac) {
        // Show custom confirmation modal instead of native alert
        this.showConfirmation(
            'Remove Device',
            'Are you sure you want to remove this device? This will unpair the device.',
            async () => {
                try {
                    this.showLoading('Removing device...');
                    await this.api.removeDevice(mac);
                    this.pairedDevices.delete(mac);
                    this.renderPairedDevices();
                    this.showToast('Device removed', 'success');
                } catch (error) {
                    this.showToast(`Failed to remove: ${error.message}`, 'error');
                } finally {
                    this.hideLoading();
                }
            }
        );
    }

    async showDeviceInfo(mac) {
        try {
            this.currentDeviceMac = mac;
            
            // Show modal immediately with loading state
            const modal = document.getElementById('device-modal');
            const body = document.getElementById('modal-body');
            modal.classList.remove('hidden');
            body.innerHTML = '<div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i> Loading device information...</div>';
            
            // Then load data
            const info = await this.api.getDeviceInfo(mac);
            this.displayDeviceModal(info);
        } catch (error) {
            this.closeModal();
            this.showToast(`Failed to get device info: ${error.message}`, 'error');
        }
    }

    // WebSocket Message Handler
    handleWebSocketMessage(data) {
        console.log('WebSocket message:', data);
        
        switch (data.type) {
            case 'discovered':
                this.discoveredDevices.set(data.mac, {
                    mac: data.mac,
                    name: data.name,
                    discovered_at: data.discovered_at,
                    rssi: null
                });
                this.renderDiscoveredDevices();
                break;
                
            case 'rssi_update':
                const device = this.discoveredDevices.get(data.mac);
                if (device) {
                    device.rssi = data.rssi;
                    this.renderDiscoveredDevices();
                }
                break;
                
            case 'device_connected':
                this.showToast(`Connected to ${data.name}`, 'success');
                this.loadPairedDevices();
                break;
                
            case 'device_disconnected':
                this.showToast('Device disconnected', 'info');
                this.loadPairedDevices();
                break;
                
            case 'device_paired':
                this.showToast(data.message, 'success');
                this.loadPairedDevices();
                break;
                
            case 'device_removed':
                this.showToast(data.message, 'success');
                this.loadPairedDevices();
                break;
        }
    }

    // UI Rendering
    renderPairedDevices() {
        const container = document.getElementById('paired-list');
        
        if (this.pairedDevices.size === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-bluetooth-b"></i>
                    <p>No paired devices</p>
                    <small>Scan for devices to pair with them</small>
                </div>
            `;
            return;
        }
        
        // Sort: connected first, then by name
        const devices = Array.from(this.pairedDevices.values()).sort((a, b) => {
            if (a.connected !== b.connected) {
                return b.connected ? 1 : -1;
            }
            return (a.name || a.mac).localeCompare(b.name || b.mac);
        });
        
        container.innerHTML = devices.map(device => this.createDeviceCard(device, true)).join('');
        
        // Add event listeners
        devices.forEach(device => {
            // Connect/Disconnect
            const connectBtn = container.querySelector(`[data-action="connect"][data-mac="${device.mac}"]`);
            if (connectBtn) {
                connectBtn.addEventListener('click', () => {
                    if (device.connected) {
                        this.disconnectDevice(device.mac);
                    } else {
                        this.connectDevice(device.mac);
                    }
                });
            }
            
            // Remove
            const removeBtn = container.querySelector(`[data-action="remove"][data-mac="${device.mac}"]`);
            if (removeBtn) {
                removeBtn.addEventListener('click', () => this.removeDevice(device.mac));
            }
            
            // Info
            const infoBtn = container.querySelector(`[data-action="info"][data-mac="${device.mac}"]`);
            if (infoBtn) {
                infoBtn.addEventListener('click', () => this.showDeviceInfo(device.mac));
            }
        });
    }

    renderDiscoveredDevices() {
        const container = document.getElementById('discovered-list');
        const filterAudio = document.getElementById('filter-audio').checked;
        
        if (this.discoveredDevices.size === 0) {
            const message = this.scanning ? 
                'Scanning for devices...' : 
                'No devices discovered yet';
            const detail = this.scanning ? 
                'Waiting for nearby Bluetooth devices...' : 
                'Click "Start Scan" to discover nearby devices';
                
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-${this.scanning ? 'spinner fa-spin' : 'search'}"></i>
                    <p>${message}</p>
                    <small>${detail}</small>
                </div>
            `;
            return;
        }
        
        // Filter and sort by RSSI (strongest first)
        let devices = Array.from(this.discoveredDevices.values());
        
        if (filterAudio) {
            devices = devices.filter(d => this.isAudioDevice(d.name));
        }
        
        devices.sort((a, b) => (b.rssi || -100) - (a.rssi || -100));
        
        if (devices.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-headphones"></i>
                    <p>No audio devices found</p>
                    <small>Try disabling the audio filter</small>
                </div>
            `;
            return;
        }
        
        container.innerHTML = devices.map(device => this.createDeviceCard(device, false)).join('');
        
        // Add event listeners
        devices.forEach(device => {
            const pairBtn = container.querySelector(`[data-action="pair"][data-mac="${device.mac}"]`);
            if (pairBtn) {
                pairBtn.addEventListener('click', () => this.pairAndConnect(device.mac));
            }
        });
    }

    createDeviceCard(device, isPaired) {
        const icon = this.getDeviceIcon(device.name, isPaired ? device.connected : null);
        const signalBars = this.getSignalBars(device.rssi);
        
        if (isPaired) {
            const statusClass = device.connected ? 'connected' : 'disconnected';
            const statusText = device.connected ? 'Connected' : 'Disconnected';
            const actionIcon = device.connected ? 'unlink' : 'link';
            const actionText = device.connected ? 'Disconnect' : 'Connect';
            
            return `
                <div class="device-card ${statusClass}">
                    <div class="device-icon">${icon}</div>
                    <div class="device-info">
                        <div class="device-name">${device.name || device.mac}</div>
                        <div class="device-mac">${device.mac}</div>
                        <div class="device-status status-${statusClass}">${statusText}</div>
                    </div>
                    <div class="device-actions">
                        <button class="btn btn-sm btn-primary" data-action="connect" data-mac="${device.mac}">
                            <i class="fas fa-${actionIcon}"></i> ${actionText}
                        </button>
                        <button class="btn btn-sm btn-secondary" data-action="info" data-mac="${device.mac}">
                            <i class="fas fa-info-circle"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" data-action="remove" data-mac="${device.mac}">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `;
        } else {
            return `
                <div class="device-card discovered">
                    <div class="device-icon">${icon}</div>
                    <div class="device-info">
                        <div class="device-name">${device.name || device.mac}</div>
                        <div class="device-mac">${device.mac}</div>
                        ${device.rssi ? `<div class="device-signal">${signalBars} ${device.rssi} dBm</div>` : ''}
                    </div>
                    <div class="device-actions">
                        <button class="btn btn-sm btn-primary" data-action="pair" data-mac="${device.mac}">
                            <i class="fas fa-plus"></i> Pair & Connect
                        </button>
                    </div>
                </div>
            `;
        }
    }

    getDeviceIcon(name, isConnected) {
        // Use SVG icons for device types
        const svgStyle = 'width: 32px; height: 32px;';
        
        // For paired devices, use connection-specific icons
        if (isConnected !== null && isConnected !== undefined) {
            if (isConnected) {
                // Connected: blue signal icon
                return `<svg xmlns="http://www.w3.org/2000/svg" style="${svgStyle}" viewBox="0 0 24 24" fill="#4CAF50"><path d="M17.71 7.71L12 2h-1v7.59L6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 11 14.41V22h1l5.71-5.71-4.3-4.29 4.3-4.29zM13 5.83l1.88 1.88L13 9.59V5.83zm1.88 10.46L13 18.17v-3.76l1.88 1.88z"/><circle cx="16" cy="12" r="1.5"/><circle cx="20" cy="12" r="1"/></svg>`;
            } else {
                // Disconnected: red slash icon
                return `<svg xmlns="http://www.w3.org/2000/svg" style="${svgStyle}" viewBox="0 0 24 24" fill="#f44336"><path d="M13 5.83l1.88 1.88L13 9.59V5.83zm5.71 1.88L12 2h-1v7.59L6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 11 14.41V22h1l5.71-5.71-4.3-4.29 4.3-4.29zM13 18.17v-3.76l1.88 1.88-1.88 1.88z"/><path d="M2 2L22 22" stroke="red" stroke-width="2"/></svg>`;
            }
        }
        
        // For discovered devices: blue-on icon
        return `<svg xmlns="http://www.w3.org/2000/svg" style="${svgStyle}" viewBox="0 0 24 24" fill="#2196F3"><path d="M17.71 7.71L12 2h-1v7.59L6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 11 14.41V22h1l5.71-5.71-4.3-4.29 4.3-4.29zM13 5.83l1.88 1.88L13 9.59V5.83zm1.88 10.46L13 18.17v-3.76l1.88 1.88z"/></svg>`;
    }

    isAudioDevice(name) {
        if (!name) return false;
        const nameLower = name.toLowerCase();
        return nameLower.includes('headphone') || 
               nameLower.includes('headset') || 
               nameLower.includes('speaker') || 
               nameLower.includes('sound') ||
               nameLower.includes('audio') ||
               nameLower.includes('music');
    }

    getSignalBars(rssi) {
        if (!rssi) return '';
        
        if (rssi >= -50) return '<i class="fas fa-signal"></i>';
        if (rssi >= -60) return '<i class="fas fa-signal"></i>';
        if (rssi >= -70) return '<i class="fas fa-signal"></i>';
        return '<i class="fas fa-signal"></i>';
    }

    // Modal
    displayDeviceModal(info) {
        this.currentDeviceInfo = info;
        
        const modal = document.getElementById('device-modal');
        const body = document.getElementById('modal-body');
        
        const trustBtn = document.getElementById('modal-trust-btn');
        trustBtn.innerHTML = info.trusted ? 
            '<i class="fas fa-shield-alt"></i> Untrust' : 
            '<i class="fas fa-shield-alt"></i> Trust';
        
        body.innerHTML = `
            <div class="device-detail">
                <div class="detail-row">
                    <label>Name:</label>
                    <span>${info.name || 'Unknown'}</span>
                </div>
                <div class="detail-row">
                    <label>MAC Address:</label>
                    <span>${info.mac}</span>
                </div>
                <div class="detail-row">
                    <label>Paired:</label>
                    <span class="badge ${info.paired ? 'badge-success' : 'badge-secondary'}">
                        ${info.paired ? 'Yes' : 'No'}
                    </span>
                </div>
                <div class="detail-row">
                    <label>Connected:</label>
                    <span class="badge ${info.connected ? 'badge-success' : 'badge-secondary'}">
                        ${info.connected ? 'Yes' : 'No'}
                    </span>
                </div>
                <div class="detail-row">
                    <label>Trusted:</label>
                    <span class="badge ${info.trusted ? 'badge-success' : 'badge-secondary'}">
                        ${info.trusted ? 'Yes' : 'No'}
                    </span>
                </div>
                ${info.battery ? `
                <div class="detail-row">
                    <label>Battery:</label>
                    <span><i class="fas fa-battery-three-quarters"></i> ${info.battery}%</span>
                </div>
                ` : ''}
                ${info.rssi ? `
                <div class="detail-row">
                    <label>Signal Strength:</label>
                    <span>${info.rssi} dBm</span>
                </div>
                ` : ''}
                ${info.icon ? `
                <div class="detail-row">
                    <label>Device Type:</label>
                    <span>${info.icon}</span>
                </div>
                ` : ''}
                ${info.uuids && info.uuids.length > 0 ? `
                <div class="detail-row">
                    <label>Supported Profiles:</label>
                    <div class="profile-list">
                        ${info.uuids.map(u => `<span class="badge badge-info">${u.name}</span>`).join('')}
                    </div>
                </div>
                ` : ''}
            </div>
        `;
        
        // Show/hide connect/disconnect buttons based on connection state
        const connectBtn = document.getElementById('modal-connect-btn');
        const disconnectBtn = document.getElementById('modal-disconnect-btn');
        
        if (info.paired) {
            if (info.connected) {
                connectBtn.style.display = 'none';
                disconnectBtn.style.display = 'inline-block';
            } else {
                connectBtn.style.display = 'inline-block';
                disconnectBtn.style.display = 'none';
            }
        } else {
            connectBtn.style.display = 'none';
            disconnectBtn.style.display = 'none';
        }
        
        modal.classList.remove('hidden');
    }

    closeModal() {
        document.getElementById('device-modal').classList.add('hidden');
        this.currentDeviceMac = null;
        this.currentDeviceInfo = null;
    }

    async modalConnect() {
        if (!this.currentDeviceMac) return;
        
        try {
            this.showLoading('Connecting...');
            await this.api.connectDevice(this.currentDeviceMac);
            this.showToast('Connected successfully', 'success');
            // Reload device info to update the modal
            await this.showDeviceInfo(this.currentDeviceMac);
            await this.loadPairedDevices();
        } catch (error) {
            this.showToast(`Failed to connect: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async modalDisconnect() {
        if (!this.currentDeviceMac) return;
        
        try {
            this.showLoading('Disconnecting...');
            await this.api.disconnectDevice(this.currentDeviceMac);
            this.showToast('Disconnected successfully', 'success');
            // Reload device info to update the modal
            await this.showDeviceInfo(this.currentDeviceMac);
            await this.loadPairedDevices();
        } catch (error) {
            this.showToast(`Failed to disconnect: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async toggleTrust() {
        if (!this.currentDeviceMac) return;
        
        try {
            const isTrusted = this.currentDeviceInfo?.trusted || false;
            
            if (isTrusted) {
                await this.api.untrustDevice(this.currentDeviceMac);
                this.showToast('Device untrusted', 'success');
            } else {
                await this.api.trustDevice(this.currentDeviceMac);
                this.showToast('Device trusted', 'success');
            }
            
            // Refresh device info
            await this.showDeviceInfo(this.currentDeviceMac);
        } catch (error) {
            this.showToast(`Failed: ${error.message}`, 'error');
        }
    }

    async removeDeviceFromModal() {
        if (!this.currentDeviceMac) return;
        
        this.closeModal();
        await this.removeDevice(this.currentDeviceMac);
    }

    // Tab Switching
    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            if (btn.dataset.tab === tabName) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            if (content.id === `${tabName}-devices`) {
                content.classList.add('active');
            } else {
                content.classList.remove('active');
            }
        });
    }

    // UI Helpers
    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        const icon = toast.querySelector('.toast-icon');
        const msg = toast.querySelector('.toast-message');
        
        // Set icon based on type
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            info: 'fa-info-circle',
            warning: 'fa-exclamation-triangle'
        };
        
        icon.className = `toast-icon fas ${icons[type] || icons.info}`;
        msg.textContent = message;
        toast.className = `toast toast-${type}`;
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            toast.classList.add('hidden');
        }, 5000);
    }

    showLoading(text = 'Processing...') {
        const overlay = document.getElementById('loading-overlay');
        const loadingText = document.getElementById('loading-text');
        loadingText.textContent = text;
        overlay.classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loading-overlay').classList.add('hidden');
    }
    
    showConfirmation(title, message, onConfirm) {
        // Create confirmation modal dynamically
        const existingModal = document.getElementById('confirm-modal');
        if (existingModal) existingModal.remove();
        
        const modal = document.createElement('div');
        modal.id = 'confirm-modal';
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content" style="max-width: 400px;">
                <div class="modal-header">
                    <h2>${title}</h2>
                </div>
                <div class="modal-body">
                    <p>${message}</p>
                </div>
                <div class="modal-footer" style="display: flex; gap: 10px; justify-content: flex-end;">
                    <button class="btn btn-secondary" id="confirm-cancel">Cancel</button>
                    <button class="btn btn-danger" id="confirm-ok">Remove</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        modal.classList.remove('hidden');
        
        document.getElementById('confirm-cancel').addEventListener('click', () => {
            modal.remove();
        });
        
        document.getElementById('confirm-ok').addEventListener('click', () => {
            modal.remove();
            onConfirm();
        });
        
        // Close on background click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.bluetoothManager = new BluetoothManager();
});
