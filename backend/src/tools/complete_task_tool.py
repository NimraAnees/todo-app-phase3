from .base import BaseMCPTool, ToolParameters, ToolResult
from typing import Dict, Any
from pydantic import Field
from sqlmodel import Session
import uuid
from ..services.task_service import TaskService


class CompleteTaskParameters(ToolParameters):
    """
    Parameters for the complete_task tool.
    """
    task_id: str = Field(..., description="ID of the task to mark as completed")


class CompleteTaskTool(BaseMCPTool):
    """
    MCP Tool for completing tasks.
    """

    def get_name(self) -> str:
        """
        Get the name of the tool.

        Returns:
            Tool name as a string
        """
        return "complete_task_tool"

    def get_description(self) -> str:
        """
        Get the description of the tool.

        Returns:
            Tool description as a string
        """
        return "Marks an existing task as completed."

    def get_parameters_schema(self) -> Dict[str, Any]:
        """
        Get the parameters schema for the tool.

        Returns:
            Schema definition for tool parameters
        """
        return CompleteTaskParameters.model_json_schema()

    def execute(self, parameters: CompleteTaskParameters) -> ToolResult:
        """
        Execute the tool to complete a task.

        Args:
            parameters: Parameters containing the task ID

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

            # Complete the task using the service
            completed_task = TaskService.complete_task(
                session=self.db_session,
                task_id=task_uuid,
                user_id=self.user_id
            )

            if completed_task is None:
                return ToolResult(
                    success=False,
                    message="Task not found or user doesn't have permission to complete it",
                    error="Task not found"
                )

            # Return success result
            return ToolResult(
                success=True,
                message=f"Successfully completed task '{completed_task.title}'",
                data={
                    "task_id": str(completed_task.id),
                    "title": completed_task.title,
                    "status": completed_task.status,
                    "completed_at": completed_task.completed_at.isoformat()
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                message="Failed to complete task",
                error=str(e),
                data=None
            )