from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from pydantic import BaseModel
import uuid
from ..auth.auth import get_current_user
from ..database import get_session
from sqlmodel import Session
from ..services.task_service import TaskService
from ..services.conversation_service import ConversationService
from ..models.conversation import Conversation
from ..tools.add_task_tool import AddTaskTool, AddTaskParameters
from ..tools.list_tasks_tool import ListTasksTool, ListTasksParameters
from ..tools.update_task_tool import UpdateTaskTool, UpdateTaskParameters
from ..tools.complete_task_tool import CompleteTaskTool, CompleteTaskParameters
from ..tools.delete_task_tool import DeleteTaskTool, DeleteTaskParameters
from ..utils.logging import log_ai_interaction
from datetime import datetime


router = APIRouter(prefix="/api/{user_id}", tags=["chat"])


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    """
    message: str
    conversation_id: str = None


class ToolCallInfo(BaseModel):
    """
    Model for tool call information.
    """
    tool_name: str
    parameters: Dict[str, Any]
    result: Dict[str, Any]


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    """
    response: str
    conversation_id: str
    message_id: str
    tool_calls: List[ToolCallInfo] = []
    context_preserved: bool = True


@router.post("/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Process natural language input from a user and return AI-generated response.

    Args:
        user_id: The ID of the authenticated user
        request: Chat request containing the user's message
        current_user: Current authenticated user (from dependency)
        session: Database session (from dependency)

    Returns:
        ChatResponse containing the AI agent's response
    """
    # Validate user ID matches authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's resources"
        )

    # Validate and parse user_id first (outside try block for specific error handling)
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    try:
        # Get or create conversation
        conversation_id = request.conversation_id
        conversation_uuid = None

        if conversation_id:
            # Verify conversation belongs to user
            try:
                conversation_uuid = uuid.UUID(conversation_id)
                existing_conv = ConversationService.get_conversation_by_id(session, conversation_uuid, user_uuid)
                if not existing_conv:
                    # If conversation doesn't exist or doesn't belong to user, create a new one
                    conversation = ConversationService.create_conversation(session, user_uuid)
                    conversation_id = str(conversation.id)
                    conversation_uuid = conversation.id
                else:
                    conversation_id = str(existing_conv.id)
                    conversation_uuid = existing_conv.id
            except ValueError:
                # Invalid conversation_id format, create new conversation
                conversation = ConversationService.create_conversation(session, user_uuid)
                conversation_id = str(conversation.id)
                conversation_uuid = conversation.id
        else:
            # Create a new conversation
            conversation = ConversationService.create_conversation(session, user_uuid)
            conversation_id = str(conversation.id)
            conversation_uuid = conversation.id

        # Add user's message to the conversation
        user_message = ConversationService.add_message_to_conversation(
            session, conversation_uuid, user_uuid, "user", request.message
        )
        message_id = str(user_message.id)

        # Process the user's message using the AI agent
        from ..agents.todo_agent import TodoAgent

        # Initialize the AI agent with the conversation context and message ID
        agent = TodoAgent(
            user_id=user_uuid,
            db_session=session,
            conversation_id=conversation_uuid,
            message_id=user_message.id
        )

        # Process the message using the agent
        # Wrap in try-except to handle agent errors gracefully
        try:
            agent_response = agent.process_message(request.message)
        except Exception as agent_error:
            # If agent processing fails, return a helpful fallback response
            agent_response = {
                "response": "I'm having trouble processing that request. Could you try rephrasing it? For example, try 'Add a task to buy groceries' or 'Show me my tasks'.",
                "tool_calls": [],
                "intent": "unknown"
            }

        # Extract the response and tool calls from the agent
        ai_response = agent_response["response"]
        tool_calls_info = []

        # Convert agent tool calls to the format expected by the endpoint
        for tool_call in agent_response.get("tool_calls", []):
            # Convert ToolResult to dict if needed
            result_dict = tool_call.result.dict() if hasattr(tool_call.result, 'dict') else tool_call.result
            tool_calls_info.append(ToolCallInfo(
                tool_name=tool_call.tool_name,
                parameters=tool_call.parameters,
                result=result_dict
            ))

        # Add AI's response to the conversation with tool call information
        ai_message = ConversationService.add_message_to_conversation(
            session, conversation_uuid, user_uuid, "assistant", ai_response,
            {"tool_calls": [call.dict() for call in tool_calls_info]} if tool_calls_info else None
        )

        # Log the AI interaction
        try:
            log_ai_interaction(
                user_id=user_id,
                conversation_id=conversation_id,
                user_input=request.message,
                ai_response=ai_response,
                tool_calls=[call.dict() for call in tool_calls_info]
            )
        except Exception:
            # If logging fails, continue anyway
            pass

        # Return the response
        return ChatResponse(
            response=ai_response,
            conversation_id=conversation_id,
            message_id=message_id,
            tool_calls=tool_calls_info,
            context_preserved=True
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error for debugging but return a user-friendly message
        import traceback
        traceback.print_exc()

        # Return 200 OK with an error message instead of 500
        # This ensures the frontend always gets a valid response
        return ChatResponse(
            response="I encountered an error processing your request. Please try again or rephrase your message.",
            conversation_id=conversation_id if conversation_id else str(uuid.uuid4()),
            message_id=str(uuid.uuid4()),
            tool_calls=[],
            context_preserved=False
        )


def extract_task_title(message: str) -> str:
    """
    Simple function to extract task title from user message.
    This is a simplified implementation - in a real system,
    this would be handled by an AI agent with NLP capabilities.

    Args:
        message: The user's message

    Returns:
        Extracted task title or None if not found
    """
    # Remove common task creation phrases
    prefixes = ["add ", "create ", "make ", "new ", "please ", "can you "]

    # Normalize the message
    normalized = message.lower().strip()

    for prefix in prefixes:
        if normalized.startswith(prefix):
            # Extract everything after the prefix
            title = normalized[len(prefix):].strip()
            # Remove common suffixes
            title = title.replace("task", "").replace("to", "").strip()
            return title.capitalize() if title else None

    # If no prefix matched, return the whole message (as a fallback)
    return message.strip() if message.strip() else None