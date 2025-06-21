from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.cerebras_service import CerebrasService
from app.models.agent import Agent
import json
import asyncio
from typing import List

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{agent_id}")
async def websocket_chat(websocket: WebSocket, agent_id: int):
    await manager.connect(websocket)
    cerebras = CerebrasService()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Prepare conversation history
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": message_data["content"]}
            ]
            
            # Stream response from Cerebras
            response_chunks = []
            async for chunk in cerebras.stream_response(messages):
                response_chunks.append(chunk)
                # Send each chunk to client in real-time
                await manager.send_personal_message(
                    json.dumps({
                        "type": "chunk",
                        "content": chunk
                    }),
                    websocket
                )
            
            # Send completion signal
            await manager.send_personal_message(
                json.dumps({
                    "type": "complete",
                    "full_response": "".join(response_chunks)
                }),
                websocket
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket) 