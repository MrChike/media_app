# 🏗️ Architecture

## Codebase Design

```bash
media_app/

├── base/                                # Core feature module
│   ├── __init__.py
│   ├── router.py                        # Defines HTTP API endpoints and maps them to controller functions
│   ├── controller.py                    # Handles request-response cycle; delegates business logic to services
│   ├── service.py                       # Core business logic for async I/O operations
│   ├── model.py                         # SQLAlchemy ORM models representing database tables
│   ├── schema.py                        # Pydantic models for input validation and output serialization
│   ├── dependencies.py                  # Module-specific DI components like authentication and DB sessions
│   └── tasks.py                         # Core business logic for CPU-bound operations

├── movies/                              # Movie feature module (same layout as base)
│   ├── __init__.py
│   ├── router.py
│   ├── controller.py
│   ├── service.py
│   ├── model.py
│   ├── schema.py
│   ├── dependencies.py
│   └── tasks.py

├── static/                              # (Optional) Static files (e.g., images, CSS)
├── templates/                           # (Optional) Jinja2 or HTML templates for frontend rendering
├── docs/                                # (Optional) API documentation, design specs, or OpenAPI enhancements

├── shared/                              # Project-wide shared codebase
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── base_settings.py             # Base config for environments
│   │   └── settings.py                  # Pydantic-based config management
│   ├── db/
│   │   ├── __init__.py
│   │   └── connection.py                # DB engine/session handling
│   ├── dependencies/                    # Shared DI functions (e.g., auth, DB session)
│   │   └── __init__.py
│   ├── middleware/                      # Global middlewares (e.g., logging, error handling)
│   │   └── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── external_apis/               # Third-party integrations
│   │   │   ├── __init__.py
│   │   │   └── omdb_movies.py           # Integration with OMDB API
│   │   └── internal_operations/         # CPU-intensive logic, background tasks
│   │       └── __init__.py
│   └── utils/                           # Generic helpers
│       ├── __init__.py
│       └── fetch_request_with_error_handling.py  # Error-resilient HTTP requests

├── scripts/                             # Developer or DevOps utilities
│   ├── __init__.py
│   └── sanity_check.py                  # A friendly reminder not to lose your mind while debugging

tests/                                   # Root of all tests
├── __init__.py
│
├── unit/                                # Fast, isolated logic-level tests
│   ├── __init__.py
│   ├── base/
│   │   ├── __init__.py
│   │   └── test_service.py
│   └── movies/
│       ├── __init__.py
│       ├── test_controller.py
│       ├── test_service.py
│       └── test_tasks.py
│
├── integration/                         # DB/API/network dependent tests
│   ├── __init__.py
│
├── e2e/                                 # High-level, full user flow tests
│   ├── __init__.py
│
├── system/                              # System resilience, performance, fault-tolerance tests
│   ├── __init__.py

├── migrations/                          # Alembic migration files
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/                        # Versioned migration scripts

├── alembic.ini                          # Alembic configuration for database migrations
├── celeryconfig.py                      # Celery settings for async task queue

├── docker-compose.api.yaml              # Docker Compose API
├── docker-compose.db.yaml               # Docker Compose DB
├── Dockerfile                           # Base app Dockerfile
├── Dockerfile.nginx                     # Nginx reverse proxy Dockerfile
├── nginx.conf                           # Nginx configuration
├── entrypoint.sh                        # Shell script to run app container
├── series_a_setup.sh                    # SeriesA Environment setup script
├── series_b_setup.sh                    # SeriesB Environment setup script

├── .example.env                         # Template for environment variables
├── .coveragerc                          # Code coverage settings
├── .gitignore                           # Files and folders ignored by Git

├── main.py                              # FastAPI application entrypoint
├── pytest.ini                           # Pytest configuration
├── requirements.txt                     # Python dependency list
├── JOURNAL.md                           # Development log: issues faced, solutions, and resources
└── README.md                            # Project overview, setup, and usage

```