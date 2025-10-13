from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None

class Task(TaskCreate):
    id: str
    is_completed: bool = False
    created_at: datetime
