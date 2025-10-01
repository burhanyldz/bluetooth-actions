"""
Bluetooth Manager FastAPI Application
Provides REST API and WebSocket endpoints for Bluetooth management
"""

import argparse
import asyncio
import logging
from typing import Dict, List, Set
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

from bluetooth_manager import BluetoothManager


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Pydantic models for request/response
class PowerRequest(BaseModel):
    power_on: bool


class DeviceAction(BaseModel):
    mac: str


# Initialize FastAPI app
app = FastAPI(title="Bluetooth Manager", version="1.0.0")

# Initialize Bluetooth Manager
bt_manager = BluetoothManager()

# Store active WebSocket connections
active_connections: Set[WebSocket] = set()


# API Endpoints

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/api/adapters")
async def list_adapters():
    """Get list of Bluetooth adapters"""
    try:
        adapters = bt_manager.list_adapters()
        return {"adapters": adapters}
    except Exception as e:
        logger.error(f"Error listing adapters: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/adapters/{adapter_id}/info")
async def get_adapter_info(adapter_id: str):
    """Get detailed information about an adapter"""
    try:
        info = bt_manager.get_adapter_info(adapter_id)
        return info
    except Exception as e:
        logger.error(f"Error getting adapter info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/adapters/default/info")
async def get_default_adapter_info():
    """Get information about the default adapter"""
    try:
        info = bt_manager.get_adapter_info()
        return info
    except Exception as e:
        logger.error(f"Error getting adapter info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/adapters/power")
async def set_adapter_power(request: PowerRequest):
    """Power on/off the Bluetooth adapter"""
    try:
        success, message = bt_manager.set_adapter_power(request.power_on)
        if success:
            return {"success": True, "message": message}
        else:
            raise HTTPException(status_code=400, detail=message)
    except Exception as e:
        logger.error(f"Error setting adapter power: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/scan/start")
async def start_scan():
    """Start Bluetooth scanning"""
    if bt_manager.scanning:
        return {"success": True, "message": "Scan already running"}
    
    # Start scan in background
    asyncio.create_task(scan_task())
    return {"success": True, "message": "Scan started"}


@app.post("/api/scan/stop")
async def stop_scan():
    """Stop Bluetooth scanning"""
    try:
        success, message = bt_manager.stop_scan()
        return {"success": success, "message": message}
    except Exception as e:
        logger.error(f"Error stopping scan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/scan/status")
async def get_scan_status():
    """Get current scanning status"""
    return {"scanning": bt_manager.scanning}


@app.get("/api/devices")
async def list_devices():
    """Get list of all known devices"""
    try:
        devices = bt_manager.get_devices()
        
        # Enrich with current status
        for device in devices:
            info = bt_manager.get_device_info(device['mac'])
            device['connected'] = info.get('connected', False)
            device['paired'] = info.get('paired', False)
            device['rssi'] = info.get('rssi')
        
        return {"devices": devices}
    except Exception as e:
        logger.error(f"Error listing devices: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/devices/{mac}/info")
async def get_device_info(mac: str):
    """Get detailed information about a device"""
    try:
        # Normalize MAC address format
        mac = mac.upper().replace('-', ':')
        info = bt_manager.get_device_info(mac)
        
        if 'error' in info:
            raise HTTPException(status_code=404, detail=info['error'])
        
        return info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting device info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/devices/{mac}/pair")
async def pair_device(mac: str):
    """Pair with a device"""
    try:
        mac = mac.upper().replace('-', ':')
        success, message = bt_manager.pair_device(mac)
        
        if success:
            # Notify all WebSocket clients
            await broadcast_message({
                "type": "device_paired",
                "mac": mac,
                "message": message
            })
            return {"success": True, "message": message}
        else:
            raise HTTPException(status_code=400, detail=message)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error pairing device: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/devices/{mac}/trust")
async def trust_device(mac: str):
    """Trust a device"""
    try:
        mac = mac.upper().replace('-', ':')
        success, message = bt_manager.trust_device(mac)
        
        if success:
            return {"success": True, "message": message}
        else:
            raise HTTPException(status_code=400, detail=message)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error trusting device: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/devices/{mac}/untrust")
async def untrust_device(mac: str):
    """Untrust a device"""
    try:
        mac = mac.upper().replace('-', ':')
        success, message = bt_manager.untrust_device(mac)
        
        if success:
            return {"success": True, "message": message}
        else:
            raise HTTPException(status_code=400, detail=message)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error untrusting device: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/devices/{mac}/connect")
async def connect_device(mac: str):
    """Connect to a device"""
    try:
        mac = mac.upper().replace('-', ':')
        success, message = bt_manager.connect_device(mac)
        
        if success:
            # Get device name
            info = bt_manager.get_device_info(mac)
            device_name = info.get('name', mac)
            
            # Notify all WebSocket clients
            await broadcast_message({
                "type": "device_connected",
                "mac": mac,
                "name": device_name,
                "message": message
            })
            return {"success": True, "message": message}
        else:
            raise HTTPException(status_code=400, detail=message)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error connecting device: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/devices/{mac}/disconnect")
async def disconnect_device(mac: str):
    """Disconnect from a device"""
    try:
        mac = mac.upper().replace('-', ':')
        success, message = bt_manager.disconnect_device(mac)
        
        if success:
            # Notify all WebSocket clients
            await broadcast_message({
                "type": "device_disconnected",
                "mac": mac,
                "message": message
            })
            return {"success": True, "message": message}
        else:
            raise HTTPException(status_code=400, detail=message)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error disconnecting device: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/devices/{mac}")
async def remove_device(mac: str):
    """Remove a device"""
    try:
        mac = mac.upper().replace('-', ':')
        success, message = bt_manager.remove_device(mac)
        
        if success:
            # Notify all WebSocket clients
            await broadcast_message({
                "type": "device_removed",
                "mac": mac,
                "message": message
            })
            return {"success": True, "message": message}
        else:
            raise HTTPException(status_code=400, detail=message)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing device: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket endpoint
@app.websocket("/ws/scan")
async def websocket_scan(websocket: WebSocket):
    """WebSocket endpoint for real-time scan updates"""
    await websocket.accept()
    active_connections.add(websocket)
    
    logger.info("WebSocket client connected")
    
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            
            # Handle client messages if needed
            if data == "ping":
                await websocket.send_json({"type": "pong"})
    
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
        active_connections.discard(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        active_connections.discard(websocket)


# Background tasks
async def scan_task():
    """Background task for scanning"""
    async def scan_callback(data: Dict):
        """Callback for scan updates"""
        await broadcast_message(data)
    
    await bt_manager.start_scan_async(scan_callback)


async def broadcast_message(message: Dict):
    """Broadcast message to all connected WebSocket clients"""
    disconnected = set()
    
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception as e:
            logger.error(f"Error broadcasting to client: {e}")
            disconnected.add(connection)
    
    # Remove disconnected clients
    for connection in disconnected:
        active_connections.discard(connection)


# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="/app/web"), name="static")


@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML"""
    return FileResponse("/app/web/index.html")


# Main entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bluetooth Manager API Server")
    parser.add_argument("--port", type=int, default=8099, help="Port to run the server on")
    parser.add_argument("--log-level", type=str, default="info", 
                       choices=["debug", "info", "warning", "error"],
                       help="Logging level")
    
    args = parser.parse_args()
    
    # Set log level
    log_level = getattr(logging, args.log_level.upper())
    logging.getLogger().setLevel(log_level)
    
    logger.info(f"Starting Bluetooth Manager on port {args.port}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=args.port,
        log_level=args.log_level
    )
