from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: Optional[date]


class ContactUpdate(ContactBase):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date

    class Config:
        from_attributes = True
