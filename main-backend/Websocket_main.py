from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
from .websocket_handler import handle_chat_message


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Chatbot WebSocket server is running!"}

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()

            response = handle_chat_message(data)

            await websocket.send_text(response)

    except WebSocketDisconnect:
        print("Client disconnected")


if __name__ == "__main__":
    uvicorn.run("Main.main:app", host="127.0.0.1", port=8000, reload=True)

