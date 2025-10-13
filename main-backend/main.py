from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer
from brotli_asgi import BrotliMiddleware  # https://github.com/fullonic/brotli-asgi

import logging
from fastapi import WebSocket, WebSocketDisconnect
import uvicorn
from models.Websocket_handler import handle_chat_message
from fastapi.responses import FileResponse
import os

logger= logging.getLogger(__name__)



app = FastAPI()




# allow cors - from https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Filename", "x-filename"]
)

# enable Brotli compression. Better for json payloads, supported by most browsers. Fallback to gzip by default. from https://github.com/fullonic/brotli-asgi
app.add_middleware(BrotliMiddleware)


# Health check
@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Backend Status</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding-top: 50px; background-color: #f4f4f4; }
                h1 { color: #2c3e50; }
                a { text-decoration: none; color: white; background-color: #007BFF; padding: 10px 20px; border-radius: 5px; }
                a:hover { background-color: #0056b3; }
            </style>
        </head>
        <body>
            <h1>🚀 Everything is working!</h1>
            <p>Welcome to the Python World</p>
            <a href="/docs">Go to API Docs</a>
        </body>
    </html>
    """
    return html_content




@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info(f"WebSocket client connected: {websocket.client}")

    try:
        while True:
            try:
                data = await websocket.receive_text()
                response = handle_chat_message(data)

            except Exception as e:
                logger.exception(f"Error processing message: {e}")
                response = "Sorry, an error occurred. Please try again."
            await websocket.send_text(response)

    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected: {websocket.client}")

@app.get("/chat", response_class=HTMLResponse)
async def get_chat():
    html_path = os.path.join(os.path.dirname(__file__), "frontend","index.html")
    if not os.path.exists(html_path):
        return HTMLResponse("<h1>index.html not found</h1>")
    return FileResponse(html_path)




# for Authorization: Bearer token header
# security = HTTPBearer()

# can add modules having api calls below
# example : 
# import module_name




# initiate
# api_roles.get_admin_apis()
# imp: This function needs to be called at the very last AFTER all the py modules are loaded.
# Because it HALTS the openapi generation process and it doesn't include subsequent loaded api calls into the apidoc, even though they're active.
