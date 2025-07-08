from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class ProfileBase(BaseModel):
    name: str
    department: Optional[str] = None
    student_id: Optional[str] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    slack_user_id: Optional[str] = None

class ProfileCreate(ProfileBase):
    id: uuid.UUID
    email: EmailStr

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    student_id: Optional[str] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    slack_user_id: Optional[str] = None

class Profile(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    department: Optional[str] = None
    student_id: Optional[str] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    slack_user_id: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 