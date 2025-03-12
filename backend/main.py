from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Get the absolute path to the frontend directory
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

# Mount the frontend directory
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(frontend_path, "landing_page.html"))
