from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class UserBase(BaseModel):
    class Config:
        from_attributes = True
        alias_generator = lambda x: "".join(
            word.capitalize() if i else word for i, word in enumerate(x.split("_"))
        )
        populate_by_name = True


class UserResponse(UserBase):
    id: Optional[int] = None
    name: str
    surname: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def remove_timezone(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value is not None and value.tzinfo is not None:
            return value.replace(tzinfo=None)
        return value


class UserCreate(UserBase):
    name: str
    surname: str
    password: str


class UserUpdate(UserBase):
    name: Optional[str] = None
    surname: Optional[str] = None
    password: Optional[str] = None