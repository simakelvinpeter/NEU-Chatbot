import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from models.message import ChatRequest, ChatResponse
from services.bot_logic import bot

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        session_id = request.session_id or str(uuid.uuid4())
        bot_message = bot.generate_response(request.message, session_id)
        
        response = ChatResponse(
            message=bot_message,
            session_id=session_id,
            timestamp=datetime.utcnow().isoformat(),
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}",
        )


@router.get(
    "/history/{session_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Get chat history",
    description="Retrieve conversation history for a specific session",
)
async def get_history(session_id: str) -> dict:
    """
    Get conversation history for a session
    
    Args:
        session_id: Session identifier
        
    Returns:
        Dictionary with session_id and list of messages
    """
    try:
        history = bot.get_session_history(session_id)
        return {
            "session_id": session_id,
            "messages": history,
            "count": len(history),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve history: {str(e)}",
        )


@router.delete(
    "/session/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Clear chat session",
    description="Delete conversation history for a specific session",
)
async def clear_session(session_id: str):
    """
    Clear a chat session
    
    Args:
        session_id: Session identifier
        
    Raises:
        HTTPException: If session not found
    """
    success = bot.clear_session(session_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    
    return None
