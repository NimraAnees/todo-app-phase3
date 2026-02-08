"""
Unit tests for the database models in the AI Chat Agent system.
"""
import pytest
from sqlmodel import Session, SQLModel, create_engine
from datetime import datetime
import uuid
from src.models.user import User
from src.models.task import Task
from src.models.conversation import Conversation
from src.models.message import Message
from src.models.tool_call import ToolCall


@pytest.fixture(name="session")
def session_fixture():
    """Create an in-memory database session for testing."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session


def test_user_model(session):
    """Test creating and retrieving a User model."""
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        email="test@example.com",
        hashed_password="hashed_password_here",
        is_active=True
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.email == "test@example.com"
    assert user.id == user_id
    assert user.is_active is True
    assert isinstance(user.created_at, datetime)


def test_task_model(session):
    """Test creating and retrieving a Task model."""
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        email="test@example.com",
        hashed_password="hashed_password_here"
    )
    session.add(user)
    session.commit()

    task = Task(
        user_id=user_id,
        title="Test Task",
        description="Test Description",
        status="pending"
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "pending"
    assert task.user_id == user_id
    assert isinstance(task.created_at, datetime)


def test_conversation_model(session):
    """Test creating and retrieving a Conversation model."""
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        email="test@example.com",
        hashed_password="hashed_password_here"
    )
    session.add(user)
    session.commit()

    conversation = Conversation(
        user_id=user_id,
        title="Test Conversation",
        status="active"
    )

    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    assert conversation.title == "Test Conversation"
    assert conversation.status == "active"
    assert conversation.user_id == user_id
    assert isinstance(conversation.started_at, datetime)


def test_message_model(session):
    """Test creating and retrieving a Message model."""
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        email="test@example.com",
        hashed_password="hashed_password_here"
    )
    session.add(user)
    session.commit()

    conversation = Conversation(
        user_id=user_id,
        title="Test Conversation",
        status="active"
    )
    session.add(conversation)
    session.commit()

    message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content="Test message content"
    )

    session.add(message)
    session.commit()
    session.refresh(message)

    assert message.role == "user"
    assert message.content == "Test message content"
    assert message.conversation_id == conversation.id
    assert message.user_id == user_id
    assert isinstance(message.timestamp, datetime)


def test_tool_call_model(session):
    """Test creating and retrieving a ToolCall model."""
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        email="test@example.com",
        hashed_password="hashed_password_here"
    )
    session.add(user)
    session.commit()

    conversation = Conversation(
        user_id=user_id,
        title="Test Conversation",
        status="active"
    )
    session.add(conversation)
    session.commit()

    message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content="Test message content"
    )
    session.add(message)
    session.commit()

    tool_call = ToolCall(
        conversation_id=conversation.id,
        message_id=message.id,
        user_id=user_id,
        tool_name="test_tool",
        parameters={"param1": "value1"},
        result={"result1": "value1"}
    )

    session.add(tool_call)
    session.commit()
    session.refresh(tool_call)

    assert tool_call.tool_name == "test_tool"
    assert tool_call.parameters == {"param1": "value1"}
    assert tool_call.result == {"result1": "value1"}
    assert tool_call.conversation_id == conversation.id
    assert tool_call.message_id == message.id
    assert tool_call.user_id == user_id
    assert isinstance(tool_call.timestamp, datetime)