---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **User Registration (Signup)**
   - Collect user credentials (email, username, password)
   - Validate input data
   - Hash passwords before storing
   - Prevent duplicate accounts

2. **User Login (Signin)**
   - Verify user credentials
   - Compare hashed passwords
   - Handle invalid login attempts
   - Return authentication tokens on success

3. **Password Security**
   - Use strong hashing algorithms (bcrypt, argon2)
   - Apply salting and proper cost factors
   - Never store plain-text passwords

4. **JWT Token Management**
   - Generate access and refresh tokens
   - Sign tokens using secure secrets
   - Set expiration times
   - Verify tokens for protected routes

5. **Better Auth Integration**
   - Integrate Better Auth for simplified auth flows
   - Configure providers and adapters
   - Manage sessions and token lifecycle
   - Support scalable authentication patterns

## Best Practices
- Enforce strong password policies
- Use HTTPS for all auth endpoints
- Rotate JWT secrets periodically
- Store tokens securely (httpOnly cookies preferred)
- Implement proper error handling without leaking sensitive info
- Follow OWASP authentication guidelines

## Example Structure
```ts
// Signup
const hashedPassword = await bcrypt.hash(password, 12);
await db.user.create({
  email,
  password: hashedPassword,
});

// Signin
const isValid = await bcrypt.compare(password, user.password);
if (!isValid) throw new Error("Invalid credentials");

// JWT
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: "1h" }
);

