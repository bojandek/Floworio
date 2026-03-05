"""
Floworio API — FastAPI Backend
Data processing, AI story generation, Kokoro TTS, Remotion rendering, Social media publishing
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os

from routers import upload, story, tts, render, publish

app = FastAPI(
    title="Floworio API",
    description="Data Story SaaS Platform — Excel → AI Story → Remotion Video → Social Media",
    version="0.1.0",
)

# CORS — allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        os.getenv("FRONTEND_URL", "http://localhost:3000"),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for serving rendered videos and audio
os.makedirs("renders", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("audio", exist_ok=True)

app.mount("/renders", StaticFiles(directory="renders"), name="renders")
app.mount("/audio", StaticFiles(directory="audio"), name="audio")

# Include routers
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(story.router, prefix="/api/story", tags=["Story"])
app.include_router(tts.router, prefix="/api/tts", tags=["TTS"])
app.include_router(render.router, prefix="/api/render", tags=["Render"])
app.include_router(publish.router, prefix="/api/publish", tags=["Publish"])


@app.get("/")
async def root():
    return {
        "name": "Floworio API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
