# Quickstart Guide: AI Chat Agent & Conversation System

**Feature**: AI Chat Agent & Conversation System
**Date**: 2026-02-06

## Overview
This guide provides instructions for setting up and running the AI Chat Agent & Conversation System. This system allows users to manage their todo list through natural language conversations with an AI agent.

## Prerequisites
- Python 3.11+
- pip package manager
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)
- OpenAI API key
- Better Auth account
- MCP Server installation

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the backend directory with the following:
```env
DATABASE_URL=postgresql://username:password@host:port/database_name
JWT_SECRET=your_jwt_secret_here
BETTER_AUTH_SECRET=your_better_auth_secret
OPENAI_API_KEY=your_openai_api_key
MCP_SECRET=your_mcp_server_secret
DEBUG=true  # Set to false for production
```

### 4. Set Up Database
```bash
# Run database migrations
python -m backend.migrations.run
```

### 5. Start the Server
```bash
uvicorn backend.src.main:app --reload --host 0.0.0.0 --port 8000
```

## API Usage Examples

### Authenticate User
First, register or login to obtain a JWT token:
```bash
POST /api/auth/register
Content-Type: application/json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

### Send Chat Message
Send a natural language message to the AI agent:
```bash
POST /api/{user_id}/chat
Authorization: Bearer {your-jwt-token}
Content-Type: application/json

{
  "message": "Add a task to buy groceries",
  "conversation_id": "optional-conversation-id-if-continuing"
}
```

Response:
```json
{
  "response": "I've added the task 'buy groceries' to your list.",
  "conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "message_id": "b2c3d4e5-f6g7-8901-2345-67890abcdef1",
  "tool_calls": [
    {
      "tool_name": "add_task_tool",
      "parameters": {"title": "buy groceries"},
      "result": {"task_id": "c3d4e5f6-g7h8-9012-3456-7890abcdef12"}
    }
  ],
  "context_preserved": true
}
```

### Get Conversation History
Retrieve a list of your conversations:
```bash
GET /api/{user_id}/conversations?limit=10&offset=0
Authorization: Bearer {your-jwt-token}
```

## AI Capabilities

The AI agent can understand and respond to natural language commands for:
- Adding tasks: "Add a task to buy groceries"
- Listing tasks: "Show me my tasks" or "What do I have to do?"
- Updating tasks: "Change the title of my meeting task to 'Team sync'"
- Completing tasks: "Mark my grocery task as complete"
- Deleting tasks: "Remove the old task from my list"

## Troubleshooting

### Common Issues
1. **JWT Token Issues**: Ensure the token is properly included in the Authorization header
2. **Database Connection**: Verify DATABASE_URL is correct and database is accessible
3. **MCP Tools Not Responding**: Check that MCP server is running and properly configured
4. **AI Not Understanding Commands**: Use clear, specific language for better interpretation

### API Response Codes
- 200: Success
- 400: Bad request (invalid input)
- 401: Unauthorized (missing or invalid JWT)
- 403: Forbidden (attempting to access other user's data)
- 500: Server error (check server logs)

## Development Tips

### Running Tests
```bash
# Run backend tests
pytest tests/

# Run contract tests
pytest tests/contract/
```

### Local Development
The server supports hot-reloading with the `--reload` flag. Changes to code will automatically restart the server during development.

### Environment Variables
For local development, you can use a local PostgreSQL instance or Neon's local development environment. Remember to never commit `.env` files to version control.