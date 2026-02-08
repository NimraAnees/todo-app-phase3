from .base import BaseMCPTool, ToolParameters, ToolResult
from typing import Dict, Any
from pydantic import Field
from sqlmodel import Session
import uuid
from ..services.task_service import TaskService


class AddTaskParameters(ToolParameters):
    """
    Parameters for the add_task tool.
    """
    title: str = Field(..., description="Title of the task to create")
    description: str = Field("", description="Optional description of the task")


class AddTaskTool(BaseMCPTool):
    """
    MCP Tool for adding tasks.
    """

    def get_name(self) -> str:
        """
        Get the name of the tool.

        Returns:
            Tool name as a string
        """
        return "add_task_tool"

    def get_description(self) -> str:
        """
        Get the description of the tool.

        Returns:
            Tool description as a string
        """
        return "Creates a new task for the user."

    def get_parameters_schema(self) -> Dict[str, Any]:
        """
        Get the parameters schema for the tool.

        Returns:
            Schema definition for tool parameters
        """
        return AddTaskParameters.model_json_schema()

    def execute(self, parameters: AddTaskParameters) -> ToolResult:
        """
        Execute the tool to add a task.

        Args:
            parameters: Parameters for the task to add

        Returns:
            Result of tool execution
        """
        try:
            # Validate inputs
            if not parameters.title or not parameters.title.strip():
                return ToolResult(
                    success=False,
                    message="Task title is required and cannot be empty",
                    error="Title is required"
                )

            # Get the database session from the instance
            if not self.db_session:
                return ToolResult(
                    success=False,
                    message="Database session is required",
                    error="Missing database session"
                )

            # Create the task using the service
            task = TaskService.create_task(
                session=self.db_session,
                user_id=self.user_id,
                title=parameters.title.strip(),
                description=parameters.description
            )

            # Return success result
            return ToolResult(
                success=True,
                message=f"Successfully created task '{task.title}'",
                data={
                    "task_id": str(task.id),
                    "title": task.title,
                    "status": task.status,
                    "created_at": task.created_at.isoformat()
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                message="Failed to create task",
                error=str(e),
                data=None
            )