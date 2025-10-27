from fastapi import WebSocket, WebSocketDisconnect, HTTPException
from main import app
from pydantic import BaseModel
from models.chatbot_service import get_response   

# Request model
class Message(BaseModel):
    message: str


#  REST API Endpoint
@app.post("/chat")
async def chat(msg: Message):
    try:
        response = get_response(msg.message)
        return {"response": response}
    except ValueError as e:
        print(f"Invalid input: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error processing chat request {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


#  WebSocket Endpoint
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = get_response(data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")
