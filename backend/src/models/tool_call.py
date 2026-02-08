from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional, Dict, Any
import uuid


class ToolCallBase(SQLModel):
    conversation_id: uuid.UUID
    message_id: uuid.UUID
    user_id: uuid.UUID
    tool_name: str


class ToolCall(ToolCallBase, table=True):
    """
    ToolCall model recording tool invocations made by the AI agent during conversations.
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", nullable=False)
    message_id: uuid.UUID = Field(foreign_key="message.id", nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    tool_name: str
    parameters: Optional[Dict[str, Any]] = Field(default={}, sa_column=Column(JSON))
    result: Optional[Dict[str, Any]] = Field(default={}, sa_column=Column(JSON))
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="tool_calls")

    def __repr__(self):
        return f"<ToolCall(id={self.id}, tool_name={self.tool_name}, timestamp={self.timestamp})>"