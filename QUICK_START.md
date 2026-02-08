# 🚀 Quick Start Guide - AI Todo App

## ✅ System Status

- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:3001
- ✅ AI Chat Interface added
- ✅ MCP endpoints fixed
- ✅ Database connected (Neon PostgreSQL)

---

## 🎯 How to Use Your App

### Step 1: Access the App

Open your browser and go to:
```
http://localhost:3001
```

### Step 2: Sign In or Create Account

**If you don't have an account:**
1. Click "Sign Up"
2. Enter email and password
3. Click "Create Account"

**If you already have an account:**
1. Click "Sign In"
2. Enter your credentials
3. Click "Login"

### Step 3: Go to Tasks Dashboard

After login, you'll be redirected to:
```
http://localhost:3001/tasks
```

---

## 💬 Using the AI Chat (Left Panel)

The AI assistant can understand natural language! Try these:

### Create Tasks
```
You: "Create a task to buy groceries"
You: "Add a task: Call the dentist tomorrow"
You: "I need to finish the project report by Friday"
```

### View Tasks
```
You: "Show all my tasks"
You: "List my pending tasks"
You: "What tasks do I have?"
```

### Update Tasks
```
You: "Update the first task to 'Buy organic groceries'"
You: "Change task title to something else"
You: "Rename the groceries task"
```

### Complete Tasks
```
You: "Mark the first task as complete"
You: "Complete the groceries task"
You: "Finish the dentist task"
```

### Delete Tasks
```
You: "Delete the first task"
You: "Remove the groceries task"
You: "Get rid of completed tasks"
```

---

## 📋 Using the Task List (Right Panel)

Traditional UI for quick actions:

1. **Add Task**: Click "Add Task" button
2. **Edit Task**: Click ✏️ edit icon
3. **Complete Task**: Click ☐ checkbox
4. **Delete Task**: Click 🗑️ trash icon

**Changes sync with AI instantly!**

---

## 🎨 UI Overview

```
┌─────────────────────────────────────────────────┐
│         AI Task Dashboard                       │
│   Chat with AI or use task list directly       │
├──────────────────────┬──────────────────────────┤
│   🤖 AI Assistant    │     📋 Your Tasks        │
│  ┌─────────────┐    │   ┌─────────────────┐   │
│  │ Bot Avatar  │    │   │  [Add Task]     │   │
│  ├─────────────┤    │   ├─────────────────┤   │
│  │ Chat        │    │   │ ☐ Buy groceries │   │
│  │ Messages    │    │   │ ☐ Call dentist  │   │
│  │             │    │   │ ✓ Finish report │   │
│  │             │    │   └─────────────────┘   │
│  ├─────────────┤    │                          │
│  │ Input Box   │    │                          │
│  │ [Send]      │    │                          │
│  └─────────────┘    │                          │
├──────────────────────┴──────────────────────────┤
│         💡 How to Use (Help Section)            │
└─────────────────────────────────────────────────┘
```

---

## 🔧 Troubleshooting

### Problem: Chat doesn't respond

**Solution 1**: Check backend is running
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

**Solution 2**: Restart backend
```bash
cd backend
python3 -m uvicorn src.main:app --reload --port 8000
```

### Problem: Tasks not appearing

**Solution**: Check you're logged in
- Look for JWT token in browser DevTools → Application → LocalStorage
- Key: `jwt_token`
- If missing, log out and log back in

### Problem: Frontend not loading

**Solution**: Restart frontend
```bash
cd frontend
npm run dev
```

### Problem: "Not Found" errors

**Solution**: Already fixed! But if you see them:
- Frontend now uses `/mcp/*` endpoints (not `/api/v1/tasks`)
- Check `FRONTEND_MCP_FIX_COMPLETE.md` for details

---

## 📊 System Architecture

```
Browser (Port 3001)
    ↓
Frontend (Next.js)
    ↓
    ├─→ Auth: /auth/register, /auth/signin
    ├─→ Chat: /api/{user_id}/chat
    └─→ Tasks: /mcp/* (list, add, update, complete, delete)
    ↓
Backend (Port 8000)
    ↓
    ├─→ AI Agent → OpenAI
    ├─→ MCP Tools → Task operations
    └─→ Database → Neon PostgreSQL
```

---

## 🎯 Key Features

| Feature | Description | Status |
|---------|-------------|--------|
| **AI Chat** | Natural language task management | ✅ Working |
| **Task List** | Traditional CRUD interface | ✅ Working |
| **Real-time Sync** | Changes sync between chat and list | ✅ Working |
| **Authentication** | JWT-based secure auth | ✅ Working |
| **Database** | Persistent storage in Neon | ✅ Working |
| **Responsive** | Works on mobile and desktop | ✅ Working |

---

## 📚 Additional Documentation

- **CHAT_INTERFACE_ADDED.md** - Complete chat feature guide
- **FRONTEND_MCP_FIX_COMPLETE.md** - MCP integration details
- **MCP_ENDPOINTS_QUICK_REFERENCE.md** - API reference
- **PHASE3_AUTH_FIX.md** - Authentication fix details

---

## 🚀 Quick Test

1. Open http://localhost:3001
2. Sign in
3. Go to `/tasks`
4. Type in chat: **"Create a task to test the AI"**
5. See it appear in the task list instantly!
6. Try: **"Show all my tasks"**
7. Click the checkbox on the task list
8. Ask AI: **"What tasks do I have?"**

---

## ✨ Tips

**Best Practices:**
- Use **AI chat** for quick, conversational task management
- Use **task list** for visual overview and bulk operations
- Both methods work equally well - choose what feels natural!

**Pro Tips:**
- Be specific: "Create a task to buy milk tomorrow" is better than "add task"
- Use complete sentences for better AI understanding
- The AI remembers context within the conversation

---

## 📞 Support

**Backend API Docs**: http://localhost:8000/docs
**Test Script**: `./test_mcp_endpoints.sh`

---

**Your AI-powered Todo App is ready!** 🎉

Start by creating your first task via chat or the task list!
