# AGENTS.md - Guidelines for Agentic Coding

This project is a **Sistema de Asistencia** (Attendance System) for Cooperativa Minera Poopó R.L., consisting of:
- **Backend**: FastAPI (Python) with SQLAlchemy ORM
- **Frontend**: Nuxt.js 4 (Vue 3) with Pinia state management

## Project Structure

```
Cooperativa_Poopo/
├── sistema-asistencia-backend/     # FastAPI backend
│   ├── main.py                     # FastAPI app entry point
│   ├── config.py                   # Configuration
│   ├── database.py                 # SQLAlchemy setup
│   ├── models/                     # SQLAlchemy models
│   ├── schemas/                    # Pydantic schemas
│   ├── services/                   # Business logic (service layer)
│   ├── repositories/               # Data access layer
│   ├── routes/                     # API endpoints
│   ├── utils/                      # Utilities (security, JWT, QR)
│   └── requirements.txt
└── sistema-asistencia-frontend/   # Nuxt.js frontend
    ├── app/
    │   ├── pages/                  # Vue page components
    │   ├── stores/                 # Pinia stores
    │   ├── plugins/                # Nuxt plugins
    │   └── assets/                 # Static assets
    ├── nuxt.config.js
    └── package.json
```

---

## Build & Development Commands

### Backend (FastAPI)

```bash
# Navigate to backend
cd sistema-asistencia-backend

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run with specific settings
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

### Frontend (Nuxt.js)

```bash
# Navigate to frontend
cd sistema-asistencia-frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Generate static site
npm run generate
```

### Running a Single Test

**No test framework is currently configured.** To add tests:
- Backend: Use `pytest` with `pytest-asyncio`
- Frontend: Use `vitest` or `nuxt/test`

---

## Code Style Guidelines

### Backend (Python)

#### Imports
- Standard library first, then third-party, then local
- Use absolute imports (e.g., `from routes import api_router`)
- Group: stdlib → external → internal with blank lines between

```python
# Correct order
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from models.user import User
from schemas.user import UserCreate
from services.auth_service import auth_service
```

#### Naming Conventions
- **Variables/functions**: `snake_case` (e.g., `user_repo`, `get_by_username`)
- **Classes**: `PascalCase` (e.g., `AuthService`, `UserResponse`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_LOGIN_ATTEMPTS`)
- **Database tables**: `snake_case` plural (e.g., `users`, `devices`)

#### Types & Type Hints
- Always use type hints for function parameters and return values
- Use `Optional[X]` instead of `X | None` for compatibility
- Use Pydantic models for request/response schemas

```python
def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID with type hints."""
    return db.query(User).filter(User.id == user_id).first()
```

#### Error Handling
- Use FastAPI's `HTTPException` for API errors
- Return appropriate HTTP status codes:
  - `200` - Success
  - `201` - Created
  - `400` - Bad Request
  - `401` - Unauthorized
  - `403` - Forbidden
  - `404` - Not Found
  - `500` - Internal Server Error

```python
from fastapi import HTTPException, status

if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )
```

#### Database Models
- Use SQLAlchemy with proper relationships
- Always define `__tablename__` explicitly in lowercase plural
- Use `autoincrement=True` for primary keys
- Add indexes for frequently queried columns

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
```

#### Pydantic Schemas
- Use `BaseModel` for request/response
- Use `ConfigDict(from_attributes=True)` for ORM compatibility
- Separate `*Base`, `*Create`, `*Update`, `*Response` schemas

```python
class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
```

#### Service Layer Pattern
- Business logic goes in `services/`
- Use singleton pattern for services: `auth_service = AuthService()`
- Services receive `db: Session` as first parameter

---

### Frontend (Vue/Nuxt)

#### Composition API
- Use `<script setup>` syntax
- Use composables for reusable logic

```vue
<script setup>
const authStore = useAuthStore()
const router = useRouter()

const loading = ref(false)
const error = ref(null)
</script>
```

#### State Management (Pinia)
- Use Pinia stores in `app/stores/`
- Follow naming: `useXxxStore` for store exports
- Use actions for async operations, getters for computed state

```javascript
// stores/users.js
export const useUsersStore = defineStore('users', {
  state: () => ({
    users: [],
    loading: false
  }),
  actions: {
    async fetchUsers() {
      // async logic
    }
  }
})
```

#### API Calls
- Use `$fetch` from Nuxt (or `useFetch`)
- Include `Authorization: Bearer` header for authenticated requests
- Handle errors consistently

```javascript
const response = await $fetch(`${authStore.apiUrl}/api/users/`, {
  headers: {
    Authorization: `Bearer ${authStore.token}`
  }
})
```

#### Template Structure
- Use semantic HTML elements
- Follow Bulma CSS class conventions (already configured)
- Group related functionality in template sections

#### Styling
- Use scoped styles in Vue components
- Follow Bulma's class naming patterns
- Keep custom SCSS in `assets/styles/`

---

## API Endpoints Pattern

The backend follows REST conventions:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/` | List users (with pagination) |
| POST | `/api/users/` | Create user |
| GET | `/api/users/{id}` | Get single user |
| PUT | `/api/users/{id}` | Update user |
| DELETE | `/api/users/{id}` | Delete user |

**Note**: Always include trailing slash in frontend API calls (`/api/users/` not `/api/users`)

---

## Common Patterns

### Repository Pattern
```python
# repositories/user_repo.py
user_repo = UserRepo()

class UserRepo:
    def get_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()
```

### Dependency Injection
```python
# In routes
@router.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return user_repo.get_all(db)
```

---

## Environment Variables

Create `.env` files as needed (do not commit secrets):

```env
# Backend
DATABASE_URL=postgresql://user:pass@localhost/dbname
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
CLOUDINARY_API_KEY=xxx
CLOUDINARY_API_SECRET=xxx
```

---

## Additional Notes

- The backend uses PostgreSQL with SQLAlchemy
- Authentication uses JWT tokens
- QR code generation for device registration
- Cloudinary for image uploads
- CORS is configured to allow all origins (adjust for production)
