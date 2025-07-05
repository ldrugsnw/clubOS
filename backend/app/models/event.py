from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
from .profile import Profile

class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    slack_message_ts: Optional[str] = None

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: uuid.UUID
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EventWithParticipants(Event):
    participants: List[Profile] 