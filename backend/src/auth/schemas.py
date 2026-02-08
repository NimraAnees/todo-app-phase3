from pydantic import BaseModel
from typing import Optional
import uuid


class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for token data.
    """
    username: Optional[str] = None


class UserBase(BaseModel):
    """
    Base schema for user data.
    """
    email: str


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str


class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    email: str
    password: str


class UserResponse(UserBase):
    """
    Schema for user response data.
    """
    id: uuid.UUID
    is_active: bool

    class Config:
        from_attributes = True


class UserPublic(UserBase):
    """
    Schema for public user data (without sensitive information).
    """
    id: uuid.UUID

    class Config:
        from_attributes = True