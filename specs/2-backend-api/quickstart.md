# Quickstart: Backend API (Tasks)

## Development Setup
1. Ensure `DATABASE_URL` is set in `.env`.
2. Install dependencies: `pip install -r backend/requirements.txt`
3. Run migrations: `psql $DATABASE_URL -f backend/migrations/002_create_tasks_table.sql`
4. Start server: `uvicorn backend.app.main:app --reload`

## Example API Call
```bash
curl -X GET http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer <your-token>"
```
