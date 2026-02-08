from sqlmodel import Session, select
from typing import List, Optional
import uuid
from datetime import datetime
from ..models.conversation import Conversation
from ..models.message import Message
from ..utils.errors import NotFoundException, ValidationException
from ..utils.logging import log_error


class ConversationService:
    """
    Service class for handling conversation-related operations.
    """

    @staticmethod
    def create_conversation(session: Session, user_id: uuid.UUID, title: str = None) -> Conversation:
        """
        Create a new conversation for a user.

        Args:
            session: Database session
            user_id: ID of the user creating the conversation
            title: Optional title for the conversation (auto-generated if not provided)

        Returns:
            Created Conversation object
        """
        try:
            # Generate a title if not provided
            if not title:
                title = f"Conversation on {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"

            # Create the conversation
            conversation = Conversation(
                user_id=user_id,
                title=title,
                started_at=datetime.utcnow(),
                last_message_at=datetime.utcnow(),
                status="active"
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

            return conversation
        except Exception as e:
            log_error(e, "Creating conversation", str(user_id))
            session.rollback()
            raise

    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Conversation]:
        """
        Get a specific conversation by its ID for a user.

        Args:
            session: Database session
            conversation_id: ID of the conversation to retrieve
            user_id: ID of the user (to ensure access control)

        Returns:
            Conversation object if found and belongs to user, None otherwise
        """
        try:
            conversation = session.get(Conversation, conversation_id)

            # Ensure the conversation belongs to the user
            if conversation and conversation.user_id != user_id:
                return None

            return conversation
        except Exception as e:
            log_error(e, "Retrieving conversation by ID", str(user_id))
            raise

    @staticmethod
    def get_user_conversations(
        session: Session,
        user_id: uuid.UUID,
        limit: int = 10,
        offset: int = 0,
        status_filter: Optional[str] = None
    ) -> List[Conversation]:
        """
        Get conversations for a user with pagination and optional status filter.

        Args:
            session: Database session
            user_id: ID of the user whose conversations to retrieve
            limit: Number of conversations to return
            offset: Offset for pagination
            status_filter: Optional status to filter conversations by (active, archived)

        Returns:
            List of Conversation objects for the user
        """
        try:
            query = select(Conversation).where(Conversation.user_id == user_id)

            if status_filter:
                query = query.where(Conversation.status == status_filter)

            query = query.order_by(Conversation.last_message_at.desc()).offset(offset).limit(limit)

            conversations = session.exec(query).all()
            return conversations
        except Exception as e:
            log_error(e, "Retrieving user conversations", str(user_id))
            raise

    @staticmethod
    def add_message_to_conversation(
        session: Session,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
        role: str,
        content: str,
        metadata: Optional[dict] = None
    ) -> Message:
        """
        Add a message to a conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation to add message to
            user_id: ID of the user (to ensure access control)
            role: Role of the message sender (user, assistant)
            content: Content of the message
            metadata: Optional metadata about the message

        Returns:
            Created Message object
        """
        try:
            # Verify that the conversation belongs to the user
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.user_id != user_id:
                raise NotFoundException(detail="Conversation not found or doesn't belong to user")

            # Create the message
            message = Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role=role,
                content=content,
                timestamp=datetime.utcnow(),
                metadata=metadata or {}
            )
            session.add(message)

            # Update the conversation's last message timestamp
            conversation.last_message_at = datetime.utcnow()
            session.add(conversation)

            session.commit()
            session.refresh(message)

            return message
        except NotFoundException:
            raise
        except Exception as e:
            log_error(e, "Adding message to conversation", str(user_id))
            session.rollback()
            raise

    @staticmethod
    def get_conversation_messages(
        session: Session,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
        limit: int = 50,
        offset: int = 0
    ) -> List[Message]:
        """
        Get messages from a conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation to get messages from
            user_id: ID of the user (to ensure access control)
            limit: Number of messages to return
            offset: Offset for pagination

        Returns:
            List of Message objects from the conversation
        """
        try:
            # Verify that the conversation belongs to the user
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.user_id != user_id:
                raise NotFoundException(detail="Conversation not found or doesn't belong to user")

            # Get messages for the conversation
            query = select(Message).where(Message.conversation_id == conversation_id)
            query = query.order_by(Message.timestamp.asc()).offset(offset).limit(limit)

            messages = session.exec(query).all()
            return messages
        except NotFoundException:
            raise
        except Exception as e:
            log_error(e, "Retrieving conversation messages", str(user_id))
            raise

    @staticmethod
    def update_conversation_title(
        session: Session,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
        new_title: str
    ) -> Optional[Conversation]:
        """
        Update the title of a conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation to update
            user_id: ID of the user (to ensure access control)
            new_title: New title for the conversation

        Returns:
            Updated Conversation object if successful, None if not found or not owned by user
        """
        try:
            # Get the conversation
            conversation = session.get(Conversation, conversation_id)

            # Ensure the conversation exists and belongs to the user
            if not conversation or conversation.user_id != user_id:
                return None

            # Update the title
            conversation.title = new_title
            conversation.updated_at = datetime.utcnow()

            session.add(conversation)
            session.commit()
            session.refresh(conversation)

            return conversation
        except Exception as e:
            log_error(e, "Updating conversation title", str(user_id))
            session.rollback()
            raise

    @staticmethod
    def archive_conversation(
        session: Session,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> bool:
        """
        Archive a conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation to archive
            user_id: ID of the user (to ensure access control)

        Returns:
            True if conversation was archived, False if not found or not owned by user
        """
        try:
            # Get the conversation
            conversation = session.get(Conversation, conversation_id)

            # Ensure the conversation exists and belongs to the user
            if not conversation or conversation.user_id != user_id:
                return False

            # Update status to archived
            conversation.status = "archived"
            conversation.updated_at = datetime.utcnow()

            session.add(conversation)
            session.commit()

            return True
        except Exception as e:
            log_error(e, "Archiving conversation", str(user_id))
            session.rollback()
            raise

    @staticmethod
    def save_tool_call(
        session: Session,
        conversation_id: uuid.UUID,
        message_id: uuid.UUID,
        user_id: uuid.UUID,
        tool_name: str,
        parameters: dict,
        result: dict
    ) -> Optional["ToolCall"]:
        """
        Save a tool call to the database.

        Args:
            session: Database session
            conversation_id: ID of the conversation where the tool was called
            message_id: ID of the message that triggered this tool call
            user_id: ID of the user who initiated the action
            tool_name: Name of the MCP tool that was called
            parameters: Parameters passed to the tool
            result: Result returned by the tool

        Returns:
            Created ToolCall object if successful, None otherwise
        """
        try:
            # Verify that the conversation belongs to the user
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.user_id != user_id:
                raise NotFoundException(detail="Conversation not found or doesn't belong to user")

            # Verify that the message belongs to the user
            message = session.get(Message, message_id)
            if not message or message.user_id != user_id:
                raise NotFoundException(detail="Message not found or doesn't belong to user")

            # Create the tool call
            tool_call = ToolCall(
                conversation_id=conversation_id,
                message_id=message_id,
                user_id=user_id,
                tool_name=tool_name,
                parameters=parameters,
                result=result,
                timestamp=datetime.utcnow()
            )

            session.add(tool_call)
            session.commit()
            session.refresh(tool_call)

            return tool_call
        except NotFoundException:
            raise
        except Exception as e:
            log_error(e, "Saving tool call", str(user_id))
            session.rollback()
            raise