from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel
import uuid


class ToolParameters(BaseModel):
    """
    Base class for tool parameters.
    All specific tool parameters should inherit from this.
    """
    pass


class ToolResult(BaseModel):
    """
    Base class for tool results.
    """
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class BaseMCPTool(ABC):
    """
    Base class for all MCP tools.
    Defines the common interface for MCP tools in the system.
    """

    def __init__(self, user_id: uuid.UUID, db_session=None):
        """
        Initialize the MCP tool with user context.

        Args:
            user_id: ID of the user invoking the tool
            db_session: Database session for the operation
        """
        self.user_id = user_id
        self.db_session = db_session

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the tool.

        Returns:
            Tool name as a string
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Get the description of the tool.

        Returns:
            Tool description as a string
        """
        pass

    @abstractmethod
    def get_parameters_schema(self) -> Dict[str, Any]:
        """
        Get the parameters schema for the tool.

        Returns:
            Schema definition for tool parameters
        """
        pass

    @abstractmethod
    def execute(self, parameters: ToolParameters) -> ToolResult:
        """
        Execute the tool with the given parameters.

        Args:
            parameters: Tool parameters

        Returns:
            Result of tool execution
        """
        pass