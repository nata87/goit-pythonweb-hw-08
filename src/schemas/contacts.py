from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date

class ContactCreate(ContactBase):
    pass

class ContactResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class ContactUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    email: EmailStr = None
    phone_number: str = None
    birthday: date = None