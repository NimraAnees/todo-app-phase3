from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, Dict, Any
import uuid
from sqlalchemy import Column, String, CheckConstraint


class MessageBase(SQLModel):
    conversation_id: uuid.UUID
    user_id: uuid.UUID
    role: str  # user or assistant
    content: str


class Message(MessageBase, table=True):
    """
    Message model representing an individual exchange in the conversation.
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    role: str  # user or assistant
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, timestamp={self.timestamp})>"