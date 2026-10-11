# Request Flow

## Layered architecture

```mermaid
flowchart LR
    Client([Client]) -->|HTTP /api/v1/...| Main[main.py<br/>FastAPI app]
    Main --> Router[api/v1/router.py<br/>prefix /api/v1]
    Router --> EP[endpoints/<br/>students.py, courses.py]
    EP -->|Pydantic validation| Schemas[schemas/<br/>StudentCreate, StudentUpdate]
    EP --> Svc[services/<br/>business rules]
    Svc --> Repo[repositories/<br/>table queries]
    Repo --> DB[core/database.py<br/>Supabase client]
    Cfg[core/config.py<br/>.env: SUPABASE_URL, SUPABASE_KEY] -.-> DB
    DB --> SB[(Supabase<br/>students, courses)]
    SB -->|rows| Repo -->|data / None| Svc -->|result / error| EP -->|JSON| Client
```

## Create student (POST /api/v1/students/)

```mermaid
sequenceDiagram
    participant C as Client
    participant E as students endpoint
    participant S as student_service
    participant SR as student_repository
    participant CS as course_service
    participant DB as Supabase

    C->>E: POST /students {student_id, name, age, course_id}
    E->>E: Validate StudentCreate (ids > 0, name 2-100, age 1-120)
    alt invalid body
        E-->>C: 422 Unprocessable Entity
    end
    E->>S: create_student(student)
    S->>SR: get_by_id(student_id)
    SR->>DB: select where student_id = ?
    DB-->>SR: rows
    alt student exists
        S-->>E: ValueError "Student already exists"
    end
    S->>CS: get_course(course_id)
    alt course missing
        CS-->>S: LookupError
    end
    S->>SR: create(student.model_dump())
    SR->>DB: insert into students
    DB-->>SR: inserted row
    SR-->>S: row
    S-->>E: row
    E-->>C: 200 JSON student
```

## Notes

- `get_students` (GET `/students/`) skips the checks: endpoint → service → repository `get_all()` → Supabase, ordered by `student_id`.
- `ValueError` and `LookupError` raised in services are not caught by the endpoints yet, so they currently surface as 500 responses. Mapping them to 409 / 404 (via `HTTPException` or exception handlers) is the usual next step.
- `update_student`, `get_student` and `delete_student` exist in the service but are not routed in `students.py` yet.
