/**
 * Bluetooth Manager API Client
 * Handles all communication with the backend API
 */

class BluetoothAPI {
    constructor(baseURL = '') {
        this.baseURL = baseURL;
        this.ws = null;
        this.wsReconnectInterval = null;
        this.onMessageCallback = null;
    }

    /**
     * Make a fetch request with error handling
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        console.log('API Request:', url, options.method || 'GET');
        
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: `HTTP ${response.status}` }));
                console.error('API Error:', url, response.status, error);
                throw new Error(error.detail || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error (${url}):`, error);
            throw error;
        }
    }

    // Adapter endpoints
    async getAdapters() {
        const response = await this.request('/api/adapters');
        // Backend returns {adapters: [...]}
        return response.adapters || [];
    }

    async getAdapterInfo(adapterId = 'default') {
        return this.request(`/api/adapters/${adapterId}/info`);
    }

    async setAdapterPower(powerOn) {
        return this.request('/api/adapters/power', {
            method: 'POST',
            body: JSON.stringify({ power_on: powerOn })
        });
    }

    // Scan endpoints
    async startScan() {
        return this.request('/api/scan/start', { method: 'POST' });
    }

    async stopScan() {
        return this.request('/api/scan/stop', { method: 'POST' });
    }

    async getScanStatus() {
        return this.request('/api/scan/status');
    }

    // Device endpoints
    async getDevices() {
        return this.request('/api/devices');
    }

    async getDeviceInfo(mac) {
        return this.request(`/api/devices/${mac}/info`);
    }

    async pairDevice(mac) {
        return this.request(`/api/devices/${mac}/pair`, { method: 'POST' });
    }

    async trustDevice(mac) {
        return this.request(`/api/devices/${mac}/trust`, { method: 'POST' });
    }

    async untrustDevice(mac) {
        return this.request(`/api/devices/${mac}/untrust`, { method: 'POST' });
    }

    async connectDevice(mac) {
        return this.request(`/api/devices/${mac}/connect`, { method: 'POST' });
    }

    async disconnectDevice(mac) {
        return this.request(`/api/devices/${mac}/disconnect`, { method: 'POST' });
    }

    async removeDevice(mac) {
        return this.request(`/api/devices/${mac}`, { method: 'DELETE' });
    }

    // WebSocket connection
    connectWebSocket(onMessage) {
        this.onMessageCallback = onMessage;
        this.initWebSocket();
    }

    initWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        
        // Get the base path from the current location (for ingress support)
        let pathname = window.location.pathname;
        pathname = pathname.replace(/\/index\.html$/i, '').replace(/\/+$/, '');
        const basePath = pathname === '' || pathname === '/' ? '' : pathname;
        
        const wsPath = basePath ? `${basePath}/ws/scan` : '/ws/scan';
        const wsURL = `${protocol}//${window.location.host}${wsPath}`;
        
        console.log('WebSocket base path:', basePath);
        console.log('WebSocket URL:', wsURL);

        try {
            this.ws = new WebSocket(wsURL);

            this.ws.onopen = () => {
                console.log('WebSocket connected');
                if (this.wsReconnectInterval) {
                    clearInterval(this.wsReconnectInterval);
                    this.wsReconnectInterval = null;
                }
            };

            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    if (this.onMessageCallback) {
                        this.onMessageCallback(data);
                    }
                } catch (error) {
                    console.error('WebSocket message parse error:', error);
                }
            };

            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            this.ws.onclose = () => {
                console.log('WebSocket disconnected');
                // Attempt to reconnect after 5 seconds
                if (!this.wsReconnectInterval) {
                    this.wsReconnectInterval = setInterval(() => {
                        console.log('Attempting to reconnect WebSocket...');
                        this.initWebSocket();
                    }, 5000);
                }
            };
        } catch (error) {
            console.error('WebSocket initialization error:', error);
        }
    }

    disconnectWebSocket() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
        if (this.wsReconnectInterval) {
            clearInterval(this.wsReconnectInterval);
            this.wsReconnectInterval = null;
        }
    }

    // Send ping to keep connection alive
    sendPing() {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send('ping');
        }
    }
}
