from .base import BaseMCPTool, ToolParameters, ToolResult
from typing import Dict, Any, Optional
from pydantic import Field
from sqlmodel import Session
import uuid
from ..services.task_service import TaskService


class ListTasksParameters(ToolParameters):
    """
    Parameters for the list_tasks tool.
    """
    status: Optional[str] = Field(None, description="Filter tasks by status (pending, in_progress, completed)")


class ListTasksTool(BaseMCPTool):
    """
    MCP Tool for listing tasks.
    """

    def get_name(self) -> str:
        """
        Get the name of the tool.

        Returns:
            Tool name as a string
        """
        return "list_tasks_tool"

    def get_description(self) -> str:
        """
        Get the description of the tool.

        Returns:
            Tool description as a string
        """
        return "Lists all tasks for the user, optionally filtered by status."

    def get_parameters_schema(self) -> Dict[str, Any]:
        """
        Get the parameters schema for the tool.

        Returns:
            Schema definition for tool parameters
        """
        return ListTasksParameters.model_json_schema()

    def execute(self, parameters: ListTasksParameters) -> ToolResult:
        """
        Execute the tool to list tasks.

        Args:
            parameters: Parameters for filtering tasks

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

            # Get tasks using the service
            tasks = TaskService.get_user_tasks(
                session=self.db_session,
                user_id=self.user_id,
                status_filter=parameters.status
            )

            # Format the result
            tasks_list = []
            for task in tasks:
                tasks_list.append({
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None
                })

            # Return success result
            return ToolResult(
                success=True,
                message=f"Retrieved {len(tasks_list)} tasks",
                data={
                    "tasks": tasks_list,
                    "count": len(tasks_list),
                    "status_filter": parameters.status
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                message="Failed to list tasks",
                error=str(e),
                data=None
            )