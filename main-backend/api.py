from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from models.chatbot_service import get_response   

router = APIRouter()

# Request model
class Message(BaseModel):
    message: str


#  REST API Endpoint
@router.post("/chat")
async def chat(msg: Message):
    response = get_response(msg.message)
    return {"response": response}


#  WebSocket Endpoint
@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = get_response(data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")
