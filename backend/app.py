import os
import uuid
from datetime import datetime
from pathlib import Path

import aiofiles
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.config import settings
from models.message import HealthResponse, FileUploadResponse
from routes import chat

load_dotenv()

from google import genai

# Create Gemini client once
client = genai.Client(api_key=settings.gemini_api_key)
MODEL_NAME = "gemini-2.0-flash"

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Backend API for Near East University Virtual Assistant",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

upload_dir = Path(settings.UPLOAD_DIR)
upload_dir.mkdir(exist_ok=True)

app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")
app.include_router(chat.router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    return {
        "message": "Welcome to NEU Virtual Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get(f"{settings.API_PREFIX}/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
    )


@app.post(
    f"{settings.API_PREFIX}/upload",
    response_model=FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(file: UploadFile = File(...)) -> FileUploadResponse:
    try:
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE} bytes",
            )

        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix
        unique_filename = f"{file_id}{file_extension}"
        file_path = upload_dir / unique_filename

        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)

        return FileUploadResponse(
            url=f"/uploads/{unique_filename}",
            id=file_id,
            filename=file.filename,
            size=file_size,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}",
        )


@app.on_event("startup")
async def startup_event():
    print(f"🚀 {settings.PROJECT_NAME} is starting...")
    print(f"📚 Documentation available at: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔧 Debug mode: {settings.DEBUG}")
    print("Gemini key loaded:", bool(settings.gemini_api_key))

    # OPTIONAL: quick sanity test (comment out if you don’t want a startup call)
    # resp = client.models.generate_content(model=MODEL_NAME, contents="Say hello in one sentence.")
    # print("Gemini test:", resp.text)


@app.on_event("shutdown")
async def shutdown_event():
    print(f"👋 {settings.PROJECT_NAME} is shutting down...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )