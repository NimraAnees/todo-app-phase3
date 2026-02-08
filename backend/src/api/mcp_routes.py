from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid

from ..database import get_session
from ..auth.auth import get_current_user
from ..tools.add_task_tool import AddTaskTool, AddTaskParameters
from ..tools.list_tasks_tool import ListTasksTool, ListTasksParameters
from ..tools.update_task_tool import UpdateTaskTool, UpdateTaskParameters
from ..tools.complete_task_tool import CompleteTaskTool, CompleteTaskParameters
from ..tools.delete_task_tool import DeleteTaskTool, DeleteTaskParameters


router = APIRouter(
    prefix="/mcp",
    tags=["mcp-tools"]
)


# Request/Response schemas for MCP endpoints
class AddTaskRequest(BaseModel):
    """Request schema for adding a task."""
    title: str = Field(..., description="Title of the task to create")
    description: str = Field("", description="Optional description of the task")


class ListTasksRequest(BaseModel):
    """Request schema for listing tasks."""
    status: Optional[str] = Field(None, description="Filter tasks by status (pending, in_progress, completed)")


class UpdateTaskRequest(BaseModel):
    """Request schema for updating a task."""
    task_id: str = Field(..., description="ID of the task to update")
    title: Optional[str] = Field(None, description="New title for the task")
    description: Optional[str] = Field(None, description="New description for the task")
    status: Optional[str] = Field(None, description="New status for the task")


class CompleteTaskRequest(BaseModel):
    """Request schema for completing a task."""
    task_id: str = Field(..., description="ID of the task to complete")


class DeleteTaskRequest(BaseModel):
    """Request schema for deleting a task."""
    task_id: str = Field(..., description="ID of the task to delete")


class MCPResponse(BaseModel):
    """Standard response schema for MCP tool endpoints."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


def convert_tool_result_to_response(tool_result) -> MCPResponse:
    """
    Convert a ToolResult object to MCPResponse.

    Args:
        tool_result: ToolResult object from tool execution

    Returns:
        MCPResponse with standardized format
    """
    return MCPResponse(
        success=tool_result.success,
        message=tool_result.message,
        data=tool_result.data,
        error=tool_result.error
    )


@router.post("/add_task", response_model=MCPResponse, status_code=status.HTTP_201_CREATED)
def add_task_endpoint(
    request: AddTaskRequest,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> MCPResponse:
    """
    Create a new task for the authenticated user.

    Requires JWT authentication. Task will be associated with the user from the token.

    Args:
        request: Task creation data (title, description)
        current_user: Current authenticated user data (injected from JWT token)
        session: Database session (injected)

    Returns:
        MCPResponse with task creation result

    Raises:
        HTTPException 401: If token is invalid or missing
        HTTPException 400: If validation fails (empty title, etc.)
        HTTPException 500: If task creation fails due to server error
    """
    try:
        # Extract user_id from token
        user_id_str = current_user.get("user_id")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )

        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: malformed user_id"
            )

        # Create tool instance
        tool = AddTaskTool(user_id=user_id, db_session=session)

        # Execute tool
        parameters = AddTaskParameters(
            title=request.title,
            description=request.description
        )
        result = tool.execute(parameters)

        # Convert result to response
        response = convert_tool_result_to_response(result)

        # Raise HTTP exception if tool execution failed
        if not result.success:
            if "required" in result.message.lower() or "empty" in result.message.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result.message
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.message
            )

        return response

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add task: {str(e)}"
        )


@router.post("/list_tasks", response_model=MCPResponse)
def list_tasks_endpoint(
    request: ListTasksRequest,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> MCPResponse:
    """
    List all tasks for the authenticated user, optionally filtered by status.

    Requires JWT authentication. Only returns tasks belonging to the authenticated user.

    Args:
        request: Filter parameters (optional status filter)
        current_user: Current authenticated user data (injected from JWT token)
        session: Database session (injected)

    Returns:
        MCPResponse with list of tasks

    Raises:
        HTTPException 401: If token is invalid or missing
        HTTPException 500: If task retrieval fails due to server error
    """
    try:
        # Extract user_id from token
        user_id_str = current_user.get("user_id")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )

        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: malformed user_id"
            )

        # Create tool instance
        tool = ListTasksTool(user_id=user_id, db_session=session)

        # Execute tool
        parameters = ListTasksParameters(status=request.status)
        result = tool.execute(parameters)

        # Convert result to response
        response = convert_tool_result_to_response(result)

        # Raise HTTP exception if tool execution failed
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.message
            )

        return response

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list tasks: {str(e)}"
        )


@router.post("/update_task", response_model=MCPResponse)
def update_task_endpoint(
    request: UpdateTaskRequest,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> MCPResponse:
    """
    Update an existing task for the authenticated user.

    Requires JWT authentication. Can only update tasks belonging to the authenticated user.

    Args:
        request: Update data (task_id, optional title/description/status)
        current_user: Current authenticated user data (injected from JWT token)
        session: Database session (injected)

    Returns:
        MCPResponse with task update result

    Raises:
        HTTPException 401: If token is invalid or missing
        HTTPException 403: If task belongs to a different user
        HTTPException 404: If task not found
        HTTPException 500: If task update fails due to server error
    """
    try:
        # Extract user_id from token
        user_id_str = current_user.get("user_id")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )

        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: malformed user_id"
            )

        # Create tool instance
        tool = UpdateTaskTool(user_id=user_id, db_session=session)

        # Execute tool
        parameters = UpdateTaskParameters(
            task_id=request.task_id,
            title=request.title,
            description=request.description,
            status=request.status
        )
        result = tool.execute(parameters)

        # Convert result to response
        response = convert_tool_result_to_response(result)

        # Raise HTTP exception if tool execution failed
        if not result.success:
            if "not found" in result.message.lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=result.message
                )
            if "not authorized" in result.message.lower() or "different user" in result.message.lower():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=result.message
                )
            if "required" in result.message.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result.message
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.message
            )

        return response

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task: {str(e)}"
        )


@router.post("/complete_task", response_model=MCPResponse)
def complete_task_endpoint(
    request: CompleteTaskRequest,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> MCPResponse:
    """
    Mark a task as completed for the authenticated user.

    Requires JWT authentication. Can only complete tasks belonging to the authenticated user.

    Args:
        request: Task completion data (task_id)
        current_user: Current authenticated user data (injected from JWT token)
        session: Database session (injected)

    Returns:
        MCPResponse with task completion result

    Raises:
        HTTPException 401: If token is invalid or missing
        HTTPException 403: If task belongs to a different user
        HTTPException 404: If task not found
        HTTPException 500: If task completion fails due to server error
    """
    try:
        # Extract user_id from token
        user_id_str = current_user.get("user_id")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )

        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: malformed user_id"
            )

        # Create tool instance
        tool = CompleteTaskTool(user_id=user_id, db_session=session)

        # Execute tool
        parameters = CompleteTaskParameters(task_id=request.task_id)
        result = tool.execute(parameters)

        # Convert result to response
        response = convert_tool_result_to_response(result)

        # Raise HTTP exception if tool execution failed
        if not result.success:
            if "not found" in result.message.lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=result.message
                )
            if "not authorized" in result.message.lower() or "different user" in result.message.lower():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=result.message
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.message
            )

        return response

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete task: {str(e)}"
        )


@router.post("/delete_task", response_model=MCPResponse, status_code=status.HTTP_200_OK)
def delete_task_endpoint(
    request: DeleteTaskRequest,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> MCPResponse:
    """
    Delete a task for the authenticated user.

    Requires JWT authentication. Can only delete tasks belonging to the authenticated user.

    Args:
        request: Task deletion data (task_id)
        current_user: Current authenticated user data (injected from JWT token)
        session: Database session (injected)

    Returns:
        MCPResponse with task deletion result

    Raises:
        HTTPException 401: If token is invalid or missing
        HTTPException 403: If task belongs to a different user
        HTTPException 404: If task not found
        HTTPException 500: If task deletion fails due to server error
    """
    try:
        # Extract user_id from token
        user_id_str = current_user.get("user_id")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )

        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: malformed user_id"
            )

        # Create tool instance
        tool = DeleteTaskTool(user_id=user_id, db_session=session)

        # Execute tool
        parameters = DeleteTaskParameters(task_id=request.task_id)
        result = tool.execute(parameters)

        # Convert result to response
        response = convert_tool_result_to_response(result)

        # Raise HTTP exception if tool execution failed
        if not result.success:
            if "not found" in result.message.lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=result.message
                )
            if "not authorized" in result.message.lower() or "different user" in result.message.lower():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=result.message
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.message
            )

        return response

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task: {str(e)}"
        )
