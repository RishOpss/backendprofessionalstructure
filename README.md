# Production Backend – Course API

A FastAPI + Supabase backend organised with a professional, layered project structure. This README explains **why** the project is structured this way and walks through the four building blocks it uses: **repositories**, **dependencies**, **middleware** and **exception handling**.

## Project Structure

```text
app/
├── main.py                      # App entry point: creates the app, adds middleware, mounts routers
├── Dockerfile                   # Container image (runs `uvicorn main:app`)
├── requirements.txt             # Pinned dependencies for Docker
├── api/
│   └── v1/                      # Versioned API (v2 can live beside it without breaking clients)
│       ├── router.py            # Aggregates endpoint routers under /api/v1
│       └── endpoints/
│           └── courses.py       # HTTP layer for /courses
├── schemas/
│   └── course.py                # Pydantic models: request/response validation
├── services/
│   └── course_service.py        # Business logic + raising HTTP errors
├── repository/
│   └── courses_repository.py    # Data-access layer: all Supabase queries live here
├── dependencies/
│   └── db.py                    # get_db(): injects the Supabase client via Depends()
├── middleware/
│   └── timing.py                # Adds an X-Process-Time header to every response
└── core/
    ├── config.py                # Settings loaded from .env
    └── database.py              # Supabase client setup
```

## Why This Structure?

| Layer                  | Responsibility                                                     | Should NOT                           |
| ---------------------- | ------------------------------------------------------------------ | ------------------------------------ |
| **`main.py`**          | Build the app, register routers and middleware                     | Contain business logic               |
| **`api/v1/endpoints`** | Parse requests, inject dependencies, call a service, return data   | Talk to the database directly        |
| **`schemas`**          | Define and validate the shape of input and output data             | Contain logic                        |
| **`services`**         | Business rules, deciding when something is an error (e.g. 404)     | Write SQL / Supabase queries         |
| **`repository`**       | Run queries against Supabase/Postgres and return raw rows          | Contain business rules or raise HTTP |
| **`dependencies`**     | Provide shared inputs (DB client, later auth user) via `Depends`   | Hold request-specific state          |
| **`middleware`**       | Process every request/response (timing, logging, CORS)             | Handle one specific route            |
| **`core`**             | Config and DB client: things the whole app uses                    | Depend on other app layers           |

### Request flow

```text
Client ──► Middleware (timing) ──► Router /api/v1 ──► Endpoint ──► Service ──► Repository ──► Supabase
                                                        │  ▲          │
                                       Depends(get_db) ─┘  │          └─ raises HTTPException (404)
                                       Schemas validate ───┘
```

Each layer only talks to the one directly below it, which gives you:

- **Separation of concerns**: change the DB without touching endpoints.
- **Testability**: swap the DB via dependency overrides; test services without HTTP.
- **Versioning**: ship `/api/v2` without breaking `/api/v1` clients.
- **Scalability**: new features are new files, not edits to a giant `main.py`.

---

## 1. Repository Pattern

**Goal:** keep every database query in one place, so the rest of the app never knows *how* data is stored.

`app/repository/courses_repository.py`:

```python
def get_all(db):
    response = db.table("courses").select("*").execute()
    return response.data

def get_by_id(course_id: int, db):
    response = db.table("courses").select("*").eq("course_id", course_id).execute()
    return response.data[0] if response.data else None

def create(db, course: Course):
    response = db.table("courses").insert(course.dict()).execute()
    return response.data[0]
```

Rules of thumb:

- Repositories **return data or `None`**; they don't decide what "not found" means for the API.
- They receive the DB client as an argument instead of importing it, so a test can pass in a fake.
- If you move from Supabase to SQLAlchemy, only this layer changes.

## 2. Dependencies (`Depends`)

**Goal:** declare what an endpoint needs and let FastAPI provide it, instead of importing globals everywhere.

`app/dependencies/db.py`:

```python
from core.database import supabase
from supabase import Client

def get_db() -> Client:
    return supabase
```

Used in `app/api/v1/endpoints/courses.py`:

```python
@router.get("/{course_id}", response_model=Course)
def get_course_by_id(course_id: int, db = Depends(get_db)):
    return course_service.get_course_by_id(db, course_id)
```

The client then flows **endpoint → service → repository** as a parameter.

Why it matters:

- **One place to change** how the DB client is created (e.g. per-request client, user JWT).
- **Easy testing**: `app.dependency_overrides[get_db] = lambda: fake_db`.
- The same pattern later powers auth (`get_current_user`), pagination and settings.

## 3. Middleware

**Goal:** run code on *every* request/response without touching any route.

`app/middleware/timing.py`:

```python
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)           # run the rest of the app
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

Registered in `app/main.py`:

```python
app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
```

Everything before `call_next` runs on the way **in**, everything after runs on the way **out**. Check it with:

```bash
curl -i http://localhost:8000/health   # look for the X-Process-Time header
```

Typical uses: timing, request logging, request IDs, CORS (`CORSMiddleware`), rate limiting.

## 4. Exception Handling

**Goal:** turn "something went wrong" into the correct HTTP status code instead of a generic 500.

`app/services/course_service.py`:

```python
def get_course_by_id(course_id: int, db):
    try:
        course = courses_repository.get_by_id(db, course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found",
            )
        return course
    except HTTPException:
        raise
```

How errors map to responses:

| Situation                               | Who handles it          | Response                             |
| --------------------------------------- | ----------------------- | ------------------------------------ |
| Body/path fails Pydantic validation     | FastAPI automatically   | `422 Unprocessable Entity`           |
| Course doesn't exist                    | Service `HTTPException` | `404 {"detail": "Course not found"}` |
| Unhandled error (e.g. Supabase failure) | Nobody yet              | `500 Internal Server Error`          |

Key ideas:

- The **repository** returns `None`; the **service** decides that `None` means 404.
- `except HTTPException: raise` re-raises deliberate HTTP errors so a broader `except` can't swallow them.
- Next step: catch `postgrest.exceptions.APIError` (already imported) and map DB errors such as duplicate keys to `409 Conflict`, or register global handlers with `@app.exception_handler(...)` in `main.py`.

---

## Endpoints

All resource routes are mounted under `/api/v1` (see `app/api/v1/router.py`):

| Method | Path                          | Description                     |
| ------ | ----------------------------- | ------------------------------- |
| GET    | `/`                           | HTML welcome page               |
| GET    | `/health`                     | Health check                    |
| GET    | `/api/v1/courses/`            | List all courses                |
| GET    | `/api/v1/courses/{course_id}` | Get one course (404 if missing) |
| POST   | `/api/v1/courses/`            | Create a course                 |

Course body (`app/schemas/course.py`):

```json
{ "course_id": 1, "name": "Backend Engineering", "duration": 12 }
```

`course_id` and `duration` must be > 0; `name` must be 2–50 characters.

Interactive docs are served at `/docs` (Swagger UI) and `/redoc`.

## Getting Started

**Requirements:** Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
# 1. Install dependencies
uv sync
```

Then create a `.env` file in the `app/` directory (it is git-ignored):

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-key
```

```bash
# 2. Run the dev server (imports are relative to app/)
cd app
uv run uvicorn main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to explore the API.

### Docker

```bash
cd app
docker build -t productionbackend .
docker run --env-file .env -p 8000:8000 productionbackend
```

## Adding a New Resource (e.g. `teachers`)

1. **Schema**: `app/schemas/teacher.py` (Pydantic models)
2. **Repository**: `app/repository/teachers_repository.py` (Supabase queries, take `db` as a parameter)
3. **Service**: `app/services/teacher_service.py` (business rules, raise `HTTPException` for 404/409)
4. **Endpoint**: `app/api/v1/endpoints/teachers.py` (an `APIRouter` using `db = Depends(get_db)`)
5. **Register** it in `app/api/v1/router.py`:

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
