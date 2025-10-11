from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer
from brotli_asgi import BrotliMiddleware  # https://github.com/fullonic/brotli-asgi


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


# for Authorization: Bearer token header
# security = HTTPBearer()

# can add modules having api calls below
# example : 
# import module_name
from api import router as chatbot_router
app.include_router(chatbot_router, prefix="/api", tags=["Chatbot"])


# initiate
# api_roles.get_admin_apis()
# imp: This function needs to be called at the very last AFTER all the py modules are loaded.
# Because it HALTS the openapi generation process and it doesn't include subsequent loaded api calls into the apidoc, even though they're active.
