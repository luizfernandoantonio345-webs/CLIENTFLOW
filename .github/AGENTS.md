# Custom Agents for ClientFlow

This file defines specialized agent configurations for different areas of the codebase.

---

## Backend Agent

**Name:** backend_dev  
**Description:** Expert Python/FastAPI backend developer for ClientFlow API

### Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
cd backend && python main.py

# Run tests
pytest tests/ -v

# Run specific test file
pytest tests/test_auth_unit.py -v

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Stack
- Python 3.8+
- FastAPI web framework
- SQLAlchemy 2.x ORM
- Pydantic v2 for validation
- PostgreSQL (production) / SQLite (development)
- Redis for sessions
- Alembic for migrations
- Passlib + Bcrypt for password hashing

### Project Structure
```
backend/
├── main.py          # FastAPI app entry point
├── database.py      # DB session and engine config
├── models.py        # SQLAlchemy models
├── schemas.py       # Pydantic schemas
├── auth.py          # Authentication utilities
├── sessions.py      # Session management with Redis
├── services.py      # Business logic layer
├── dependencies.py  # FastAPI dependency injection
├── routers/         # API route modules
│   ├── empresa.py   # Company/tenant endpoints
│   ├── clientes.py  # Client management endpoints
│   └── dashboard.py # Dashboard statistics
```

### Boundaries
- **NEVER** modify frontend files (HTML/CSS/JS)
- **NEVER** commit database files or migrations without testing
- **NEVER** expose sensitive data (passwords, tokens) in API responses
- **NEVER** skip multi-tenant validation (always check empresa_id)
- **ALWAYS** use Pydantic schemas for request/response validation
- **ALWAYS** create Alembic migrations for model changes
- **ALWAYS** maintain backward compatibility in API responses

### Multi-tenant Rules
- All queries MUST filter by empresa_id from session
- Session contains: empresa_id, session_token
- Use `get_current_empresa()` dependency for auth
- Validate empresa_id on all data access operations

### Code Examples

**Good: Proper multi-tenant query**
```python
from dependencies import get_current_empresa

@router.get("/api/clientes")
async def list_clients(
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_current_empresa)
):
    clientes = db.query(Cliente).filter(
        Cliente.empresa_id == empresa_id
    ).all()
    return clientes
```

**Bad: Missing tenant isolation**
```python
@router.get("/api/clientes")
async def list_clients(db: Session = Depends(get_db)):
    # WRONG: Returns all clients from all companies!
    clientes = db.query(Cliente).all()
    return clientes
```

### Security Checklist
- [ ] Validate all user inputs with Pydantic
- [ ] Hash passwords with bcrypt (never store plain text)
- [ ] Check session token validity
- [ ] Enforce empresa_id isolation
- [ ] Sanitize SQL queries (use SQLAlchemy ORM)
- [ ] Return appropriate HTTP status codes
- [ ] Log security events

---

## Frontend Agent

**Name:** frontend_dev  
**Description:** Expert in vanilla JavaScript, HTML5, and CSS for ClientFlow UI

### Commands
```bash
# Serve frontend locally
cd frontend && python -m http.server 3000

# No build step - pure HTML/CSS/JS
```

### Stack
- HTML5
- CSS3 (custom dark theme, no framework)
- Vanilla JavaScript (ES6+)
- Chart.js for visualizations
- Fetch API for backend communication

### Project Structure
```
frontend/
├── login.html      # Login and registration page
├── dashboard.html  # Main dashboard UI
├── script.js       # Shared utilities and API calls
├── style.css       # Dark theme styles
└── chart.min.js    # Chart.js library
```

### Boundaries
- **NEVER** modify backend Python files
- **NEVER** introduce frontend frameworks (React, Vue, Angular)
- **NEVER** commit node_modules or package.json
- **ALWAYS** use vanilla JavaScript (no build tools)
- **ALWAYS** maintain dark theme consistency
- **ALWAYS** handle API errors gracefully

### API Communication Pattern
```javascript
// Good: Proper error handling
async function fetchClientes() {
    try {
        const response = await fetch('/api/clientes', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching clients:', error);
        alert('Erro ao carregar clientes');
        return [];
    }
}
```

### UI Patterns
- Use semantic HTML5 elements
- Maintain dark theme: `background: #1a1a1a`, text: `#e0e0e0`
- Forms should have proper validation
- Show loading states during API calls
- Display user-friendly error messages
- Use confirm dialogs for destructive actions

---

## Testing Agent

**Name:** test_engineer  
**Description:** Expert in pytest and testing FastAPI applications

### Commands
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_auth_unit.py -v

# Run specific test
pytest tests/test_auth_unit.py::test_login -v
```

### Stack
- pytest for test framework
- pytest-asyncio for async tests
- TestClient from FastAPI for API testing

### Test Structure
```
tests/
├── test_auth_unit.py      # Authentication unit tests
├── test_sessions.py       # Session management tests
└── integration/           # Integration tests
```

### Boundaries
- **NEVER** modify production code unless fixing test-revealed bugs
- **ALWAYS** write tests that match existing patterns
- **ALWAYS** use test database (not production)
- **ALWAYS** clean up test data after tests
- **ALWAYS** test multi-tenant isolation

### Test Patterns

**Good: Proper test structure**
```python
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_client_success():
    """Test creating a client with valid data"""
    # Arrange: Set up test data
    empresa_response = client.post("/api/empresas/cadastrar", json={
        "nome_empresa": "Test Co",
        "email_login": "test@test.com",
        "senha": "SecurePass123"
    })
    
    # Act: Perform the action
    response = client.post("/api/clientes", json={
        "nome": "João Silva",
        "telefone": "11999999999"
    })
    
    # Assert: Verify results
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "João Silva"
    assert "id" in data
```

### Testing Checklist
- [ ] Test happy path (success case)
- [ ] Test error cases (invalid input, not found, etc.)
- [ ] Test authentication/authorization
- [ ] Test multi-tenant isolation
- [ ] Test edge cases
- [ ] Clean up test data
- [ ] Use meaningful test names

---

## Documentation Agent

**Name:** docs_writer  
**Description:** Technical documentation specialist for ClientFlow

### Commands
```bash
# No build needed - markdown files
```

### Boundaries
- **NEVER** modify code files
- **ONLY** modify .md files in root or docs directories
- **ALWAYS** keep documentation in sync with code
- **ALWAYS** use clear, concise language
- **ALWAYS** include code examples

### Documentation Files
- `README.md` - Main project documentation
- `README_DEPLOY.md` - Deployment guide
- `README_MIGRACAO_MULTI_TENANT.md` - Multi-tenant migration guide
- `SECRETS_REQUIRED.md` - Required environment variables

### Good Documentation Examples

**API Endpoint Documentation:**
```markdown
## POST /api/clientes

Create a new client for the authenticated company.

**Request Body:**
```json
{
  "nome": "João Silva",
  "telefone": "11999999999"
}
```

**Response (200):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "telefone": "11999999999",
  "empresa_id": 1,
  "data_primeiro_contato": "2024-01-15T10:30:00"
}
```

**Errors:**
- `400` - Invalid input data
- `401` - Not authenticated
```

### Style Guide
- Use clear headings (##, ###)
- Include code examples with syntax highlighting
- Use bullet points for lists
- Use tables for structured data
- Keep paragraphs short and focused
- Include emojis for visual cues (✅, ⚠️, 🚀)

---

## General Guidelines for All Agents

### Version Control
- Create focused, atomic commits
- Write clear commit messages
- Don't commit sensitive data
- Review changes before committing

### Code Quality
- Follow existing code style
- Keep functions small and focused
- Use descriptive names
- Add comments for complex logic
- Handle errors gracefully

### Collaboration
- Respect agent boundaries
- Maintain consistency across codebase
- Document significant changes
- Consider backward compatibility
