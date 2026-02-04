---
name: backend-api-core
description: Design backend APIs by defining routes, handling requests/responses, and connecting to databases.
---

# Backend API Core Skill

## Instructions

1. **Routing**
   - Define RESTful routes (GET, POST, PUT, DELETE)
   - Organize routes by resource/module
   - Use clear and consistent URL naming

2. **Request & Response Handling**
   - Parse request parameters, body, and headers
   - Validate incoming data
   - Return proper HTTP status codes
   - Send structured JSON responses

3. **Database Integration**
   - Connect to database (SQL or NoSQL)
   - Perform CRUD operations
   - Use environment variables for credentials
   - Handle connection errors gracefully

4. **Error Handling**
   - Centralized error middleware
   - Meaningful error messages
   - Avoid leaking sensitive information

## Best Practices
- Keep controllers thin and focused
- Separate routes, controllers, and services
- Use async/await for I/O operations
- Always validate and sanitize inputs
- Follow REST or API design standards

## Example Structure
```js
// routes/user.routes.js
import express from "express";
import { getUsers, createUser } from "../controllers/user.controller.js";

const router = express.Router();

router.get("/users", getUsers);
router.post("/users", createUser);

export default router;
