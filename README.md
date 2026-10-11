# Production Backend – Course & Student API

A FastAPI + Supabase backend organised with a professional, layered project structure. This README explains **why** the project is structured this way and how to apply the same pattern to any API you build.

## Project Structure

```text
app/
├── main.py                  # App entry point: creates FastAPI app, mounts routers
├── api/
│   └── v1/                  # Versioned API (v2 can live beside it without breaking clients)
│       ├── router.py        # Aggregates all endpoint routers under one prefix
│       └── endpoints/
│           ├── courses.py   # HTTP layer for /courses
│           └── students.py  # HTTP layer for /students
├── schemas/                 # Pydantic models: request/response validation
│   ├── course.py
│   └── students.py
├── services/                # Business logic, independent of HTTP
│   ├── course_service.py
│   └── student_service.py
├── repositories/            # (planned) Data-access layer: all DB queries live here
├── dependencies/            # (planned) Reusable FastAPI Depends(): auth, DB session, pagination
├── core/
│   ├── config.py            # Settings loaded from environment variables
│   ├── database.py          # Supabase client setup
│   ├── logging.py           # (planned) Logging configuration
│   └── exceptions.py        # (planned) Custom exceptions and handlers
└── middleware/              # (planned) CORS, request logging, rate limiting, etc.
```

Items marked *(planned)* are part of the target structure and are added as the project grows.

## Why This Structure?

| Layer | Responsibility | Should NOT |
| ----- | -------------- | ---------- |
| **`main.py`** | Build the app, register routers and middleware | Contain business logic |
| **`api/v1/endpoints`** | Parse requests, call a service, return responses and status codes | Talk to the database directly |
| **`schemas`** | Define and validate the shape of input and output data | Contain logic |
| **`services`** | Implement business rules (e.g. "a student can't enrol twice") | Know about HTTP or `Request` objects |
| **`repositories`** | Run queries against Supabase/Postgres | Contain business rules |
| **`dependencies`** | Share cross-cutting inputs (auth user, DB client) via `Depends` | Hold state |
| **`core`** | Config, logging, exceptions: things the whole app uses | Depend on other app layers |
| **`middleware`** | Process every request/response (CORS, timing, logging) | Handle one specific route |

### Request flow

```text
Client ──► Middleware ──► Router (api/v1) ──► Endpoint ──► Service ──► Repository ──► Supabase
                                                │            │
                                          Schemas validate   Business rules
                                          input/output
```

Each layer only talks to the one directly below it, which gives you:

- **Separation of concerns**: change the DB without touching endpoints.
- **Testability**: test services without HTTP, endpoints with mocked services.
- **Versioning**: ship `/api/v2` without breaking `/api/v1` clients.
- **Scalability**: new features are new files, not edits to a giant `main.py`.
- **Team-friendliness**: people work in different layers with fewer merge conflicts.

## Endpoints

All routes are mounted under `/api` (see `app/api/v1/router.py`):

| Prefix          | Tag      | Defined in                         |
| --------------- | -------- | ---------------------------------- |
| `/api/students` | students | `app/api/v1/endpoints/students.py` |
| `/api/courses`  | courses  | `app/api/v1/endpoints/courses.py`  |

Interactive docs are served at `/docs` (Swagger UI) and `/redoc`.

## Getting Started

**Requirements:** Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
# 1. Install dependencies
uv sync

# 2. Configure environment
cp .env.example .env     # then set your Supabase URL and key
```

Example `.env`:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-key
```

```bash
# 3. Run the dev server
uv run uvicorn app.main:app --reload
```

Open <http://localhost:8000/docs> to explore the API.

## Adding a New Resource (e.g. `teachers`)

1. **Schema**: `app/schemas/teacher.py` (Pydantic models)
2. **Service**: `app/services/teacher_service.py` (business logic)
3. **Endpoint**: `app/api/v1/endpoints/teachers.py` (an `APIRouter`)
4. **Register**: add it to `app/api/v1/router.py`:

   ```python
   api_router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
   ```

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/): web framework
- [Supabase](https://supabase.com/): Postgres database and backend platform
- [Uvicorn](https://www.uvicorn.org/): ASGI server
- [uv](https://docs.astral.sh/uv/): dependency and environment management

## Further Reading

See [`FLOW.md`](FLOW.md) for the request flow walkthrough.
