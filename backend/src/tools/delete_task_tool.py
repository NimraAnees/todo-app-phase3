from .base import BaseMCPTool, ToolParameters, ToolResult
from typing import Dict, Any
from pydantic import Field
from sqlmodel import Session
import uuid
from ..services.task_service import TaskService


class DeleteTaskParameters(ToolParameters):
    """
    Parameters for the delete_task tool.
    """
    task_id: str = Field(..., description="ID of the task to delete")


class DeleteTaskTool(BaseMCPTool):
    """
    MCP Tool for deleting tasks.
    """

    def get_name(self) -> str:
        """
        Get the name of the tool.

        Returns:
            Tool name as a string
        """
        return "delete_task_tool"

    def get_description(self) -> str:
        """
        Get the description of the tool.

        Returns:
            Tool description as a string
        """
        return "Deletes an existing task for the user."

    def get_parameters_schema(self) -> Dict[str, Any]:
        """
        Get the parameters schema for the tool.

        Returns:
            Schema definition for tool parameters
        """
        return DeleteTaskParameters.model_json_schema()

    def execute(self, parameters: DeleteTaskParameters) -> ToolResult:
        """
        Execute the tool to delete a task.

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

            # Delete the task using the service
            delete_success = TaskService.delete_task(
                session=self.db_session,
                task_id=task_uuid,
                user_id=self.user_id
            )

            if not delete_success:
                return ToolResult(
                    success=False,
                    message="Task not found or user doesn't have permission to delete it",
                    error="Task not found"
                )

            # Return success result
            return ToolResult(
                success=True,
                message="Successfully deleted task",
                data={
                    "task_id": parameters.task_id
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                message="Failed to delete task",
                error=str(e),
                data=None
            )