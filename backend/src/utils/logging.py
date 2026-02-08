import logging
from datetime import datetime
from typing import Dict, Any
import json


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Sets up a logger with the specified name and level.

    Args:
        name: Logger name
        level: Logging level (defaults to INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding multiple handlers if logger already exists
    if logger.handlers:
        return logger

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    return logger


def log_api_call(
    endpoint: str,
    method: str,
    user_id: str,
    params: Dict[str, Any] = None,
    response_status: int = None,
    duration_ms: float = None
) -> None:
    """
    Logs API calls with structured information.

    Args:
        endpoint: API endpoint that was called
        method: HTTP method (GET, POST, etc.)
        user_id: ID of the user making the request
        params: Request parameters
        response_status: HTTP response status code
        duration_ms: Duration of the request in milliseconds
    """
    logger = setup_logger("api")

    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "api_call",
        "endpoint": endpoint,
        "method": method,
        "user_id": user_id,
        "params": params or {},
        "response_status": response_status,
        "duration_ms": duration_ms
    }

    logger.info(json.dumps(log_data))


def log_ai_interaction(
    user_id: str,
    conversation_id: str,
    user_input: str,
    ai_response: str,
    tool_calls: list = None,
    duration_ms: float = None
) -> None:
    """
    Logs AI agent interactions with structured information.

    Args:
        user_id: ID of the user interacting with the AI
        conversation_id: ID of the conversation
        user_input: The user's natural language input
        ai_response: The AI's response to the user
        tool_calls: List of tools called during the interaction
        duration_ms: Duration of the interaction in milliseconds
    """
    logger = setup_logger("ai_agent")

    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "ai_interaction",
        "user_id": user_id,
        "conversation_id": conversation_id,
        "user_input": user_input,
        "ai_response": ai_response,
        "tool_calls": tool_calls or [],
        "duration_ms": duration_ms
    }

    logger.info(json.dumps(log_data))


def log_error(error: Exception, context: str = "", user_id: str = None) -> None:
    """
    Logs errors with structured information.

    Args:
        error: The exception that occurred
        context: Context about where the error occurred
        user_id: ID of the user associated with the error (if applicable)
    """
    logger = setup_logger("error")

    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "error",
        "type": type(error).__name__,
        "message": str(error),
        "context": context,
        "user_id": user_id,
        "traceback": str(error.__traceback__) if error.__traceback__ else None
    }

    logger.error(json.dumps(log_data))