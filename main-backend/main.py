from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from brotli_asgi import BrotliMiddleware

from api import router
from utils.db import save_message
from utils.estimator import estimate_project

app = FastAPI()

# Include API Routes
app.include_router(router)

# Serve Frontend at ROOT
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Brotli compression
app.add_middleware(BrotliMiddleware)


# --------------------------------
#         WEBSOCKET CHAT
# --------------------------------
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            user_msg = await websocket.receive_text()
            save_message("user", user_msg)

            # Check estimator
            estimate = estimate_project(user_msg)
            if estimate:
                bot_reply = (
                    f"<b>Project:</b> {estimate['project']}<br>"
                    f"<b>Estimated Time:</b> {estimate['time']}<br>"
                    f"<b>Features:</b><br>• "
                    + "<br>• ".join(estimate["features"])
                )
            else:
                bot_reply = f"You said: {user_msg}"

            save_message("bot", bot_reply)
            await websocket.send_text(bot_reply)

    except WebSocketDisconnect:
        print("Client Disconnected")
