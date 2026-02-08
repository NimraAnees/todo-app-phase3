from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid


class ConversationBase(SQLModel):
    title: str
    status: str = Field(default="active")


class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a user's ongoing dialogue with the AI agent.
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    title: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    last_message_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="active")  # active, archived

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")
    tool_calls: List["ToolCall"] = Relationship(back_populates="conversation")

    def __repr__(self):
        return f"<Conversation(id={self.id}, title={self.title}, status={self.status})>"