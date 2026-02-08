from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import uuid
from ..tools.base import ToolResult
from ..tools.add_task_tool import AddTaskTool, AddTaskParameters
from ..tools.list_tasks_tool import ListTasksTool, ListTasksParameters
from ..tools.update_task_tool import UpdateTaskTool, UpdateTaskParameters
from ..tools.complete_task_tool import CompleteTaskTool, CompleteTaskParameters
from ..tools.delete_task_tool import DeleteTaskTool, DeleteTaskParameters
from ..services.conversation_service import ConversationService
from sqlmodel import Session


class ToolCallResult(BaseModel):
    """
    Result of a tool call made by the AI agent.
    """
    tool_name: str
    parameters: Dict[str, Any]
    result: ToolResult


class TodoAgent:
    """
    Basic AI agent for processing natural language todo commands.
    This is a simplified implementation that uses rule-based parsing.
    In a production system, this would be replaced with an OpenAI agent
    that can call the MCP tools.
    """

    def __init__(self, user_id: uuid.UUID, db_session: Session, conversation_id: Optional[uuid.UUID] = None, message_id: Optional[uuid.UUID] = None):
        """
        Initialize the AI agent with user context.

        Args:
            user_id: ID of the user interacting with the agent
            db_session: Database session for operations
            conversation_id: Optional conversation ID to retrieve context from
            message_id: Optional message ID that triggered this agent call
        """
        self.user_id = user_id
        self.db_session = db_session
        self.conversation_id = conversation_id
        self.message_id = message_id  # Store the message ID
        self.conversation_context = self._load_conversation_context() if conversation_id else {}

    def _load_conversation_context(self) -> Dict[str, Any]:
        """
        Load conversation context from the database.

        Returns:
            Dictionary containing conversation context
        """
        if not self.conversation_id:
            return {}

        try:
            # Get recent messages from the conversation
            recent_messages = ConversationService.get_conversation_messages(
                session=self.db_session,
                conversation_id=self.conversation_id,
                user_id=self.user_id,
                limit=10  # Get last 10 messages
            )

            # Extract relevant context from messages
            context = {
                "recent_messages": [msg.content for msg in recent_messages],
                "message_count": len(recent_messages),
                "participants": set(msg.role for msg in recent_messages)
            }

            return context
        except Exception:
            # If there's an error loading context, return an empty context
            return {}

    def get_recent_tasks_mentioned(self) -> List[str]:
        """
        Get a list of task titles mentioned in recent conversation.

        Returns:
            List of task titles mentioned in the conversation
        """
        if not self.conversation_context.get("recent_messages"):
            return []

        # This is a simplified implementation
        # In a real system, we would use more sophisticated NLP to identify tasks
        mentioned_tasks = []

        # Look for task-like phrases in recent messages
        for message in self.conversation_context["recent_messages"]:
            # Look for common task indicators in the message
            # This is a basic implementation - a real system would use NER or similar
            lower_msg = message.lower()

            # If the message contains task-related keywords, consider it as mentioning a task
            if any(indicator in lower_msg for indicator in ["task", "to do", "todo", "need to", "have to", "should"]):
                # Extract potential task phrases
                # This is a simplified approach
                words = message.split()

                # Look for sequences that might represent task titles
                # For example, after "add" or "create" or "task"
                for i, word in enumerate(words):
                    if word.lower() in ["add", "create", "make", "task"] and i + 1 < len(words):
                        # Take the next few words as a potential task title
                        potential_task = " ".join(words[i+1:i+4])  # Take up to 3 words
                        if potential_task:
                            mentioned_tasks.append(potential_task.strip())

                    # Also look for phrases after "to" which often indicate tasks
                    if word.lower() == "to" and i + 1 < len(words):
                        potential_task = " ".join(words[i+1:i+4])  # Take up to 3 words after "to"
                        if potential_task:
                            mentioned_tasks.append(potential_task.strip())

        # Remove duplicates while preserving order
        seen = set()
        unique_tasks = []
        for task in mentioned_tasks:
            if task.lower() not in seen:
                seen.add(task.lower())
                unique_tasks.append(task)

        return unique_tasks

    def process_message(self, message: str, conversation_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a natural language message and return an appropriate response.

        Args:
            message: Natural language message from the user
            conversation_context: Optional context from the conversation history

        Returns:
            Dictionary containing the response and any tool calls made
        """
        # Preprocess the message
        processed_message = message.strip().lower()

        # Use either the provided context or the agent's stored context
        current_context = conversation_context or self.conversation_context

        # Identify intent and call appropriate tools
        tool_calls = []
        response = ""

        # Determine intent based on keywords
        if self._is_add_task_intent(processed_message):
            title, description = self._extract_task_details(processed_message)
            if title:
                tool_result = self._call_add_task_tool(title, description)
                tool_calls.append(tool_result)

                if tool_result.result.success:
                    response = f"I've added the task '{title}' to your list."
                else:
                    response = f"Sorry, I couldn't add the task: {tool_result.result.error or 'Unknown error'}"
            else:
                response = "I couldn't understand what task you wanted to add. Please be more specific."

        elif self._is_list_tasks_intent(processed_message):
            status_filter = self._extract_status_filter(processed_message)
            tool_result = self._call_list_tasks_tool(status_filter)
            tool_calls.append(tool_result)

            if tool_result.result.success and tool_result.result.data:
                tasks = tool_result.result.data.get("tasks", [])
                if tasks:
                    task_titles = [task["title"] for task in tasks[:5]]  # Limit to first 5 tasks
                    response = f"You have {len(tasks)} tasks. Here are some: {', '.join(task_titles)}"
                else:
                    response = "You don't have any tasks yet."
            else:
                response = "I couldn't retrieve your tasks."

        elif self._is_complete_task_intent(processed_message):
            task_identifier = self._extract_task_identifier(processed_message)

            # If no specific identifier is given, try to infer from conversation context
            if not task_identifier and current_context:
                recent_tasks = self.get_recent_tasks_mentioned()
                if recent_tasks:
                    # Use the most recently mentioned task
                    task_identifier = recent_tasks[-1]

            if task_identifier:
                # First, find the task by title or other identifier
                list_result = self._call_list_tasks_tool(None)
                if list_result.result.success and list_result.result.data:
                    tasks = list_result.result.data.get("tasks", [])
                    target_task = self._find_task_by_identifier(tasks, task_identifier)

                    if target_task:
                        complete_result = self._call_complete_task_tool(str(target_task["id"]))
                        tool_calls.extend([list_result, complete_result])

                        if complete_result.result.success:
                            response = f"I've marked the task '{target_task['title']}' as completed."
                        else:
                            response = f"Sorry, I couldn't complete the task: {complete_result.result.error or 'Unknown error'}"
                    else:
                        response = f"I couldn't find a task matching '{task_identifier}'. Could you clarify which task you want to complete?"
                else:
                    response = "I couldn't find your tasks to complete."
            else:
                response = "To complete a task, please specify which task you want to complete."

        elif self._is_update_task_intent(processed_message):
            # Simplified update - just handle title changes for now
            task_identifier, new_title = self._extract_task_and_new_title(processed_message)

            # If no specific identifier is given, try to infer from conversation context
            if not task_identifier and current_context:
                recent_tasks = self.get_recent_tasks_mentioned()
                if recent_tasks:
                    # Use the most recently mentioned task
                    task_identifier = recent_tasks[-1]

            if task_identifier and new_title:
                # Find the task
                list_result = self._call_list_tasks_tool(None)
                if list_result.result.success and list_result.result.data:
                    tasks = list_result.result.data.get("tasks", [])
                    target_task = self._find_task_by_identifier(tasks, task_identifier)

                    if target_task:
                        update_result = self._call_update_task_tool(str(target_task["id"]), new_title)
                        tool_calls.extend([list_result, update_result])

                        if update_result.result.success:
                            response = f"I've updated the task '{target_task['title']}' to '{new_title}'."
                        else:
                            response = f"Sorry, I couldn't update the task: {update_result.result.error or 'Unknown error'}"
                    else:
                        response = f"I couldn't find a task matching '{task_identifier}'. Could you clarify which task you want to update?"
                else:
                    response = "I couldn't find your tasks to update."
            else:
                response = "To update a task, please specify which task and the new information."

        elif self._is_delete_task_intent(processed_message):
            task_identifier = self._extract_task_identifier(processed_message)

            # If no specific identifier is given, try to infer from conversation context
            if not task_identifier and current_context:
                recent_tasks = self.get_recent_tasks_mentioned()
                if recent_tasks:
                    # Use the most recently mentioned task
                    task_identifier = recent_tasks[-1]

            if task_identifier:
                # Find the task
                list_result = self._call_list_tasks_tool(None)
                if list_result.result.success and list_result.result.data:
                    tasks = list_result.result.data.get("tasks", [])
                    target_task = self._find_task_by_identifier(tasks, task_identifier)

                    if target_task:
                        delete_result = self._call_delete_task_tool(str(target_task["id"]))
                        tool_calls.extend([list_result, delete_result])

                        if delete_result.result.success:
                            response = f"I've deleted the task '{target_task['title']}'."
                        else:
                            response = f"Sorry, I couldn't delete the task: {delete_result.result.error or 'Unknown error'}"
                    else:
                        response = f"I couldn't find a task matching '{task_identifier}'. Could you clarify which task you want to delete?"
                else:
                    response = "I couldn't find your tasks to delete."
            else:
                response = "To delete a task, please specify which task you want to delete."

        else:
            # Default response for unrecognized intents
            response = (f"I received your message: '{message}'. I can help you manage your tasks by adding, listing, "
                       f"updating, completing, or deleting them. Try saying something like 'Add a task to buy groceries' "
                       f"or 'Show me my tasks'.")

        return {
            "response": response,
            "tool_calls": tool_calls,
            "intent": self._identify_intent(processed_message)
        }

    def _identify_intent(self, message: str) -> str:
        """
        Identify the intent from the user's message.

        Args:
            message: Lowercase user message

        Returns:
            Intent as a string
        """
        if self._is_add_task_intent(message):
            return "add_task"
        elif self._is_list_tasks_intent(message):
            return "list_tasks"
        elif self._is_complete_task_intent(message):
            return "complete_task"
        elif self._is_update_task_intent(message):
            return "update_task"
        elif self._is_delete_task_intent(message):
            return "delete_task"
        else:
            return "unknown"

    def _is_add_task_intent(self, message: str) -> bool:
        """
        Check if the message indicates an intent to add a task.

        Args:
            message: Lowercase user message

        Returns:
            True if the intent is to add a task, False otherwise
        """
        # Explicit add keywords
        add_keywords = ["add", "create", "make", "new", "put in", "enter", "remember"]

        # Implicit task indicators (common phrases that imply task creation)
        implicit_task_phrases = [
            "i have to", "i need to", "i should", "i must", "i will", "i want to",
            "need to", "have to", "should", "must", "going to", "gonna",
            "remind me to", "don't forget to"
        ]

        # Task-related words
        task_related = ["task", "todo", "to do", "thing", "item"]

        # Check for explicit add keywords
        has_add_keyword = any(keyword in message for keyword in add_keywords)

        # Check for implicit task phrases (these strongly suggest task creation)
        has_implicit_phrase = any(phrase in message for phrase in implicit_task_phrases)

        # Check for task-related words
        has_task_related = any(keyword in message for keyword in task_related)

        # Intent is "add task" if:
        # 1. Has explicit add keyword (e.g., "add task to...")
        # 2. Has implicit phrase (e.g., "I have to pay bills")
        # 3. Has add keyword + task related word
        return has_add_keyword or has_implicit_phrase or (has_task_related and has_add_keyword)

    def _is_list_tasks_intent(self, message: str) -> bool:
        """
        Check if the message indicates an intent to list tasks.

        Args:
            message: Lowercase user message

        Returns:
            True if the intent is to list tasks, False otherwise
        """
        list_keywords = ["list", "show", "display", "view", "see", "what", "my", "all", "current"]
        task_related = ["tasks", "todos", "to dos", "things", "items", "list"]

        has_list_keyword = any(keyword in message for keyword in list_keywords)
        has_task_related = any(keyword in message for keyword in task_related)

        return (has_list_keyword and has_task_related) or "my tasks" in message

    def _is_complete_task_intent(self, message: str) -> bool:
        """
        Check if the message indicates an intent to complete a task.

        Args:
            message: Lowercase user message

        Returns:
            True if the intent is to complete a task, False otherwise
        """
        complete_keywords = ["complete", "done", "finished", "finish", "mark as"]
        task_related = ["task", "todo", "to do", "thing", "item"]

        has_complete_keyword = any(keyword in message for keyword in complete_keywords)
        has_task_related = any(keyword in message for keyword in task_related)

        return has_complete_keyword and has_task_related

    def _is_update_task_intent(self, message: str) -> bool:
        """
        Check if the message indicates an intent to update a task.

        Args:
            message: Lowercase user message

        Returns:
            True if the intent is to update a task, False otherwise
        """
        update_keywords = ["update", "change", "modify", "edit", "alter", "switch"]
        task_related = ["task", "todo", "to do", "thing", "item"]

        has_update_keyword = any(keyword in message for keyword in update_keywords)
        has_task_related = any(keyword in message for keyword in task_related)

        return has_update_keyword and has_task_related

    def _is_delete_task_intent(self, message: str) -> bool:
        """
        Check if the message indicates an intent to delete a task.

        Args:
            message: Lowercase user message

        Returns:
            True if the intent is to delete a task, False otherwise
        """
        delete_keywords = ["delete", "remove", "erase", "get rid of", "cancel"]
        task_related = ["task", "todo", "to do", "thing", "item"]

        has_delete_keyword = any(keyword in message for keyword in delete_keywords)
        has_task_related = any(keyword in message for keyword in task_related)

        return has_delete_keyword and has_task_related

    def _extract_task_details(self, message: str) -> tuple:
        """
        Extract task title and description from the user's message.

        Args:
            message: Lowercase user message

        Returns:
            Tuple of (title, description) or (None, None) if not found
        """
        # Remove common prefixes
        explicit_prefixes = [
            "add task ", "create task ", "make task ", "new task ",
            "add a task ", "create a task ", "make a task ",
            "add ", "create ", "make ", "new ",
            "remind me to ", "remember to ", "don't forget to "
        ]

        # Remove implicit phrases that indicate intent but aren't part of the task
        implicit_phrases = [
            "i have to ", "i need to ", "i should ", "i must ", "i will ", "i want to ",
            "need to ", "have to ", "should ", "must ", "going to ", "gonna ",
            "add a task that ", "create a task that "
        ]

        normalized = message.strip()

        # First, try explicit prefixes
        for prefix in explicit_prefixes:
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix):].strip()
                break

        # Then, try implicit phrases
        for phrase in implicit_phrases:
            if normalized.startswith(phrase):
                normalized = normalized[len(phrase):].strip()
                break

        # Remove remaining connector words if they're at the start
        connector_words = ["to ", "that ", "task ", "a task ", "the task "]
        for word in connector_words:
            if normalized.startswith(word):
                normalized = normalized[len(word):].strip()

        # Clean up the extracted task title
        if normalized and len(normalized) > 2:
            # Capitalize first letter
            return normalized[0].upper() + normalized[1:], ""

        return None, None

    def _extract_status_filter(self, message: str) -> Optional[str]:
        """
        Extract status filter from the message (e.g., "show completed tasks").

        Args:
            message: Lowercase user message

        Returns:
            Status filter or None if not found
        """
        if "completed" in message or "done" in message:
            return "completed"
        elif "pending" in message or "not done" in message:
            return "pending"
        elif "in progress" in message:
            return "in_progress"
        return None

    def _extract_task_identifier(self, message: str) -> Optional[str]:
        """
        Extract a task identifier from the message (e.g., task name or partial name).

        Args:
            message: Lowercase user message

        Returns:
            Task identifier or None if not found
        """
        # Remove common phrases like "the task", "that task", etc.
        message = message.replace("the task", "").replace("that task", "").replace("task", "").strip()

        # Look for keywords that might indicate what task they mean
        exclude_words = ["complete", "done", "finish", "mark", "update", "change", "delete", "remove", "as"]
        words = message.split()
        filtered_words = [word for word in words if word not in exclude_words and len(word) > 2]

        if filtered_words:
            # Return the most likely identifier (could be improved with NLP)
            return " ".join(filtered_words)

        return None

    def _extract_task_and_new_title(self, message: str) -> tuple:
        """
        Extract the task identifier and new title from an update message.

        Args:
            message: Lowercase user message

        Returns:
            Tuple of (task_identifier, new_title) or (None, None) if not found
        """
        # Look for patterns like "change 'old task' to 'new task'"
        import re

        # Simple pattern matching for now
        if "to" in message:
            parts = message.split("to", 1)  # Split on first occurrence of "to"
            if len(parts) == 2:
                task_part = parts[0].strip()
                new_title_part = parts[1].strip()

                # Remove update-related words from the task part
                update_words = ["update", "change", "modify", "edit", "alter", "switch"]
                for word in update_words:
                    task_part = task_part.replace(word, "").strip()

                # Remove common phrases
                task_part = task_part.replace("task", "").replace("the", "").replace("a", "").strip()

                if task_part and new_title_part:
                    return task_part, new_title_part.capitalize()

        return None, None

    def _find_task_by_identifier(self, tasks: List[Dict[str, Any]], identifier: str) -> Optional[Dict[str, Any]]:
        """
        Find a task in the list by its identifier (title or partial title).

        Args:
            tasks: List of task dictionaries
            identifier: Identifier to search for

        Returns:
            Matching task dictionary or None if not found
        """
        if not identifier:
            return None

        identifier_lower = identifier.lower()

        # First, try exact match
        for task in tasks:
            if task["title"].lower() == identifier_lower:
                return task

        # Then, try partial match
        for task in tasks:
            if identifier_lower in task["title"].lower():
                return task

        # Finally, try if any word in identifier matches any word in title
        identifier_words = set(identifier_lower.split())
        for task in tasks:
            task_words = set(task["title"].lower().split())
            if identifier_words.intersection(task_words):
                return task

        return None

    def _call_add_task_tool(self, title: str, description: str = "") -> ToolCallResult:
        """
        Call the add task tool.

        Args:
            title: Title of the task to add
            description: Optional description of the task

        Returns:
            Tool call result
        """
        tool = AddTaskTool(user_id=self.user_id, db_session=self.db_session)
        params = AddTaskParameters(title=title, description=description)
        result = tool.execute(params)

        # Save the tool call to the database if we have a conversation
        if self.conversation_id:
            try:
                ConversationService.save_tool_call(
                    session=self.db_session,
                    conversation_id=self.conversation_id,
                    message_id=uuid.uuid4(),  # This would need to be the actual message ID
                    user_id=self.user_id,
                    tool_name=tool.get_name(),
                    parameters=params.dict(),
                    result=result.dict()
                )
            except Exception:
                # If saving the tool call fails, continue anyway
                pass

        return ToolCallResult(
            tool_name=tool.get_name(),
            parameters=params.dict(),
            result=result
        )

    def _call_list_tasks_tool(self, status_filter: Optional[str]) -> ToolCallResult:
        """
        Call the list tasks tool.

        Args:
            status_filter: Optional status filter

        Returns:
            Tool call result
        """
        tool = ListTasksTool(user_id=self.user_id, db_session=self.db_session)
        params = ListTasksParameters(status=status_filter)
        result = tool.execute(params)

        # Save the tool call to the database if we have a conversation
        if self.conversation_id:
            try:
                ConversationService.save_tool_call(
                    session=self.db_session,
                    conversation_id=self.conversation_id,
                    message_id=uuid.uuid4(),  # This would need to be the actual message ID
                    user_id=self.user_id,
                    tool_name=tool.get_name(),
                    parameters=params.dict(),
                    result=result.dict()
                )
            except Exception:
                # If saving the tool call fails, continue anyway
                pass

        return ToolCallResult(
            tool_name=tool.get_name(),
            parameters=params.dict(),
            result=result
        )

    def _call_update_task_tool(self, task_id: str, new_title: str = None) -> ToolCallResult:
        """
        Call the update task tool.

        Args:
            task_id: ID of the task to update
            new_title: New title for the task

        Returns:
            Tool call result
        """
        tool = UpdateTaskTool(user_id=self.user_id, db_session=self.db_session)
        params = UpdateTaskParameters(task_id=task_id, title=new_title)
        result = tool.execute(params)

        # Save the tool call to the database if we have a conversation
        if self.conversation_id:
            try:
                ConversationService.save_tool_call(
                    session=self.db_session,
                    conversation_id=self.conversation_id,
                    message_id=uuid.uuid4(),  # This would need to be the actual message ID
                    user_id=self.user_id,
                    tool_name=tool.get_name(),
                    parameters=params.dict(),
                    result=result.dict()
                )
            except Exception:
                # If saving the tool call fails, continue anyway
                pass

        return ToolCallResult(
            tool_name=tool.get_name(),
            parameters=params.dict(),
            result=result
        )

    def _call_complete_task_tool(self, task_id: str) -> ToolCallResult:
        """
        Call the complete task tool.

        Args:
            task_id: ID of the task to complete

        Returns:
            Tool call result
        """
        tool = CompleteTaskTool(user_id=self.user_id, db_session=self.db_session)
        params = CompleteTaskParameters(task_id=task_id)
        result = tool.execute(params)

        # Save the tool call to the database if we have a conversation
        if self.conversation_id:
            try:
                ConversationService.save_tool_call(
                    session=self.db_session,
                    conversation_id=self.conversation_id,
                    message_id=uuid.uuid4(),  # This would need to be the actual message ID
                    user_id=self.user_id,
                    tool_name=tool.get_name(),
                    parameters=params.dict(),
                    result=result.dict()
                )
            except Exception:
                # If saving the tool call fails, continue anyway
                pass

        return ToolCallResult(
            tool_name=tool.get_name(),
            parameters=params.dict(),
            result=result
        )

    def _call_delete_task_tool(self, task_id: str) -> ToolCallResult:
        """
        Call the delete task tool.

        Args:
            task_id: ID of the task to delete

        Returns:
            Tool call result
        """
        tool = DeleteTaskTool(user_id=self.user_id, db_session=self.db_session)
        params = DeleteTaskParameters(task_id=task_id)
        result = tool.execute(params)

        # Save the tool call to the database if we have a conversation
        if self.conversation_id:
            try:
                ConversationService.save_tool_call(
                    session=self.db_session,
                    conversation_id=self.conversation_id,
                    message_id=uuid.uuid4(),  # This would need to be the actual message ID
                    user_id=self.user_id,
                    tool_name=tool.get_name(),
                    parameters=params.dict(),
                    result=result.dict()
                )
            except Exception:
                # If saving the tool call fails, continue anyway
                pass

        return ToolCallResult(
            tool_name=tool.get_name(),
            parameters=params.dict(),
            result=result
        )