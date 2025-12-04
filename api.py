from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from models.chatbot_service import get_response

# NEW IMPORTS FOR DB + ESTIMATOR
from utils.db import save_message
from utils.estimator import estimate_project

router = APIRouter()


class Message(BaseModel):
    message: str


# ------------- REST API ENDPOINT -------------
@router.post("/chat")
async def chat(msg: Message):
    try:
        user_message = msg.message
        save_message("user", user_message)

        estimate = estimate_project(user_message)
        if estimate:
            bot_reply = (
                f"<b>Project:</b> {estimate['project']}<br>"
                f"<b>Estimated Time:</b> {estimate['time']}<br>"
                f"<b>Features:</b><br>• " + "<br>• ".join(estimate["features"])
            )
        else:
            bot_reply = get_response(user_message)

        save_message("bot", bot_reply)
        return {"response": bot_reply}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# ------------- WEBSOCKET ENDPOINT -------------
@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            save_message("user", data)

            estimate = estimate_project(data)
            if estimate:
                reply = (
                    f"<b>Project:</b> {estimate['project']}<br>"
                    f"<b>Estimated Time:</b> {estimate['time']}<br>"
                    f"<b>Features:</b><br>• " + "<br>• ".join(estimate["features"])
                )
            else:
                reply = get_response(data)

            save_message("bot", reply)
            await websocket.send_text(reply)

    except WebSocketDisconnect:
        print("Client disconnected")
