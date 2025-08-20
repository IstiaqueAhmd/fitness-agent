from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = "anonymous"

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: datetime

class ChatSession(BaseModel):
    session_id: str
    user_id: str
    title: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatHistory(BaseModel):
    session_id: str
    messages: List[ChatMessage]

class SessionList(BaseModel):
    sessions: List[ChatSession]

class FitnessPlan(BaseModel):
    id: Optional[int] = None
    user_id: str
    session_id: str
    plan_name: str
    plan_type: str  # "workout", "nutrition", "combined"
    plan_data: Dict[str, Any]
    goals: str
    duration_weeks: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class FitnessPlanCreate(BaseModel):
    plan_name: str
    plan_type: str
    plan_data: Dict[str, Any]
    goals: str
    duration_weeks: int = 12

class FitnessPlanList(BaseModel):
    plans: List[FitnessPlan]