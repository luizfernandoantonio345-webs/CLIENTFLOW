# GitHub Copilot Instructions for ClientFlow

## Project Overview

ClientFlow is a multi-tenant SaaS system for managing clients and customer service for local businesses (mechanics, workshops, etc.).

## Tech Stack

### Backend
- **Python 3.8+** with FastAPI framework
- **SQLAlchemy** ORM with PostgreSQL/SQLite
- **Alembic** for database migrations
- **Redis** for session management
- **Passlib + Bcrypt** for password encryption
- **Pydantic** for data validation

### Frontend
- **HTML5, CSS3** (dark theme)
- **Vanilla JavaScript** (no framework)
- **Chart.js** for visualizations

## Project Structure

```
ClientFlow/
├── backend/           # FastAPI backend application
│   ├── main.py       # API entry point with routes
│   ├── database.py   # Database configuration
│   ├── models.py     # SQLAlchemy models
│   ├── schemas.py    # Pydantic schemas
│   ├── auth.py       # Authentication logic
│   ├── sessions.py   # Session management
│   ├── routers/      # API route modules
│   └── services.py   # Business logic services
├── frontend/         # Static HTML/CSS/JS frontend
├── tests/           # Test suite
├── alembic/         # Database migrations
└── infra/           # Infrastructure as Code (Terraform)
```

## Development Guidelines

### Building and Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run backend server (development)
cd backend && python main.py

# Run tests
pytest tests/

# Create database migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### Code Style
- Follow PEP 8 for Python code
- Use type hints in Python functions
- Keep functions small and focused
- Use descriptive variable and function names
- Add docstrings to functions and classes

### Security
- Never commit secrets or API keys
- Always hash passwords with bcrypt
- Use Pydantic for input validation
- Implement proper authentication checks
- Follow multi-tenant isolation principles (each empresa_id must be validated)

### Database
- All models extend SQLAlchemy Base
- Use Alembic for migrations (never modify database directly)
- Maintain multi-tenant isolation via empresa_id foreign keys
- Main tables: empresas, clientes, atendimentos

### API Endpoints
- Follow REST conventions
- Use proper HTTP status codes
- Return consistent JSON responses
- Include proper error handling
- Document endpoints with FastAPI docstrings

## Important Rules

1. **Multi-tenant Isolation**: Always filter queries by empresa_id from session
2. **Security First**: Never expose sensitive data in API responses
3. **Minimal Changes**: Only modify code directly related to the task
4. **Test Before Commit**: Run existing tests to ensure no regressions
5. **Documentation**: Update README if public API changes

## Common Tasks

- Add new API endpoint → Create route in appropriate router file
- Add database field → Update model, create Alembic migration, update schema
- Add frontend feature → Modify HTML/CSS/JS in frontend directory
- Fix security issue → Check auth.py, sessions.py, and model permissions

## Files to Never Modify

- `.env.example` (only add new vars, never remove)
- `requirements.txt` (only add if absolutely necessary)
- Database models (use migrations instead)

## When in Doubt

- Check existing code patterns in the same module
- Refer to FastAPI documentation for API design
- Follow SQLAlchemy best practices for database operations
- Maintain consistency with existing code style
