# E-Learning Platform - AI Coding Agent Instructions

## Architecture Overview

**Stack**: React 19 (Vite) + FastAPI + SQLAlchemy with SQLite
- **Frontend**: `/client` - React with Redux Toolkit, Zustand for auth state, TailwindCSS, React Hook Form
- **Backend**: `/server` - FastAPI with role-based access control (Student/Instructor)
- **Database**: SQLAlchemy ORM models define User, Course, Lesson, Enrollment with relationships

**Key Design Patterns**:
- Frontend can toggle Mock API via `VITE_USE_MOCK_API` env var for development without backend
- JWT token stored in localStorage with auto-logout on 401 responses
- Role-based routing with `ProtectedRoute` component wrapping instructor-only views

## Critical Data Flow

1. **Auth Flow**: Login → JWT token stored → `useAuthStore` hydrates user on app load
2. **Course Enrollment**: Student enrolls → creates `Enrollment` record → accesses `Lesson` content
3. **Instructor Content**: Instructor creates `Course` → adds `Lesson` items → students view via `CoursePlayer`

**Database Relationships** (critical for queries):
- `User` has many `Course` (as instructor) and `Enrollment`
- `Course` has many `Lesson` (cascade delete) and `Enrollment` (cascade delete)
- `Lesson` belongs to `Course`
- `Enrollment` links `User` ↔ `Course`

## Developer Workflows

**Frontend Development**:
```bash
cd client && npm run dev    # Starts Vite on http://localhost:5173
npm run build              # Production build
npm run lint              # ESLint check
```

**Backend Development**:
```bash
cd server && python -m uvicorn app.main:app --reload  # Auto-reload on changes
# Or configure IDE to run main.py directly
```

**Database**: 
- Migrations use Alembic (in requirements.txt)
- Seed data auto-runs on app startup via `seed_data()` in main.py
- Uses SQLite for dev (FILE: `learnflow.db`)

## Project-Specific Conventions

### Backend (FastAPI)

**Route Organization** (FILE: `app/api/routers/`):
- Each resource gets its own router module (`courses.py`, `lessons.py`, etc.)
- All routers registered in `main.py` with distinct prefixes
- Use `require_instructor` or `get_current_user` dependencies for auth gates

**Example Pattern** (FILE: `app/api/routers/courses.py`):
```python
@router.post("/", response_model=CourseSchema, status_code=status.HTTP_201_CREATED)
def create_course(
    course_data: CourseCreate,
    instructor: User = Depends(require_instructor),  # Built-in auth check
    db: Session = Depends(get_db)
):
    course = Course(title=course_data.title, instructor_id=instructor.id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course
```

**Access Control** (FILE: `app/api/deps.py`):
- `get_current_user`: Extracts user from JWT
- `require_instructor`: Enforces user.role == "instructor"
- `ensure_enrolled_or_instructor`: Custom check for lesson access (instructor owns course OR student enrolled)

### Frontend (React/Zustand)

**State Management** (FILE: `client/src/store/authStore.js`):
- Use Zustand for global auth (`token`, `user`)
- `hydrate()` called on app load to restore session from localStorage
- Token persisted as `learnflow_token` in localStorage

**API Layer** (FILE: `client/src/api/client.js`):
- Axios instance with automatic Bearer token injection in request interceptor
- 401 response triggers auto-logout + redirect to `/login`
- Conditionally uses mock API based on `VITE_USE_MOCK_API` env (see `mockApi` in `/mocks`)

**Component Patterns** (FILE: `client/src/components/ProtectedRoute.jsx`):
```jsx
<ProtectedRoute allowedRoles={["instructor"]}>
  <Outlet />  // Wrapped routes only render if user authenticated + correct role
</ProtectedRoute>
```

**UI Components** (FILE: `client/src/components/ui/`):
- Radix UI primitives with TailwindCSS (see `Button.tsx`, `Card.jsx`)
- Use `clsx` for conditional classes, `class-variance-authority` for component variants

## Integration Points & External Dependencies

| Layer | Key Dependencies | Purpose |
|-------|------------------|---------|
| Frontend | axios, react-router-dom, zustand, react-hook-form, framer-motion | HTTP client, routing, state, forms, animations |
| Backend | FastAPI, SQLAlchemy 2.0, psycopg2-binary (or sqlite), passlib, python-jose | Framework, ORM, DB driver, password hashing, JWT |
| Common | pydantic, zod | Data validation (backend schemas, frontend form schemas) |

**CORS**: Limited to `localhost:5173` in `main.py` - update `origins` list for production

## Adding New Features - Quick Checklist

1. **New Resource Type**: Create model in `/server/app/models/`, schema in `/schemas/`, router in `/api/routers/`
2. **New API Endpoint**: Follow courses.py pattern with `Depends(get_db)` + auth decorators
3. **New Frontend Page**: Add to `/client/src/pages/`, route in App.jsx, wrap with ProtectedRoute if needed
4. **Role-Gated Views**: Use `ProtectedRoute allowedRoles={["instructor"]}` wrapper
5. **Forms**: Use react-hook-form + Zod schema (see existing forms for pattern)

## Notes for AI Agents

- **Backward compatibility**: Database migrations tracked by Alembic - run `alembic upgrade head` if models change
- **Testing**: No test files present; mock API in `/mocks` used for frontend dev without backend
- **Environment**: Copy `.env.example` or set vars: `DATABASE_URL`, `JWT_SECRET`, `VITE_API_BASE_URL`, `VITE_USE_MOCK_API`
- **Common gotcha**: Cascade deletes on Course/Lesson - deleting a course auto-removes all enrollments and lessons
