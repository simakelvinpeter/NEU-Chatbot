from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="User's message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    language: Optional[str] = Field("EN", description="Language preference: EN or TR")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "When is the deadline for registration?",
                "session_id": "abc123",
                "language": "EN"
            }
        }

class ChatResponse(BaseModel):
    message: str = Field(..., description="Bot's response message")
    session_id: str = Field(..., description="Session ID for this conversation")
    timestamp: str = Field(..., description="Timestamp of the response")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "The deadline for fall semester registration is September 15th.",
                "session_id": "abc123",
                "timestamp": "2023-12-06T10:30:00"
            }
        }

class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status")
    timestamp: str = Field(..., description="Current server timestamp")
    version: str = Field(..., description="API version")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2023-12-06T10:30:00",
                "version": "1.0.0"
            }
        }

class FileUploadResponse(BaseModel):
    url: str = Field(..., description="URL of the uploaded file")
    id: str = Field(..., description="Unique identifier for the file")
    filename: str = Field(..., description="Original filename")
    size: int = Field(..., description="File size in bytes")

    class Config:
        json_schema_extra = {
            "example": {
                "url": "/uploads/abc123_document.pdf",
                "id": "abc123",
                "filename": "document.pdf",
                "size": 1024000
            }
        }
