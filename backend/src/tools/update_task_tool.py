from .base import BaseMCPTool, ToolParameters, ToolResult
from typing import Dict, Any, Optional
from pydantic import Field
from sqlmodel import Session
import uuid
from ..services.task_service import TaskService


class UpdateTaskParameters(ToolParameters):
    """
    Parameters for the update_task tool.
    """
    task_id: str = Field(..., description="ID of the task to update")
    title: Optional[str] = Field(None, description="New title for the task")
    description: Optional[str] = Field(None, description="New description for the task")
    status: Optional[str] = Field(None, description="New status for the task (pending, in_progress, completed)")


class UpdateTaskTool(BaseMCPTool):
    """
    MCP Tool for updating tasks.
    """

    def get_name(self) -> str:
        """
        Get the name of the tool.

        Returns:
            Tool name as a string
        """
        return "update_task_tool"

    def get_description(self) -> str:
        """
        Get the description of the tool.

        Returns:
            Tool description as a string
        """
        return "Updates an existing task for the user."

    def get_parameters_schema(self) -> Dict[str, Any]:
        """
        Get the parameters schema for the tool.

        Returns:
            Schema definition for tool parameters
        """
        return UpdateTaskParameters.model_json_schema()

    def execute(self, parameters: UpdateTaskParameters) -> ToolResult:
        """
        Execute the tool to update a task.

        Args:
            parameters: Parameters for updating the task

        Returns:
            Result of tool execution
        """
        try:
            # Get the database session from the instance
            if not self.db_session:
                return ToolResult(
                    success=False,
                    message="Database session is required",
                    error="Missing database session"
                )

            # Validate the task ID
            try:
                task_uuid = uuid.UUID(parameters.task_id)
            except ValueError:
                return ToolResult(
                    success=False,
                    message="Invalid task ID format",
                    error="Task ID must be a valid UUID"
                )

            # Update the task using the service
            updated_task = TaskService.update_task(
                session=self.db_session,
                task_id=task_uuid,
                user_id=self.user_id,
                title=parameters.title,
                description=parameters.description,
                status=parameters.status
            )

            if updated_task is None:
                return ToolResult(
                    success=False,
                    message="Task not found or user doesn't have permission to update it",
                    error="Task not found"
                )

            # Return success result
            return ToolResult(
                success=True,
                message=f"Successfully updated task '{updated_task.title}'",
                data={
                    "task_id": str(updated_task.id),
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "status": updated_task.status,
                    "updated_at": updated_task.updated_at.isoformat()
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                message="Failed to update task",
                error=str(e),
                data=None
            )