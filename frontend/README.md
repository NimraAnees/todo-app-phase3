# Todo App Frontend

A responsive Next.js frontend for the Todo application with secure API integration.

## Features

- **Authentication**: Secure login and signup with JWT token management
- **Task Management**: Create, read, update, and delete tasks
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Loading States**: Visual feedback during API operations
- **Error Handling**: Proper error messages and recovery

## Tech Stack

- Next.js 14+ (App Router)
- React 18+
- TypeScript
- Tailwind CSS
- Better Auth client

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
3. Create environment variables:
   ```bash
   cp .env.local.example .env.local
   ```
4. Update the environment variables in `.env.local` with your backend API URL

### Development

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: Base URL of the backend API (e.g., `http://localhost:8000`)

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication pages
│   ├── tasks/             # Tasks page
│   └── layout.tsx         # Root layout
├── components/            # Reusable UI components
│   ├── auth/              # Authentication components
│   ├── tasks/             # Task management components
│   ├── ui/                # Generic UI components
│   └── providers/         # Context providers
├── lib/                   # Utility functions and services
│   ├── api/               # API client and services
│   └── utils/             # Utility functions
├── hooks/                 # Custom React hooks
└── public/                # Static assets
```

## API Integration

The frontend communicates with the backend API using JWT authentication. All API requests automatically include the JWT token in the Authorization header.

## Security

- JWT tokens are securely stored in localStorage
- All API requests are authenticated with JWT tokens
- Input validation is performed on both frontend and backend
- User data isolation is enforced by the backend
