import asyncio
import random
import string

from app.utils.state import semaphore, state
from app.utils.tools import make_logger
from fastapi import APIRouter, Path, WebSocket

from ..utils.responses import (camera_not_connected, camera_not_enrolled,
                               capture_success_wait_response)

logger_ = make_logger('results')
logger_conn = make_logger('connections')

router = APIRouter(prefix='/capture', tags=["Capturas"])

@router.post("/{camera_id}")
async def capture_qrcode_route(camera_id: int = Path(ge=1)):

    if not camera_id in state.websockets.keys():
        return await camera_not_connected(camera_id)

    if not state.websockets[camera_id]["connected"]:
        return await camera_not_connected(camera_id)

    request_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=24))
    state.websockets[camera_id]["request_id"] = request_id

    state.websockets[camera_id]["capture"] = False
    
    websocket: WebSocket = state.websockets[camera_id]["ws"]
    
    # Protected region
    async with semaphore:
        try:
            await websocket.send_text(state.websockets[camera_id]["request_id"])
            lectures = await websocket.receive_json()
        except:
            return await camera_not_connected(camera_id)
    # End protected region

    logger_.info(f"[{request_id}] Lectures[drone_id = {camera_id}]: {lectures}")

    return await capture_success_wait_response(request_id, lectures)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    id: str = await websocket.receive_text()
    camera_id: int = int(id)
    state.websockets[camera_id] = {
        "ws": websocket,
        "capture": False, 
        "request_id": None, 
        "connected": True
    }

    await websocket.send_text("test")
    lectures = await websocket.receive_json()
    logger_.info(f"[TEST] Lectures[drone_id = {camera_id}]: {lectures}")
    logger_conn.info("Connected to: {}".format(websocket.client.host))
    # mantem o loop vivo enquanto a conexão durar
    while True:

        try:
            async with semaphore:
                await websocket.send_text("connection_test")

        except:
            del state.websockets[camera_id]
            break

        await asyncio.sleep(5)

    logger_conn.info("Disconnected from: {}".format(websocket.client.host))
    return